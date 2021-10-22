import pylab
import fileinput
import os
import boolean2
import pandas as pd
from boolean2 import Model
from boolean2 import util

main_folder = "C:\Users\harsi\Desktop\BRAFi_SOCE figures\Simulation_2"
path_to_save = main_folder + "\long_term_BRAFi_Pump_off"
isExist = os.path.exists(path_to_save)
if not isExist:
    os.mkdir(path_to_save)


# if mode is sync uncomment this part

# model = Model(text=text, mode='sync')
# model.initialize()
# model.iterate(steps=10)
#
# # for node in model.data:
# #     print(node, model.data[node])
#
# p1 = pylab.plot(model.data["Ca_cyt"], 'sb-', label='Ca_cyt')
# p2 = pylab.plot(model.data["ERK"], 'vr-', label='ERK')
# p3 = pylab.plot(model.data["BRAFi"], 'og-', label='BRAFi')
# pylab.legend()
# pylab.ylim((-0.1, 1.1))
# pylab.show()

# if mode is async uncomment this part

coll = util.Collector()
for i in range(1000):
    model = boolean2.Model('my_model_rules.txt', mode='async')
    model.initialize()
    model.iterate(steps=10)

    # takes all nodes
    nodes = model.nodes
    coll.collect(states=model.states, nodes=nodes)

avgs = coll.get_averages(normalize=True)
df = pd.DataFrame.from_dict(avgs, orient="index")

with open("my_model_rules.txt") as f:
    lines = f.readlines()


for nodes,i in zip(model.nodes,range(0,10)):
    x = df.loc[nodes][10]
    x = int(x)
    n_line = str(nodes) + ' = ' + str(bool(x)) +'\n'
    lines[i] = n_line
    print(lines[i])

with open("my_model_rules.txt",'w') as f:
    f.writelines(lines)

# df.to_csv(path_to_save + "\simulations.csv")

ca_levels = [sum(x) for x in zip(avgs['Ca_cyt_normal'], avgs['Ca_cyt_high'])]
ca_levels = [x / 2 for x in ca_levels]

p1 = pylab.plot(ca_levels, 'sb-', label='Cytoplasmic Ca')  # type: object
p2 = pylab.plot(avgs['BRAF'], 'vr-', label='BRAF')
p3 = pylab.plot(avgs['ERK'], 'og-', label='ERK')
p4 = pylab.plot(avgs['Gen_exp'], 'sc-', label='gene exp')
p5 = pylab.plot(avgs['Ca_cyt_high'], 'sy-', label='Ca_cyt_high')
p6 = pylab.plot(avgs['Ca_cyt_normal'], 'v-', label='Ca_cyt_normal')
p7 = pylab.plot(avgs['Ca_channel'], 'v-', label='Ca_channel')
pylab.legend()
pylab.ylim((-0.1, 1.1))
pylab.savefig(path_to_save + '/long_term_BRAFi_Pump_off_3.png')

# write a function to save the figures
# text_file = open(path_to_save + '/Param.txt', 'w')
# n = text_file.write(text)
# text_file.close()
