=========
HydeyHole
=========

.. image:: resources/logos/hydeyhole.png


Dependencies
------------

For the list of dependencies, see ``requirements.txt``.

These are automatically installed when you run most of the ``make`` targets.
See below for more details.


Getting Started
---------------

To run HydeyHole, first you need to generate SSH keys for the Twisted SSH
server:

.. code:: bash

  $ make keys

Once that is completed, you can do is this to start the daemon and log in:

.. code:: bash

  $ make shell

This will start a HydeyHole server running on the configured port, and then
ssh into it using a custom command. You may, of course, do all these things
by hand if you so desire!

If you do wish to run things manually, keep in mind that the ``make`` targets
use a ``virtualenv`` and it will be easiest if you do too.

Once you are logged in to HydeyHole, you will see something like this:

.. code:: text

  :>
  :
  : Welcome to
  :  _         _         _       _
  : | |_ _ _ _| |___ _ _| |_ ___| |___
  : |   | | | . | -_| | |   | . | | -_|
  : |_|_|_  |___|___|_  |_|_|___|_|___|
  :     |___|       |___|
  :
  : You have logged into a HydeyHole Shell Server.
  :
  : You have logged onto a HydeyHole Server; you are currently at a Hy
  : command prompt. Hy is a Lisp dialect of Python of which you can
  : learn more about here:
  :   https://github.com/hylang/hy
  :
  :
  : Type '(ls)' or '(dir)' to see the objects in the current namespace.
  : Use (help ...) to get API docs for available objects.
  :
  : Enjoy!
  :
  :>

Using Hy in HydeyHole
=====================

TBD

Adding Functionality
====================

TBD




.. Links
.. -----