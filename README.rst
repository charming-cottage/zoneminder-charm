Charmed ZoneMinder
##################

Overview
========

A machine charm for `ZoneMinder`_ ready to run on top of `juju`_.

ZoneMinder is a full-featured, open source, state-of-the-art video
surveillance software system.

Monitor your home, office, or wherever you want. Using off the shelf hardware
with any camera, you can design a system as large or as small as you need.

Checklist
=========

☐ user-defined apache2 port
☐ user-defined ``/etc/zm/conf.d/03-custom.conf``
☐ preserve ``/etc/zm/conf.d/03-custom.conf`` (peer relation data bag)
☐ expose camera stream ports
☐ license
☐ unit tests
☐ publish charm to charmhub

Requirements
============

The charm is meant to be deployed using ``juju>=3.1``.

Usage
=====

The Zoneminder charm is not yet available on charmhub, so can be downloaded
from the github release page or built with `charmcraft`_

.. code-block:: shell

    charmcraft pack

It can be deployed with

.. code-block:: shell

    juju deploy ./zoneminder_ubuntu-22.04-amd64.charm

To access the web interface on port 80, expose the charm:

.. code-block:: shell

    juju expose zoneminder

ZoneMinder will be available at ``<server-ip>/zm``.

Contributing
============

Contributions are encouraged! Please see the `HACKING`_ doc and
`Juju SDK docs`_ for guidelines on enhancements to this charm
following best practice guidelines.

.. _`charmcraft`: https://github.com/canonical/charmcraft
.. _`HACKING`: ./HACKING.rst
.. _`juju`: https://juju.is/
.. _`Juju SDK docs`: https://juju.is/docs/sdk
.. _`ZoneMinder`: https://zoneminder.com/
