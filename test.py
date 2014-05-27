from concepts import Context

c = Context()
c = Context.fromfile('examples/digits.cxt')
c.additem('cat',['a','b','fish'])

#c.additem('cat',['eats fish'])
print c.tostring()
