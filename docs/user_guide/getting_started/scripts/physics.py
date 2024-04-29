"""Basic physics in Sapien.

This script provides an example where an object is sliding down the slope and bouncing on the ground.
The user can modify physical properties, like static and dynamic friction, to see different behaviors.
The default physical properties can be modified through sapien.PhysxSceneConfig.
The physical material can be specified before each actor is built.

Concepts:
    - sapien.physx.PhysxSceneConfig containing default physical parameters
    - sapien.physx.PhysxMaterial
    - kinematic actors
    - sapien.physx.PhysxRigidBodyComponent.set_linear_damping, sapien.physx.PhysxRigidBodyComponent.set_angular_damping
    - Get kinematic quantities through
        sapien.Entity.get_pose(), sapien.physx.PhysxRigidBodyComponent.get_linear_velocity(), sapien.physx.PhysxRigidBodyComponent.get_angular_velocity()
"""

import sapien as sapien
from sapien.utils import Viewer
import numpy as np
from  transforms3d.quaternions import axangle2quat

def create_box(
        scene: sapien.Scene,
        pose: sapien.Pose,
        half_size,
        color=None,
        is_kinematic=False,
        density=1000.0,
        physical_material: sapien.physx.PhysxMaterial = None,
        name='',
) -> sapien.Entity:
    """Create a box.

    Args:
        scene: sapien.Scene to create a box.
        pose: 6D pose of the box.
        half_size: [3], half size along x, y, z axes.
        color: [3] or [4], rgb or rgba.
        is_kinematic: whether an object is kinematic (can not be affected by forces).
        density: float, the density of the box.
        physical_material: physical material of the actor.
        name: name of the actor.

    Returns:
        sapien.Entity
    """
    half_size = np.array(half_size)
    builder = scene.create_actor_builder()
    builder.add_box_collision(half_size=half_size, material=physical_material, density=density)  # Add collision shape
    builder.add_box_visual(half_size=half_size, material=color)  # Add visual shape
    if is_kinematic:
        box = builder.build_kinematic(name=name)
    else:
        box = builder.build(name=name)
    box.set_pose(pose)
    return box


def create_sphere(
        scene: sapien.Scene,
        pose: sapien.Pose,
        radius,
        color=None,
        density=1000.0,
        physical_material: sapien.physx.PhysxMaterial = None,
        name='',
) -> sapien.Entity:
    """Create a sphere."""
    builder = scene.create_actor_builder()
    builder.add_sphere_collision(radius=radius, material=physical_material, density=density)
    builder.add_sphere_visual(radius=radius, material=color)
    sphere = builder.build(name=name)
    sphere.set_pose(pose)
    return sphere


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--object', default='box', choices=['box', 'sphere'], type=str, help='the type of object')

    parser.add_argument('--gravity', default=-9.8, type=float, help='z-axis gravity')
    parser.add_argument('--angle', default=30.0, type=float, help='the angle of the slope')
    parser.add_argument('--offset', default=0.1, type=float, help='z-offset of the slope above the ground')

    parser.add_argument('--static-friction', default=0.3, type=float, help='static friction')
    parser.add_argument('--dynamic-friction', default=0.3, type=float, help='dynamic friction')
    parser.add_argument('--restitution', default=0.1, type=float, help='restitution (elasticity of collision)')
    parser.add_argument('--linear-damping', default=0.0, type=float,
                        help='linear damping (resistance proportional to linear velocity)')
    parser.add_argument('--angular-damping', default=0.0, type=float,
                        help='angular damping (resistance proportional to angular velocity)')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    scene_config = sapien.physx.PhysxSceneConfig()
    # The default physical properties can be modified through sapien.SceneConfig
    print(scene_config.gravity)
    scene_config.gravity = np.array([0.0, 0.0, args.gravity])
    sapien.physx.set_scene_config(scene_config)

    # SAPIEN's default physical material for PhysX can be modified at any time
    # It is not bound to a scene
    default_material = sapien.physx.get_default_material()
    print(default_material.static_friction)
    print(default_material.dynamic_friction)
    print(default_material.restitution)
    sapien.physx.set_default_material(
        static_friction=0.3, dynamic_friction=0.3, restitution=0.0)

    # by default, SAPIEN scene consists of PhysxSystem and RenderSystem
    # The PhysxSystem can take a PhysxSceneConfig to custom its behavior
    scene = sapien.Scene([
        sapien.physx.PhysxCpuSystem(),
        sapien.render.RenderSystem(),
    ])
    scene.set_timestep(1 / 100.0)

    # ---------------------------------------------------------------------------- #
    # Sliding/Rolling down the slope
    # ---------------------------------------------------------------------------- #
    physical_material: sapien.physx.PhysxMaterial = sapien.physx.PhysxMaterial(
        static_friction=args.static_friction,
        dynamic_friction=args.dynamic_friction,
        restitution=args.restitution,
    )

    scene.add_ground(altitude=0, material=physical_material)

    # Slope
    half_size = [0.25, 0.5, 0.05]
    z_offset = args.offset
    angle = np.deg2rad(args.angle)
    slope_pose = sapien.Pose(
        p=[0, 0, half_size[1] * np.sin(angle) + half_size[2] * np.cos(angle) + z_offset],
        q=axangle2quat([1.0, 0.0, 0.0], angle),
    )
    slope = create_box(
        scene,
        slope_pose,
        half_size=half_size,
        color=[0.5, 0.5, 0.5],
        name='slope',
        is_kinematic=True,
        physical_material=physical_material
    )

    if args.object == 'box':
        box_half_size = 0.05
        box_pose = sapien.Pose(
            p=[0,
               (half_size[1] - box_half_size) * np.cos(angle) -
                (half_size[2] + box_half_size) * np.sin(angle),
                (half_size[1] - box_half_size) * np.sin(angle) +
                (half_size[2] + box_half_size) * np.cos(angle) + slope_pose.p[2]],
            q=axangle2quat([1.0, 0.0, 0.0], angle),
        )
        actor = create_box(
            scene,
            box_pose,
            half_size=[box_half_size] * 3,
            color=[0., 0., 1.],
            physical_material=physical_material,
            name='box',
        )
    elif args.object == 'sphere':
        # NOTE: Since Sapien does not model rolling resistance (friction), the sphere will roll forever.
        # However, you can set actor's damping, like air resistance.
        radius = 0.05
        sphere_pose = sapien.Pose(
            p=[0,
               (half_size[1] - radius) * np.cos(angle) -
                (half_size[2] + radius) * np.sin(angle),
                (half_size[1] - radius) * np.sin(angle) +
                (half_size[2] + radius) * np.cos(angle) + slope_pose.p[2]],
        )
        actor = create_sphere(
            scene,
            sphere_pose,
            radius=0.05,
            color=[0., 1., 0.],
            physical_material=physical_material,
            name='sphere',
        )
    else:
        raise NotImplementedError()

    rigid_component = actor.find_component_by_type(sapien.physx.PhysxRigidBodyComponent)
    rigid_component.set_linear_damping(args.linear_damping)
    rigid_component.set_angular_damping(args.angular_damping)
    # ---------------------------------------------------------------------------- #


    scene.set_ambient_light([0.5, 0.5, 0.5])
    scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

    viewer = scene.create_viewer()

    viewer.set_camera_xyz(x=-2, y=0, z=2.5)
    viewer.set_camera_rpy(r=0, p=-np.arctan2(2, 2), y=0)
    viewer.window.set_camera_parameters(near=0.05, far=100, fovy=1)

    steps = 0
    pause = True
    while not viewer.closed:
        if viewer.window.key_down('c'):  # press c to start
            pause = False
        if not pause:
            scene.step()
        scene.update_render()
        viewer.render()
        if steps % 10 == 0:
            print('step:', steps)
            print('Pose', actor.get_pose())
            print('Velocity', rigid_component.get_linear_velocity())
            print('Angular velocity', rigid_component.get_angular_velocity())
        steps += 1


if __name__ == '__main__':
    main()
