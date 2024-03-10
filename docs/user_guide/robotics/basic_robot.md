# Getting Started with Robot

:::{note}
This tutorial assumes you have read the **get started** section. The assets (robot) and full scripts can be found at [here](<#full-script>).
:::

In this tutorial, you will learn the following:

* Load a robot (URDF)
* Set joint positions
* Compensate passive forces
* Control the robot by torques

## Set up the engine, renderer and scene

First of all, let's set up the simulation environment as illustrated in <project:#hello_world>.
```python
scene = sapien.Scene()
scene.add_ground(0)

scene.set_ambient_light([0.5, 0.5, 0.5])
scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

viewer = scene.create_viewer()
viewer.set_camera_xyz(x=-2, y=0, z=1)
viewer.set_camera_rpy(r=0, p=-0.3, y=0)
```

## Load a robot URDF

Robots models provided by robot manufacturers are commonly represented in the
[URDF XML](http://wiki.ros.org/urdf/XML) format. In this tutorial, we take
[Kinova Jaco2 arm](https://github.com/Kinovarobotics/kinova-ros) as an example.

```python
loader = scene.create_urdf_loader()
loader.fix_root_link = fix_root_link
robot = loader.load("assets/jaco2/jaco2.urdf")
robot.set_root_pose(sapien.Pose([0, 0, 0], [1, 0, 0, 0]))
```

Note that URDF loader has the `fix_root_link` property. If it is set to true
(by default), then the root link of the robot will be fixed. Otherwise, it is
allowed to move freely.

The robot is loaded as `PhysxArticulation`, which is a tree of links connected
by joints. We can set the pose of its root link through `set_root_pose(...)`.

If you run the example with `demo(fix_root_link=False, balance_passive_force=False)`, 
you will observe the following "falling-down" robot arm. We will see how to keep the robot at a certain pose later.

```{figure} assets/robot_fall.gif
:width: 640px
:align: center
:figclass: align-center

The robot arm falls down
```

:::{note}
When a robot is already loaded, it is independent of the URDF loader. Changing
properties of the loader will have no effect on the loaded robot.
:::

## Compensate passive forces (e.g. gravity)

You may find that even if you run the example with `fix_root_link=True`, the robot still can not maintain its initial joint positions.
It is due to gravitational force and other possible passive forces, like Coriolis and Centrifugal force.

```{figure} assets/robot_fix.gif
:width: 640px
:align: center
:figclass: align-center

The root link (base) of the robot is fixed, but it still falls down due to passive forces.
```

For a real robot, gravity compensation is done by an internal controller hardware.
So it is usually desirable to skip this troublesome calculation of how to compensate gravity.
SAPIEN provides `compute_passive_force` to compute desired forces or torques on joints to compensate passive forces.
In this example, we only consider gravity as well as coriolis and centrifugal force.

```python
while not viewer.closed:
    for _ in range(4):  # render every 4 steps
        if balance_passive_force:
            qf = robot.compute_passive_force(
                gravity=True,
                coriolis_and_centrifugal=True,
            )
            robot.set_qf(qf)
        scene.step()
    scene.update_render()
    viewer.render()
```

We recompute the compensative torque every step and control the robot by `set_qf(qf)`.
`qf` should be a concatenation of the force or torque to apply on each joint.
Its length is the degree of freedom, and its order is the same as that returned by `robot.get_joints()`.
Note that when `qf` is set, it will be applied every simulation step.
You can call `robot.get_qf()` to acquire its current value.

Now, if you run the example with `demo(fix_root_link=True, balance_passive_force=True)`, it is observed that the robot can stay at the target pose for a short period.
However, it will then deviate from this pose gradually due to numerical error.

```{figure} assets/robot_fix_balance.gif
    :width: 640px
    :align: center
    :figclass: align-center

The robot arm is able to stay at the target pose, but might deviate gradually due to numerical error.
The animation is accelerated.
```

:::{note}
   To avoid deviating from the target pose gradually,
   either we specify the damping (resistence proportional to velocity) of each joint in the URDF XML, or a controller can be used to compute desired extra forces or torques to keep the robot around the target pose.
   <project:#pid> will elaborate how to control the robot with a controller.
:::


### Disable Gravity

While compensating passive force is the most realistic way to simulate what
happens on a real robot, when building simulation, a more common approach to
achieve the same goal is to disable the gravity of all links.

```python
for link in robot.links:
    link.disable_gravity = True
```
This approach has the same effect as 
```python
robot.set_qf(robot.compute_passive_force(gravity=True, coriolis_and_centrifugal=False))
```

From a simulation point of view, these 2 methods are exactly equivalent. When
possible, `disable_gravity` is always preferred as it avoids expensive
computations of inverse and forward dynamics. While `disable_gravity` does not
account for Coriolis forces, such forces are typically very small at low
velocity.

(full-script)=
## Full Script
:::{dropdown} Assets
<path:assets/jaco2.zip>
:::

:::{dropdown} Code
```python
import sapien


def demo(fix_root_link, balance_passive_force):
    scene = sapien.Scene()
    scene.add_ground(0)

    scene.set_ambient_light([0.5, 0.5, 0.5])
    scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

    viewer = scene.create_viewer()
    viewer.set_camera_xyz(x=-2, y=0, z=1)
    viewer.set_camera_rpy(r=0, p=-0.3, y=0)

    # Load URDF
    loader = scene.create_urdf_loader()
    loader.fix_root_link = fix_root_link
    robot = loader.load("assets/jaco2/jaco2.urdf")
    robot.set_root_pose(sapien.Pose([0, 0, 0], [1, 0, 0, 0]))

    # Set initial joint positions
    arm_init_qpos = [4.71, 2.84, 0, 0.75, 4.62, 4.48, 4.88]
    gripper_init_qpos = [0, 0, 0, 0, 0, 0]
    init_qpos = arm_init_qpos + gripper_init_qpos
    robot.set_qpos(init_qpos)

    while not viewer.closed:
        for _ in range(4):  # render every 4 steps
            if balance_passive_force:
                qf = robot.compute_passive_force(
                    gravity=True,
                    coriolis_and_centrifugal=True,
                )
                robot.set_qf(qf)
            scene.step()
        scene.update_render()
        viewer.render()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--fix-root-link", action="store_true")
    parser.add_argument("--balance-passive-force", action="store_true")
    args = parser.parse_args()

    demo(
        fix_root_link=args.fix_root_link,
        balance_passive_force=args.balance_passive_force,
    )


if __name__ == "__main__":
    main()
```
:::
