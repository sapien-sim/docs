.. _entity:

Scene, Entity, and Component
==================================

Scene
-----------

Everything simulated or rendered needs to live in a 3D world. SAPIEN calls this
world ``Scene``. A scene is simply constructed with ``sapien.Scene()``. A scene
does 2 things: holding a list of ``Entity`` and managing a list of ``System``.

Entity
-----------

Every object in the SAPIEN scene is an ``Entity``, from robot links, tables, to
lights and cameras. The specific functionalities of an ``Entity`` is specified
with its attached components.

Formally, an ``Entity`` in SAPIEN has a 6-D ``Pose``, i.e. position and
orientation, and a list of attached components. To give an entity specific
functionalities, you need to attach components to it through ``entity.add_component(component)``

A ``PhysxRigidDynamicComponent`` makes the entity a rigid body that interacts
with PhysX physical simulation. A ``RenderbodyComponent`` assigns the entity a
visual appearance so it can be rendered by a camera, which is another entity
with a ``RenderCameraComponent`` attached.

Component
-----------

The ``Component`` is the fundamental concept that gives SAPIEN entities their
functionalities. Each component may have very different purposes, but they all
implement 2 functions ``add_to_scene`` and ``remove_from_scene``.

Let's take a look at ``PhysxRigidDynamicComponent`` as an example. When an
entity with this component is added to scene. The ``add_to_scene`` function is
called. Which first queries the scene for a ``PhysxSystem``, which contains a
simulation scene from PhysX. Then the ``PhysxRigidDynamicComponent`` registers
itself into the ``PhysxSystem``, which adds a PhysX rigid dynamic actor into the
simulation scene. In the future, when the step function of the ``PhysxSystem``
is called, ``PhysxSystem`` synchronizes the updated poses to the
``PhysxRigidDynamicComponent``, which updates the pose of the sapien ``Entity``.

Components on an entity can be obtained by ``entity.components`` or
``entity.find_component_by_type``. For example, to retrieve a component of type
``PhysxRigidDynamicComponent``, you could use

.. code-block:: python

   entity.find_component_by_type(sapien.physx.PhysxRigidDynamicComponent)

System
-----------

As we can see from the example in the component section. A ``System`` can
perform actions over a set of specific components. For example, ``PhysxSystem``
can update PhysX-related components, and ``RenderSystem`` manages render bodies
and cameras to perform rendering.

.. note::

   While SAPIEN features ``Entity``, ``Component``, and ``System``. SAPIEN is
   not an `ECS (Entity component system)
   <https://en.wikipedia.org/wiki/Entity_component_system>`_ architecture but
   simply borrows the concepts from ECS, similar to the Unity game engine.
