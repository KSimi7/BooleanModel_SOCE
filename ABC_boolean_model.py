import pylab
import boolean2
from boolean2 import Model
from boolean2 import ruleparser
from boolean2 import util
import numpy as np

text = """
A = True
B = False
C = True

1: A* = B or C
1: B* = not A and C
2: C* = A and not C
"""

# if mode is sync uncomment this part

on = ['B']
off = []
new_text = boolean2.modify_states(text, turnon=on, turnoff=off)
print(new_text)

# model = Model(text=new_text, mode='time')
# model.initialize()
# model.iterate(steps=20)
#
# for node in model.data:
#     print(node, model.data[node])
#
# p1 = pylab.plot(model.data["A"], 'sb-', label='A')
# p2 = pylab.plot(model.data["B"], 'vr-', label='B')
# p3 = pylab.plot(model.data["C"], 'og-', label='C')
# pylab.legend()
# pylab.ylim((-0.1, 1.1))
# pylab.show()

# if mode is async uncomment this part

coll = util.Collector()
for i in range(10):
    model = boolean2.Model(new_text, mode='async')
    model.initialize()
    model.iterate(steps=10)

    # takes all nodes
    # for some reason model.nodes() is not working
    nodes = model.nodes
    print(model.data)
    coll.collect(states=model.states, nodes=nodes)

avgs = coll.get_averages(normalize=True)


p1 = pylab.plot(avgs['A'], 'sb-', label='A')
p2 = pylab.plot(avgs['B'], 'vr-', label='B')
p3 = pylab.plot(avgs['C'], 'og-', label='C')
pylab.legend()
pylab.ylim((-0.1, 1.1))
pylab.show()
