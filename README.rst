hrmpy
=====

This is an (incomplete, currently) implementation of the assembler from
`Tomorrow Corporation`_'s excellent game `Human Resource Machine`_.

.. _Tomorrow Corporation: http://tomorrowcorporation.com/
.. _Human Resource Machine: http://tomorrowcorporation.com/humanresourcemachine


Why?
----

Why not?

Mostly, I've been looking for something to implement in RPython, and this
seemed like a reasonable option.


How?
----

You can run a program with the untranslated interpreter::

  $ python -m hrmpy progs/04-scrambler-handler.hrm inputs/jot10.txt

You can translate::

  $ /path/to/rpython/bin/rpython targethrmpy.py

And then run the translated version::

  $ ./hrmpy-c progs/04-scrambler-handler.hrm inputs/jot10.txt


Tests?
------

There are (not enought) tests. Run them like so::

  $ pip install -r requirements-dev.txt  # To install pytest and friends
  $ py.test
