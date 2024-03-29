# importing all the essential libraries

import pylab
import os
import boolean2
import pandas as pd
from boolean2 import util

# Creating a path to save plots, results and the parameters

main_folder = "C:\Users\harsi\Desktop\BRAFi_SOCE figures"
path_to_save = main_folder + "\\Network_3"
isExist = os.path.exists(path_to_save)

if not isExist:
    os.mkdir(path_to_save)


# function to simulate model

def async_model_sim(model_rules, iterations):
    coll = util.Collector()
    for i in range(1000):
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
    ca_levels = [sum(x) for x in zip(average_states['Ca_cyt_normal'], average_states['Ca_ER_dump'],
                                     average_states['Ca_SOCE'])]
    ca_levels = [x / 3 for x in ca_levels]

    p1 = pylab.plot(ca_levels, 'sb-', label='Cytoplasmic Ca')  # type: object
    p2 = pylab.plot(average_states['BRAF'], 'vr-', label='BRAF')
    p3 = pylab.plot(average_states['ERK'], 'og-', label='ERK')
    p4 = pylab.plot(average_states['MEK'], 'vc-', label='MEK')
    p5 = pylab.plot(average_states['UK_node'], 'sy-', label='UK_node')
    pylab.legend()
    pylab.ylim((-0.1, 1.1))
    pylab.savefig(path_to_save + '/short_fig_' + str(count) + '.png')
    pylab.close()

def plots_for_simulation_delay(average_states, count, path_to_save):
    ca_levels = [sum(x) for x in zip(average_states['Ca_cyt_1'], average_states['Ca_cyt_2'])]
    ca_levels = [x / 2 for x in ca_levels]

    p1 = pylab.plot(average_states['ERK'], 'sb-', label='ERK')  # type: object
    # p2 = pylab.plot(average_states['delay1'], 'vr-', label='delay1')
    # p3 = pylab.plot(average_states['delay8'], 'og-', label='delay8')
    # p4 = pylab.plot(average_states['delay6'], 'vc-', label='delay6')
    # p5 = pylab.plot(average_states['delay7'], 'sy-', label='delay7')
    p6 = pylab.plot(average_states['delay5'], 'sm-', label='delay5')
    p7 = pylab.plot(average_states['Gen_exp'], 'vk-', label='gene exp')
    # p8 = pylab.plot(average_states['delay7'], 'sy-', label='delay7')
    # p9 = pylab.plot(average_states['delay8'], 'sy-', label='delay8')
    # p9 = pylab.plot(average_states['delay8'], 'sy-', label='delay8')
    pylab.legend()
    pylab.ylim((-0.1, 1.1))
    pylab.savefig(path_to_save + '/short__delay_fig_' + str(count) + '.png')
    pylab.close()



count = range(5)
treatment = 'short'
combined_states = {}
for i in count:
    with open(path_to_save + "\model_rules_" + str(i) + ".txt", 'r') as f:
        model_rules = f.read()

    if (i < 1):

        on = []
        off = ['BRAFi', 'Ca_ER_pumpi ']
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt, iterations=10)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i+1)
        plots_for_simulation(average_states,i,path_to_save)
        combined_states = average_states



    elif(i==1):
        if treatment == 'short':
            steps = 10
        else:
            steps = 30
        on = ['BRAFi']
        off = []
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt,iterations=steps)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i+1)
        plots_for_simulation(average_states,i,path_to_save)
        for key, value in combined_states.iteritems():
            value.extend(average_states[key])

    elif(i == 2):
        # ERK_state = combined_states['ERK']
        # ERK_state_mean = (sum(ERK_state[-20:])/len(ERK_state[-20:]))
        # if ERK_state_mean == 0:
        #     on = ['UK_node']
        off = ['Ca_ext']
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt, iterations=10)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i + 1)
        plots_for_simulation(average_states,i,path_to_save)
        for key, value in combined_states.iteritems():
            value.extend(average_states[key])

    elif(i == 3):
        on = ['Ca_ER_pumpi ']
        off = []
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt,iterations=10)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i+1)
        plots_for_simulation(average_states,i,path_to_save)
        for key, value in combined_states.iteritems():
            value.extend(average_states[key])

    else:
        on = ['Ca_ext']
        off = []
        new_txt = boolean2.modify_states(model_rules, turnon=on, turnoff=off)
        average_states, df, nodes = async_model_sim(new_txt, iterations=30)
        updating_initial_condition(model_rules, nodes, df, path_to_save, count=i + 1)
        # plots_for_simulation(average_states,i,path_to_save)
        for key, value in combined_states.iteritems():
            value.extend(average_states[key])

# print(combined_states)

plots_for_simulation(combined_states, "combined", path_to_save)
# plots_for_simulation_delay(combined_states, "combined_2", path_to_save)