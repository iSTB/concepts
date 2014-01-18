Concepts
========

|PyPI version| |License| |Downloads|

Concepts is a simple Python implementation of **Formal Concept Analysis** (FCA).

FCA provides a mathematical model for describing a set of **objects** (e.g. King
Arthur, Sir Robin, and the holy grail) with a set of **properties** or features
(e.g. human, knight, king, and mysterious) which each of the objects either
has or not. A table called *formal context* defines which objects have a given
property and vice versa which properties a given object has.


Installation
------------

.. code:: bash

    $ pip install concepts


Formal contexts
---------------

With Concepts, context objects can be created from a string with an ascii-art
style table. The objects and properties will simply be represented by strings.
Separate the property columns with *pipe* symbols, create one row for each objects
and indicate the presence of a property with the character *X*. Note that the
object and property names need to be disjoint to uniquely identify them.

.. code:: python

    >>> from concepts import Context

    >>> c = Context.from_string('''
    ...            |human|knight|king |mysterious|
    ... King Arthur|  X  |  X   |  X  |          |
    ... Sir Robin  |  X  |  X   |     |          |
    ... holy grail |     |      |     |     X    |
    ... ''')

    >>> c  # doctest: +ELLIPSIS
    <Context object mapping 3 objects to 4 properties at 0x...>

After creation, the parsed content of the table is available on the **context object**.

.. code:: python

    >>> c.objects  # row headings
    ('King Arthur', 'Sir Robin', 'holy grail')

    >>> c.properties  # column headings
    ('human', 'knight', 'king', 'mysterious')

    >>> c.bools  # data cells
    [(True, True, True, False), (True, True, False, False), (False, False, False, True)]


The context object can be queried to return the **common properties** for a
collection of objects (common *intent*, ``intension``) as well as the
**common objects** for a collection of properties (common *extent*, 
``extension``):

.. code:: python

    >>> c.intension(['King Arthur', 'Sir Robin'])  # common properties?
    ('human', 'knight')

    >>> c.extension(['knight', 'mysterious'])  # objects with these properties?
    ()

In FCA these operations are called *derivations* and usually notated with the
*prime* symbol(').

.. code:: python

    >>> c.extension(['knight', 'king'])
    ('King Arthur',)

    >>> c.extension(['mysterious', 'human'])
    ()


Formal concepts
---------------

A pair of objects and properties such that the objects share exactly the
properties and the properties apply to exactly the objects is called *formal
concept*. Informally, they result from maximal rectangles of *X*-marks in the
context table, when rows and columns can be reordered freely.

You can retrieve the **closest matching concept** corresponding to a collection
of objects or properties with the ``__getitem__`` method of the concept object:

.. code:: python

    >>> c[('king',)]  # closest concept matching intent/extent
    (('King Arthur',), ('human', 'knight', 'king'))

    >>> assert c.intension(('King Arthur',)) == ('human', 'knight', 'king')
    >>> assert c.extension(('human', 'knight', 'king')) == ('King Arthur',)

    >>> c[('King Arthur', 'Sir Robin')]
    (('King Arthur', 'Sir Robin'), ('human', 'knight'))

Within each context, there is a **maximally general concept** comprising all
of the objects as extent and having an empty intent (*supremum*).

.. code:: python

    >>> c[('Sir Robin', 'holy grail')]  # maximal concept, supremum
    (('King Arthur', 'Sir Robin', 'holy grail'), ())


Furthermore there is a **minimally general concept** comprising no object at all
and having all properties as intent (*infimum*).

.. code:: python

    >>> c[('mysterious', 'knight')]  # minimal concept, infimum
    ((), ('human', 'knight', 'king', 'mysterious'))

The concepts of a context can be ordered by extent set-inclusion (or dually 
intent set-inclusion). With this (partial) order, they form a *concept lattice*
having the **supremum** concept (i.e. the tautology) at the top, the **infimum** concept
(i.e. the contradiction) at the bottom, and the other concepts in between.


Concept lattice
---------------

The concept ``lattice`` of a context contains **all pairs of objects and properties**
(*formal concepts*) that can be retrieved from a formal context:

.. code:: python

    >>> c  # doctest: +ELLIPSIS
    <Context object mapping 3 objects to 4 properties at 0x...>
    
    >>> l = c.lattice

    >>> l  # doctest: +ELLIPSIS
    <Lattice object of 2 atoms 5 concepts 2 coatoms at 0x...>

    >>> for extent, intent in l:
    ...     print extent, intent
    () ('human', 'knight', 'king', 'mysterious')
    ('King Arthur',) ('human', 'knight', 'king')
    ('holy grail',) ('mysterious',)
    ('King Arthur', 'Sir Robin') ('human', 'knight')
    ('King Arthur', 'Sir Robin', 'holy grail') ()

Individual concepts can be retrieved by different means :

.. code:: python

    >>> l.infimum  # first concept, index 0
    <Infimum {} <-> [human knight king mysterious]>

    >>> l.supremum  # last concept
    <Supremum {King Arthur, Sir Robin, holy grail} <-> []>

    >>> l[1]
    <Atom {King Arthur} <-> [human knight king] <=> King Arthur <=> king>

    >>> l[('mysterious',)]
    <Atom {holy grail} <-> [mysterious] <=> holy grail <=> mysterious>


The concepts form a **directed acyclic graph** and are linked upward (more general
concepts, superconcepts) and downward (less general concepts, subconcepts):

.. code:: python

    >>> l.infimum.upper_neighbors
    (<Atom {King Arthur} <-> [human knight king] <=> King Arthur <=> king>, <Atom {holy grail} <-> [mysterious] <=> holy grail <=> mysterious>)

    >>> l[1].lower_neighbors
    (<Infimum {} <-> [human knight king mysterious]>,)


Visualization
-------------

To visualize the lattice, use its ``graphviz`` method:

.. code:: python

    >>> dot = l.graphviz()

    >>> print dot.source  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    // <Lattice object of 2 atoms 5 concepts 2 coatoms at 0x...>
    digraph Lattice {
    node [width=.25 style=filled shape=circle label=""]
    edge [labeldistance=1.5 dir=none minlen=2]
    	c0
    	c1
    		c1 -> c1 [color=transparent headlabel="King Arthur" labelangle=270]
    		c1 -> c1 [color=transparent taillabel=king labelangle=90]
    		c1 -> c0
    	c2
    		c2 -> c2 [color=transparent headlabel="holy grail" labelangle=270]
    		c2 -> c2 [color=transparent taillabel=mysterious labelangle=90]
    		c2 -> c0
    	c3
    		c3 -> c3 [color=transparent headlabel="Sir Robin" labelangle=270]
    		c3 -> c3 [color=transparent taillabel="human knight" labelangle=90]
    		c3 -> c1
    	c4
    		c4 -> c2
    		c4 -> c3
    }

.. image:: https://raw.github.com/xflr6/concepts/master/docs/holy-grail.png


For example:

.. code:: python

    >>> w = Context.from_file('examples/liveinwater.cxt')
    >>> dot = w.lattice.graphviz()
    >>> print dot.source  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    // <Lattice object of 4 atoms 19 concepts 4 coatoms at 0x...>
    digraph Lattice {
    node [width=.25 style=filled shape=circle label=""]
    edge [labeldistance=1.5 dir=none minlen=2]
    	c0
    	c1
    		c1 -> c1 [color=transparent headlabel=frog labelangle=270]
    		c1 -> c0
    	c2
    		c2 -> c2 [color=transparent headlabel=dog labelangle=270]
    		c2 -> c2 [color=transparent taillabel="breast feeds" labelangle=90]
    		c2 -> c0
    	c3
    		c3 -> c3 [color=transparent headlabel=reed labelangle=270]
    		c3 -> c0
    ...

.. image:: https://raw.github.com/xflr6/concepts/master/docs/liveinwater.png


Persistence
-----------

Contexts can be loaded from and saved to files in cxt and table format:

.. code:: python

    >>> c1 = Context.from_file('examples/liveinwater.cxt')
    >>> c1  # doctest: +ELLIPSIS
    <Context object mapping 8 objects to 9 properties at 0x...>

    >>> c2 = Context.from_file('examples/liveinwater.txt', frmat='table')
    >>> c2  # doctest: +ELLIPSIS
    <Context object mapping 8 objects to 9 properties at 0x...>

    >>> c1 == c2
    True


Context objects are picklable:

.. code:: python

    >>> import pickle

    >>> pickle.loads(pickle.dumps(c)) == c
    True


Further reading
---------------

- http://en.wikipedia.org/wiki/Formal_concept_analysis
- http://www.upriss.org.uk/fca/

The generation of the concept lattice is based on the algorithm from
C. Lindig. Fast Concept Analysis. In Gerhard Stumme, editors, Working
with Conceptual Structures - Contributions to ICCS 2000, Shaker Verlag,
Aachen, Germany, 2000.

- http://www.st.cs.uni-saarland.de/~lindig/papers/lindig-fca-2000.pdf

The included example cxt files are taken from `Uta Priss' FCA homepage
<http://www.upriss.org.uk/fca/examples.html>`_


License
-------

Concepts is distributed under the `MIT license
<http://opensource.org/licenses/MIT>`_.

.. |PyPI version| image:: https://pypip.in/v/concepts/badge.png
    :target: https://pypi.python.org/pypi/concepts
    :alt: Latest PyPI Version
.. |License| image:: https://pypip.in/license/concepts/badge.png
    :target: https://pypi.python.org/pypi/concepts
    :alt: License
.. |Downloads| image:: https://pypip.in/d/concepts/badge.png
    :target: https://pypi.python.org/pypi/concepts
    :alt: Downloads