=========
HydeyHole
=========

.. image:: resources/logos/hydeyhole-192.png


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

This will do several things:

* create a virtualenv

* download and install deps into that env

* start a HydeyHole server running on the configured port

* ssh into it using a custom twistd command

You may, of course, do all these things by hand if you so desire!

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

The "help" text that you get upon login is the best first hint. You can get a
list of available functions, modules, etc., by executing the following:

.. code:: lisp

  :> (ls)

If you'd like to see the available objects listed in module order, you can
do this:

.. code:: lisp

  :> (ls "module")

Otherwise, you may do anything here that you do in Hy:

.. code:: lisp

  :> (+ 1 2 3 4 5 6)
  21
  :> (setv l [1 2 3 4 5 6])
  :> (sum l)
  21
  :> (car l)
  1
  :> (cdr l)
  [2, 3, 4, 5, 6]
  :> (get l 4)
  5
  :>

For more information on Hy, be sure to `read the docs`_!


Adding Functionality
====================

If you would like to add new commands to HydeyHole, you'll want to spend some
time in ``hydeyhole.app.shell.command``. We recommend adding a new ``*API``
class for a new group of commands. This will allow users to sort the new
commands with the ``(ls "module")`` call in the shell.

If you would like your new ``*API`` methods to be available to uses when the
log in to HydeyHole, you will want to decorate them with ``@commands.add``.
Again, spending some time looking at the API classes in the ``command`` module
will show you what you need to do.


.. Links
.. -----
.. _read the docs: http://docs.hylang.org/en/latest/
