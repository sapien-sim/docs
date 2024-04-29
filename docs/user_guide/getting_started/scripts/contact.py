"""A simple example for contact."""

import sapien
import numpy as np


def main():
    scene = sapien.Scene()
    dt = 1 / 100.0
    scene.set_timestep(dt)

    # ---------------------------------------------------------------------------- #
    # Add two boxes
    # ---------------------------------------------------------------------------- #
    actor_builder = scene.create_actor_builder()
    actor_builder.add_box_collision(half_size=[0.5, 0.5, 0.5])
    # actor_builder.add_box_visual(half_size=[0.5, 0.5, 0.5], color=[1, 0, 0])
    box1 = actor_builder.build_kinematic(name="box1")
    box1.set_pose(sapien.Pose(p=[0, 0, 1.0]))
    print(
        "Mass of box1:",
        box1.find_component_by_type(sapien.physx.PhysxRigidDynamicComponent).mass,
    )

    actor_builder = scene.create_actor_builder()
    actor_builder.add_box_collision(half_size=[0.25, 0.25, 0.25])
    # actor_builder.add_box_visual(half_size=[0.25, 0.25, 0.25], color=[0, 1, 0])
    box2 = actor_builder.build(name="box2")
    box2.set_pose(sapien.Pose(p=[0, 0, 1.75]))
    print(
        "Mass of box1:",
        box2.find_component_by_type(sapien.physx.PhysxRigidDynamicComponent).mass,
    )

    # step a few times to settle the scene
    for _ in range(10):
        scene.step()

    # ---------------------------------------------------------------------------- #
    # Check contacts
    # ---------------------------------------------------------------------------- #

    contacts = scene.get_contacts()
    support_force = 0
    for contact in contacts:
        print(contact)
        for point in contact.points:
            print("Impulse (F * dt) on the first actor:", point.impulse)
            print("Normal (same direction as impulse):", point.normal)
            print("Contact position (in the world frame):", point.position)
            print("Minimum distance between two shapes:", point.separation)
            if contact.bodies[0].entity.name == "box2":
                support_force += point.impulse[2] / dt
            elif contact.bodies[0].entity.name == "box1":
                support_force -= point.impulse[2] / dt
            else:
                raise RuntimeError("Impossible case in this example.")
    # Sanity check: the support force should balance the gravity
    np.testing.assert_allclose(
        support_force,
        9.81
        * box2.find_component_by_type(sapien.physx.PhysxRigidDynamicComponent).mass,
        rtol=1e-3,
    )


if __name__ == "__main__":
    main()
