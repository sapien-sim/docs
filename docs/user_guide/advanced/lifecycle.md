# Component Lifecycle

A `Component` is the smallest functional unit in SAPIEN. The behavior of a
component is determined by 2 lifecycle functions `on_add_to_scene()` and
`on_remove_from_scene()`

## on_add_to_scene

`on_add_to_scene()` is called once immediately after the component is added to a
scene. Specifically, it is called when the following 3 conditions all become
true `component.enabled`, `component.entity is not None`,
`component.entity.scene is not None`. For example, adding an entity with the
component to a scene, adding the component to an entity in a scene, or enabling
the component on an entity in a scene. 

The implementation of this function should register itself to a suitable system
of the scene.

## on_remove_from_scene

`on_remove_from_scene()` is called immediately after the condition above are no
longer all true. For example, disabling a component, or removing the parent
entity of the component from the scene.

The implementation of this function should unregister itself from the system.

