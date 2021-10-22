# importing the packages
import pylab   # to plot
import os      # to direct path
import boolean2   # to perform boolean simulations
import pandas as pd  # for dataframes to store data
from boolean2 import util # to collect the data from async simulatioms

# Defining the path to the folder to save plots and data

main_folder = "C:\Users\harsi\Desktop\BRAFi_SOCE figures\Simulation_2"
path_to_save = main_folder + "\long_term_BRAFi_Pump_off"

# if the path does not exist this code will generate a folder
isExist = os.path.exists(path_to_save)
if not isExist:
    os.mkdir(path_to_save)

# text for initial condition of each node and the interaction between
# node in the model.

text = """
BRAFi = True
BRAF = False
MEK = False
ERK = False
UK_node = False
Ca_normal = True
Ca_ER_dump = False
Ca_SOCE = False
Ca_channel = False
Ca_ext = True
Ca_ER = True
Ca_ER_pump = True
Ca_ER_pumpi = False

BRAF* = not BRAFi
MEK* = BRAF or Ca_SOCE
ERK* = MEK
UK_node* = not ERK
Ca_channel* = UK_node
Ca_ER_dump* = Ca_ER_pumpi
Ca_SOCE* = not Ca_ER and (Ca_channel and Ca_ext)
Ca_ER* = Ca_normal and Ca_ER_pump
Ca_ER_pump* = Ca_ER_pumpi

"""

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
# on = []
# off = ['BRAFi', 'Ca_er_pumpi ']
# new_txt = boolean2.modify_states(text, turnon=on, turnoff=off)
# print(new_txt)


# boolean simulation

coll = util.Collector()
for i in range(1000):
    model = boolean2.Model(text, mode='async')
    model.initialize()
    model.iterate(steps=10)

    # takes all nodes
    nodes = model.nodes
    coll.collect(states=model.states, nodes=nodes)

# Taking average of the states for 1000 runs

avgs = coll.get_averages(normalize=True)
# df = pd.DataFrame.from_dict(avgs, orient="index")
# df.to_csv(path_to_save + "\simulations.csv")

# Taking average of the three main Ca_nodes in the model to determine cytoplasmic Ca state

ca_levels = [sum(x) for x in zip(avgs['Ca_normal'], avgs['Ca_ER_dump'],
                                 avgs['Ca_SOCE'])]
ca_levels = [x / 3 for x in ca_levels]


# plotting the output

p1 = pylab.plot(ca_levels, 'sb-', label='Cytoplasmic Ca')  # type: object
p2 = pylab.plot(avgs['BRAF'], 'vr-', label='BRAF')
p3 = pylab.plot(avgs['ERK'], 'og-', label='ERK')
# p4 = pylab.plot(avgs['Gen_exp'], 'sc-', label='gene exp')
# p5 = pylab.plot(avgs['Ca_cyt_high'], 'sy-', label='Ca_cyt_high')
# p6 = pylab.plot(avgs['Ca_cyt_normal'], 'v-', label='Ca_cyt_normal')
# p7 = pylab.plot(avgs['Ca_channel'], 'v-', label='Ca_channel')
pylab.legend()
pylab.ylim((-0.1, 1.1))
pylab.show()
# pylab.savefig(path_to_save + '/long_term_BRAFi_Pump_off_3.png')

# write a function to save the figures
# text_file = open(path_to_save + '/Param.txt', 'w')
# n = text_file.write(text)
# text_file.close()
