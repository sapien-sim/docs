# Drive Robot with PID Controller

:::{note}
Please first complete <project:#basic_robot> before continuing.
:::

A fundamental problem  in robotics is how to apply forces on the joints of a robot to drive them to target positions.
Such low-level control is the basis for applications, e.g., following a trajectory.

In this tutorial, you will learn the following:

* Drive the robot with the PhysX internal PD controller
* Write your own PID controller

```{figure} assets/pid_internal.gif
:width: 640px
:align: center
:figclass: align-center

Drive the robot with the internal PD controller
```
    
## Setup

As before, we first set up the simulation world.
Note that we decrease the timestep, which is helpful for the simple PID controller implemented in this example.

```python
scene = sapien.Scene()
# A small timestep for higher control accuracy
scene.set_timestep(1 / 2000.0)
scene.add_ground(0)

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-2, y=0, z=1)
viewer.set_camera_rpy(r=0, p=-0.3, y=0)

# Load URDF
loader = scene.create_urdf_loader()
loader.fix_root_link = True
robot = loader.load("../assets/jaco2/jaco2.urdf")
robot.set_root_pose(sapien.Pose([0, 0, 0], [1, 0, 0, 0]))

# Set joint positions
arm_zero_qpos = [0, 3.14, 0, 3.14, 0, 3.14, 0]
gripper_init_qpos = [0, 0, 0, 0, 0, 0]
zero_qpos = arm_zero_qpos + gripper_init_qpos
robot.set_qpos(zero_qpos)
arm_target_qpos = [4.71, 2.84, 0.0, 0.75, 4.62, 4.48, 4.88]
target_qpos = arm_target_qpos + gripper_init_qpos
```

## Drive the robot with PhysX internal PD controller

```python
active_joints = robot.get_active_joints()
if use_internal_drive:
    for joint_idx, joint in enumerate(active_joints):
        joint.set_drive_property(stiffness=20, damping=5, force_limit=1000, mode="force")
        joint.set_drive_target(target_qpos[joint_idx])
    # Or you can directly set joint targets for an articulation
    # robot.set_drive_target(target_qpos)
```

SAPIEN provides builtin PhysX **drives** (controllers) to control either the position or speed of a joint.
For each active joint (with non-zero degree of freedom), we can call `set_drive_property(...)` to set its drive properties: `stiffness` and `damping`.
The drive is a **proportional derivative drive**, which applies a force as follows: 

<p align="center">
    <i>force = stiffness * (target_position - position) + damping * (target_velocity - velocity)</i>
</p>

The `stiffness` and `damping` can be regarded as the *P* and *D* term in a typical [PID controller](https://en.wikipedia.org/wiki/PID_controller).
They implies the extent to which the drive attempts to achieve the target position and velocity respectively.

The `force_limit` is the maximum force or torque allowed for this drive to
output. The `mode` parameter can be either `"force"` or `"acceleration"`. In
acceleration mode, the actual force excerted by the drive is scaled by the
inertia of connected links, allowing the same set of `stiffness` and `damping`
parameter to produce similar behavior for robots of different masses.

:::{note}
   The PhysX backend in fact integrates the drive into the PhysX solver.
   The force applied will be computed implicitly every simulation step.
:::

The initial target position and velocity of a joint are zero by default.
You can call `joint.set_drive_target(...)` to set the target position of a joint, or `robot.set_drive_target(...)` to set the target positions of all the joints of the robot.
Similarly, you can also call `set_drive_velocity_target(...)` to set the target velocity.

:::{note}
   If you do not balance the passive force or disable gravity, the robot can never reach the desired pose (but maybe a close pose) given in `set_drive_target` due to steady-state-error.
:::

## Write your own PID controller

You can write your own PID controller, if you need an integrator term *I* to
compensate some steady-state-error which can not be compensated by
``compensate_passive_force``.

```python
class SimplePID:
    def __init__(self, kp=0.0, ki=0.0, kd=0.0):
        self.p = kp
        self.i = ki
        self.d = kd

        self._cp = 0
        self._ci = 0
        self._cd = 0

        self._last_error = 0

    def compute(self, current_error, dt):
        self._cp = current_error
        self._ci += current_error * dt
        self._cd = (current_error - self._last_error) / dt
        self._last_error = current_error
        signal = (self.p * self._cp) + (self.i * self._ci) + (self.d * self._cd)
        return signal

def pid_forward(
    pids: list, target_pos: np.ndarray, current_pos: np.ndarray, dt: float
) -> np.ndarray:
    errors = target_pos - current_pos
    qf = [pid.compute(error, dt) for pid, error in zip(pids, errors)]
    return np.array(qf)
```

```python
active_joints = robot.get_active_joints()

if use_external_pid:
    pids = []
    pid_parameters = [
        (40, 5, 2), (40, 5, 2), (40, 5, 2), (20, 5.0, 2),
        (5, 0.8, 2), (5, 0.8, 2), (5, 0.8, 0.4),
        (0.1, 0, 0.02), (0.1, 0, 0.02), (0.1, 0, 0.02),
        (0.1, 0, 0.02), (0.1, 0, 0.02), (0.1, 0, 0.02),
    ]
    for i, joint in enumerate(active_joints):
        pids.append(SimplePID(*pid_parameters[i]))
```

We provide a very simple implementation here, the parameters of which are not carefully tuned.
You can try to add extra tricks for integration or error propagation, to improve the stability of your own controller.

```python
while not viewer.closed:
    for _ in range(4):  # render every 4 steps
        qf = robot.compute_passive_force(
            gravity=True,
            coriolis_and_centrifugal=True,
        )
        if use_external_pid:
            pid_qf = pid_forward(
                pids, target_qpos, robot.get_qpos(), scene.get_timestep()
            )
            qf += pid_qf
        robot.set_qf(qf)
        scene.step()
    scene.update_render()
    viewer.render()
```

```{figure} assets/pid_external.gif
:align: center
:figclass: align-center

Drive the robot with the simple PID controller
```
   
:::{note}
   In most cases, it is recommended to use the internal drive rather than your
   own PID. The PhysX internal drive is much more efficient and stable when the
   parameters are not carefully tuned. If the *I* term is required, you may
   compute accumulated error and modify the `target_position` to achieve similar
   effect.
:::

:::{warning}
   The parameters (``stiffness`` and ``damping``) for the internal drive in this example can not be directly used for downstream tasks like manipulation. 
:::
