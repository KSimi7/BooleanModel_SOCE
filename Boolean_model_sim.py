# importing all the essential libraries

import pylab
import os
import boolean2
import pandas as pd
from boolean2 import util

# Creating a path to save plots, results and the parameters

main_folder = "C:\Users\harsi\Desktop\BRAFi_SOCE figures"
path_to_save = main_folder + "\\test_4"
isExist = os.path.exists(path_to_save)

if not isExist:
    os.mkdir(path_to_save)


# function to simulate model

def async_model_sim(model_rules, iterations):
    coll = util.Collector()
    for k in range(1000):
        model = boolean2.Model(model_rules, mode='async')
        model.initialize()
        model.iterate(steps=iterations)

        # takes all nodes
        nodes = model.nodes
        coll.collect(states=model.states, nodes=nodes)

    avgs = coll.get_averages(normalize=True)
    df = pd.DataFrame.from_dict(avgs, orient="index")
    # df.to_csv(path_to_save)

    return (avgs, df, nodes)


def updating_initial_condition(rules, nodes, df, path_to_save, count):
    with open(path_to_save + "\model_rules_" + str(count) + ".txt", 'w') as f:
        f.write(rules)

    with open(path_to_save + "\model_rules_" + str(count) + ".txt", 'r') as f:
        lines = f.readlines()

    for node, i in zip(nodes, range(0, 23)):
        x = df.loc[node, 10]
        # print(x)
        x = int(x)
        n_line = str(node) + ' = ' + str(bool(x)) + '\n'
        lines[i] = n_line
        # # print(lines[i])

    with open(path_to_save + "\model_rules_" + str(count) + ".txt", 'w') as f:
        f.writelines(lines)


def plots_for_simulation(average_states, count, path_to_save):
    ca_levels = [sum(x) for x in zip(average_states['Ca_normal'], average_states['Ca_ER_dump'],
                                     average_states['Ca_SOCE'])]
    ca_levels = [x / 3 for x in ca_levels]

    p1 = pylab.plot(ca_levels, 'sb-', label='Cytoplasmic Ca')  # type: object
    p2 = pylab.plot(average_states['BRAF'], 'vr-', label='BRAF')
    p3 = pylab.plot(average_states['ERK'], 'og-', label='ERK')
    # P4 = pylab.plot(average_states['Ca_channel'], 'vm-', label='Ca_channel')
    # p5 = pylab.plot(average_states['Ca_SOCE'], 'sc-', label='Ca_SOCE')
    # p7 = pylab.plot(average_states['Ca_ER_dump'], 'vk-', label='Ca_ER_dump')
    pylab.legend()
    pylab.ylim((-0.1, 1.1))
    pylab.savefig(path_to_save + '\\'+ count + '.png')
    pylab.close()

count = 7
time = {1:'t_BRAFi_ON',2: 't_BRAFi_ON',3: 't_BRAFi_ON', 4 : 't_Ca_ext_OFF', 5: 't_Ca_er_pumpi_ON', 6: 't_Ca_ext_ON'}
on_dict = {'t_BRAFi_ON': ['BRAFi'], 't_Ca_ext_OFF': [], 't_Ca_er_pumpi_ON': ['Ca_ER_pumpi'], 't_Ca_ext_ON': ['Ca_ext']}
off_dict = {'t_BRAFi_ON': [], 't_Ca_ext_OFF': ['Ca_ext'], 't_Ca_er_pumpi_ON': [], 't_Ca_ext_ON': []}

mean_ERK_state = []
combined_states = {}


for i in range(count):
    with open(path_to_save + "\model_rules_" + str(i) + ".txt", 'r') as f:
        model_rules = f.read()

    if (i < 1):

        on = []
        off = ['BRAFi', 'Ca_ER_pumpi']
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt, iterations=10)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i+1)
        plots_for_simulation(average_states,'normal',path_to_save)
        combined_states = average_states



    elif(1 <=i <=3):
        on = ['BRAFi']
        off = []
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt,iterations=10)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i+1)
        plots_for_simulation(average_states,'BRAFi_ON',path_to_save)
        for key, value in combined_states.iteritems():
            value.extend(average_states[key])

    elif(i == 4):
        if sum(combined_states['ERK'])/len(combined_states['ERK'])<0.3:
            on = ['UK_node']
            off = ['Ca_ext']
        else:
            on = []
            off = ['UK_node','Ca_ext']
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt, iterations=10)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i + 1)
        plots_for_simulation(average_states,'Ca_ext_off',path_to_save)
        for key, value in combined_states.iteritems():
            value.extend(average_states[key])

    elif(i == 5):
        on = ['Ca_ER_pumpi ']
        off = []
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt,iterations=10)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i+1)
        plots_for_simulation(average_states,'Ca_ER_pumpi_on',path_to_save)
        for key, value in combined_states.iteritems():
            value.extend(average_states[key])

    else:
        on = ['Ca_ext']
        off = []
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt, iterations=10)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i + 1)
        plots_for_simulation(average_states,'Ca_Ext_on',path_to_save)
        for key, value in combined_states.iteritems():
            value.extend(average_states[key])

# for i in range(count):
#
#     with open(path_to_save + "\model_rules_" + str(i) + ".txt", 'r') as f:
#         model_rules = f.read()

#     if i in time:
#         ERK_state = sum(mean_ERK_state)/len(mean_ERK_state)
#         on = []
#         off = []
#         if (ERK_state<0.5):
#             on = on_dict[time[i]]
#             on.append('UK_node')
#
#             if off_dict[time[i]] == None:
#                 off = []
#             else:
#                 off = off_dict[time[i]]
#             print(time[i])
#             print(ERK_state)
#             print(on)
#             print(off)
#             new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff= off)
#             average_states, df, nodes = async_model_sim(new_txt, iterations=10)
#             updating_initial_condition(model_rules, nodes, df, path_to_save, count=i + 1)
#             plots_for_simulation(average_states, time[i], path_to_save)
#             mean_ERK_state.append(sum(average_states['ERK']) / len(average_states['ERK']))
#             for key, value in combined_states.iteritems():
#                 value.extend(average_states[key])
#
#         elif (ERK_state>0.5):
#             if off_dict[time[i]] == None:
#                 nodes_off = []
#             else:
#                 nodes_off = off_dict[time[i]]
#             nodes_off.append('UK_node')
#             on = on_dict[time[i]]
#             off = nodes_off
#             print(time[i])
#             print(ERK_state)
#             print(on)
#             print(off)
#             new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
#             average_states, df, nodes = async_model_sim(new_txt, iterations=10)
#             updating_initial_condition(model_rules, nodes, df, path_to_save, count=i + 1)
#             plots_for_simulation(average_states, time[i], path_to_save)
#             mean_ERK_state.append(sum(average_states['ERK']) / len(average_states['ERK']))
#             for key, value in combined_states.iteritems():
#                 value.extend(average_states[key])
#
#     else:
#         on = []
#         off = ['BRAFi', 'Ca_ER_pumpi ']
#         new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
#         # df.to_csv(path_to_save)
#         average_states, df, nodes = async_model_sim(new_txt, iterations=10)
#         updating_initial_condition(model_rules, nodes, df, path_to_save, count=i+1)
#         plots_for_simulation(average_states,'normal',path_to_save)
#         mean_ERK_state.append(sum(average_states['ERK']) / len(average_states['ERK']))
#         combined_states = average_states
#
plots_for_simulation(combined_states, "combined", path_to_save)