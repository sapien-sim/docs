.. _contact:

Contact
==================

.. highlight:: python

Contact information is useful to check whether two rigid bodies collide or whether an object is grasped by a gripper.
The example shows how to check the contact between two rigid objects (one box supported by another box).

In this tutorial, you will learn the following:

* Get contact information from ``PhysxContact``

The full script is included as follows:

.. literalinclude:: scripts/contact.py
    :linenos:

You can call ``get_contacts`` to fetch all contacts after the current simulation step.
It returns a list of ``PhysxContact``.
``contact.components[0]`` and ``contact.components[1]`` refer to two PhysX rigid components involved in the contact.
``contact.shapes[0]`` and ``contact.shapes[1]`` refer to two PhysX collision shapes involved in the contact.
``contact.points`` contains a list of ``PhysxContactPoint``.

For each contact point, 

* ``impulse``: the impulse applied on the first actor.
* ``normal``: the direction of impulse.
* ``position``: the point of application in the world frame.
* ``separation``: distance between the two shapes involved in the contact (can be negative).

.. note::
   ``PhysxContact`` in SAPIEN does not mean that two actors are touching each
   other. A contact will be generated when the distance between two actors are
   smaller than a given contact offset, which can be changed in
   ``PhysxSceneConfig`` before creating the scene. To check for touching and
   penetration, one should check the impulse of a contact point.
