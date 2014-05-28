from concepts import Context

c = Context()
#c = Context.fromfile('examples/digits.cxt')
c.additem('cat',['a','b','eats fish'])

#c.additem('cat',['eats fish'])
print c.tostring()
