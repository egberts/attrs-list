# attrs-list
Making python-attrs work with list type during serialization, particularly with deep nesting of classes.

I had multiple attrs-defined classes and the list-type were not being 'print'ed
and treated as 'ignored'.

Needed to be able to traverse all the attrs-defined classes during a simple
print statement.

This snippet of code shows how to do this that should require no-attrs-class
dependency.

Also, it works well for JSON-print.
