import networkx as nx
import matplotlib.pyplot as plt

a = ['BRAFi', 'BRAF', 'MEK', 'ERK', 'Tc', 'Tl', 'Gene_exp']
b = ['Ca_ext', 'Ca_channel', 'Ca_cyt_normal', 'Ca_cyt_high', 'ER_pump', 'ER_pumpi', 'Ca_ER']
B = nx.Graph()
B.add_nodes_from(a, bipartite=0)
B.add_nodes_from(b, bipartite=1)

B.add_edges_from([('Ca_cyt_high', "MEK"), ('Ca_channel', "ERK"), ('Ca_channel', 'Gene_exp')])

left_or_top = a

pos = nx.bipartite_layout(B, left_or_top)

nx.draw(B,pos,node_color='#A0CBE2',edge_color='#00bb5e',width=1,
     edge_cmap=plt.cm.Blues,with_labels=True)

plt.savefig('Bipartite.png',dpi=200)
plt.show()