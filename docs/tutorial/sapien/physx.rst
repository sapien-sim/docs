.. _physx:

PhysX Components
==================================

This section discusses how to build and access rigid and articulated objects
simulated with the PhysX simulator. To make the building process of a rigid or
articulated object simpler, SAPIEN provides builder classes :ref:`actor_builder`
and :ref:`articulation_builder` wrapped around the low-level component API.

Rigid Body Hierarchy
----------------------------------

There are 3 types of rigid components in SAPIEN ``PhysxRigidStaticComponent``,
``PhysxRigidDynamicComponent``, and ``PhysxArticulationLinkComponent``.

All 3 types components shared the same base class ``PhysxRigidBaseComponent``
which implements the ``attach`` function that allows attaching collision shapes
of type ``PhysxCollisionShape``.

``PhysxRigidDynamicComponent`` and ``PhysxArticulationLinkComponent`` are both
affected by forces, and they share the ``PhysxRigidBodyComponent`` base class,
which provides functions related to mass properties, external forces, velocity,
damping, etc.

The class hierarchy is summarized in the figure below.

.. figure:: assets/rigid_hierarchy.svg
    :align: center
    :figclass: align-center

Rigid Static Component
----------------------------------

``PhysxRigidStaticComponent`` represents a static object that never moves.
Setting pose of a static component is expensive and should be avoided.

Rigid body Component
----------------------------------
``PhysxRigidBodyComponent`` represents bodies affected by forces.


Rigid Dynamic Component
----------------------------------

Articulation Link Component
----------------------------------

Collision Shape
----------------------------------

Collision shapes can be attached to any ``PhysxRigidBaseComponent``. There are 7
types of collision shapes.

- ``PhysxCollisionShapePlane`` is an infinite plane, which is typically used as
  the ground. This shape can only be used with static or kinematic objects.
- ``PhysxCollisionShapeBox`` represents a box, characterized by ``half_size``.
- ``PhysxCollisionShapeSphere`` represents a sphere characterized by ``radius``.
- ``PhysxCollisionShapeCapsule`` represents a capsule characterized by
  ``radius`` and ``half_length``.
- ``PhysxCollisionShapeCylinder`` represents a cylinder characterized by
  ``radius`` and ``half_length``
- ``PhysxCollisionShapeConvexMesh`` represents a convex mesh.
- ``PhysxCollisionShapeTriangleMesh`` represents any triangle mesh. However, it
  may only be used for static or kinematic objects.


Joint Component
----------------------------------

Drive Component
----------------------------------

Gear Component
----------------------------------
