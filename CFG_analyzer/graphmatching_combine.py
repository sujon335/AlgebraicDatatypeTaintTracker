import networkx as nx
from networkx.algorithms import isomorphism
from networkx.algorithms.approximation import ramsey
import re
import os
import csv
import matplotlib.pyplot as plt
import sys
from networkx.algorithms.traversal.depth_first_search import dfs_tree
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
import numpy as np
from graphviz import Digraph

np.set_printoptions(threshold=sys.maxsize)
G1 = nx.Graph()
G2 = nx.Graph()

def read_txt(path):
    f1 = open(path)

    Families = []

    for line in f1:
        line = line.rstrip("\n")

        Families.append(str(line))
    f1.close()
    return Families

def read_file(path):
    f = open(path)

    graph = []

    for line in f:
        line = line.rstrip("\n")
        graph.append(str(line))
    f.close()
    return graph

def create_graph(graph, parent):
    
    l = len(graph)
    neighbors = []
    #G = nx.DiGraph()
    G = nx.MultiDiGraph()
    G1 = Digraph(comment = '')
    
    for i in range(0, l):
        string1 = graph[i]
        
        node = str(string1.split("---->")[0])
        node = node.replace(" ", "")
        
        if len(string1.split("---->")) > 1 and str(string1.split("---->")[1]).split(",") != [' []']:
            #print(string1)          
            edges = str(string1.split("---->")[1]).split(",")
           
            
            if not G.has_node(node):   
                G.add_node(node)
                G1.node(node)
            

            for j in range(0, len(edges)):
                
                edge = edges[j]
                edge = edge.replace("[","",1)
                edge = edge.replace("]","",-1)
                edge = edge.replace("'", "")                
                edge = edge.replace(" ", "")
                #nx.add_path(G, [node, edge])
                #if 'com/scvngr/levelup/' in edge:
                    
                G.add_edge(node, edge)
                G1.edge(node, edge)
                
                if node in parent:
                    neighbors.append(edge)
    #print(G.edges('Lcom/popdeem/sdk/core/utils/PDUniqueIdentifierUtils$GenerateUIDAsync;.doInBackground:([Ljava/lang/Void;)Ljava/lang/String;'))
    return G, neighbors

def create_subtree(Graph, node):
    T = nx.dfs_tree(Graph, source=node)
    return T

def print_loop(neighbor1, neighbor2, names1, names2, G1, G2):

    sum1 = []
    sum2 = []
    index1 = []
    index2 = []
    sum1 = 0
    io = False
    count = 0
    owncode = False

    #print(neighbor1)
    #print(neighbor2)

    sums1 = len(neighbor1) 
    sums2 = len(neighbor2)
   
    for i1 in range(0, len(neighbor1)):
        
        T1 = create_subtree(G1, neighbor1[i1])
        n1 = neighbor1[i1]
        
        match = False
        n_max = ""
        obfuscate = False
        i_max = -1
        ll2 = 0

        dd = {}
        nn = 0
        for i2 in range(0, len(neighbor2)):
            
            T2 = create_subtree(G2, neighbor2[i2])
            

            n1 = neighbor1[i1]
            n2 = neighbor2[i2]

            #if n1.split(":")[-1] == n2.split(":")[-1] and n1.split(":")[-1] == "(Landroid/content/Context;)Ljava/lang/String;":
           
            
            if n1.split(":")[-1] == n2.split(":")[-1]:
                
                if len(n1.split("/")) <= 2 or len(n2.split("/")) <= 2:
                    continue
                f11 = n1.split("/")[0]
                f12 = n1.split("/")[1]
                f13 = n1.split("/")[2]
                f21 = n2.split("/")[0]
                f22 = n2.split("/")[1]
                f23 = n2.split("/")[2]

                l1_local = str(n1.split(";")[0])

                for ii in range(1, len(l1_local.split("/"))):
                    f = l1_local.split("/")[ii]
                    if len(f) == 1:
                        obfuscate = True

                l2_local = str(n2.split(";")[0])
                for ii in range(1, len(l2_local.split("/"))):
                    f = l2_local.split("/")[ii]
                    if len(f) == 1:
                        obfuscate = True
                  
                if  len(l1_local.split("/")[len(l1_local.split("/")) - 1]) != 1 and len(l2_local.split("/")[len(l2_local.split("/")) - 1]) != 1:
                    #print(l1_local.split("/")[len(l1_local.split("/")) - 1])
                    obfuscate = False
      
                if f11 == f21: 
                    if len(f12) == 1 and len(f22) >= 1:
                        match = True
                    elif len(f12) >= 1 and len(f22) == 1:
                        match = True
                    
                    #nx.draw_networkx(T1)
                    
                    #nx.draw_networkx(T2)
                    
                    #plt.show()
                    #print(sorted(T1.degree, key=lambda x: x[1], reverse=True))


                if f11 == f21 and f12 == f22:

                    match = True
                
                if f13 != f23 and len(f13) > 1 and len(f23) > 1:

                    match = False


                if len(str(l1_local).split("/")) != len(str(l2_local).split("/")):

                    match = False

                m1 = str(str(str(n1.split(";")[1]).split(":")[0]).split(".")[1])
                m2 = str(str(str(n2.split(";")[1]).split(":")[0]).split(".")[1])
                #print(m1, m2)

                if len(m1) > 1 and len(m2) > 1:
                    match = False

                if match == True:

                    T1_deob = keep_argument(T1)
                    T2_deob = keep_argument(T2)

                    common = de_obfuscate(T1_deob, T2_deob)
                    
                    if n1 in dd:
                        if dd[n1] < common:
                            dd[n1] = common
                            nn = n2
                            ll2 = len(T2)
                    else:
                        dd[n1] = common
                        nn =n2
                        ll2 = len(T2)

                m1 = str(n1.split(";")[1]).split(":")[0]
                m2 = str(n2.split(";")[1]).split(":")[0]


        if n1 in dd:
            sum1 = sum1 + dd[n1]*2 + 2
            if (dd[n1]*2)/(len(T1) + ll2) >= 0.8:

                with open('/Users/sujon335/PycharmProjects/CFG_analyzer/TopFreeApps/matches2.csv', 'a') as file:
                    
                    file.write("{},{},{},{}".format(names1, names2, n1, nn))
                    file.write("\n")
                file.close()

                #print(names1, names2, n1, nn, (dd[n1]*2)/(len(T1) + ll2))

            if names1 in dic:
                ll = dic[names1]
                ll.append(n1)
                dic[names1] = ll 
            else:
                ll = [n1]
                dic[names1] = ll

            if names2 in dic:
                ll = dic[names2]
                ll.append(nn)
                dic[names2] = ll
            else:
                ll = [nn]
                dic[names2] = ll 


    if len(G1.edges())+ len(G2.edges()) == 0:
        #print("{},{},{}".format(names1, names2, 0))
        #print(0)
        return 0
    else:
        #print("{},{},{}".format(names1, names2, sum1/(len(G1.edges())+ len(G2.edges()))))
        #print(sum1/(len(G1.edges())+ len(G2.edges())))
        return 1 - sum1/(len(G1.edges())+ len(G2.edges()))

####remove obfuscated part
def keep_argument(Graph):
    
    G = nx.DiGraph()
    result = []
    list2 = list(Graph.edges())
    #print(list2)
    for edge in list2:
         
        s1 = str(edge[0].split(":")[-1])
        s2 = str(edge[1].split(":")[-1])
        result.append(tuple([s1,s2]))
    #print(edge)
    #nx.draw_networkx(Graph)
    #plt.show()
    return result

####deobfuscate graph
def de_obfuscate(list1, list2):

    visited1 = [False] * len(list1)
    visited2 = [False] * len(list2)
    intersection=[i for i in list1 if i in list2]
    #print(intersection)
    return len(intersection)
    #print(edges2)

#path1 = '/Users/xinyin/Downloads/PunchhTech/AndroidID/'
#path1 = '/Users/xinyin/Downloads/PunchhTech/IMEI/'
#path1 = '/Users/xinyin/Downloads/'
#path2 = '/Users/xinyin/Downloads/Graphs2/Paytronix/AndroidID/'
#path1= '/Users/xinyin/Downloads/LevelUp/IMEI/'
#path1 = '/Users/xinyin/Downloads/Combined_Graphs_With_All_IDs/Levelup/'
path1 = '/Users/sujon335/PycharmProjects/CFG_analyzer/TopFreeApps/Combined/'
#Families1 = ['CPKRewards.txt', 'DogfishOff.txt']
#Families1 = ['BlueSushiSakeGrill.txt', 'BluestoneLane.txt']
Families1 = read_txt(path1 + 'sort.txt')
#Families1 = ['DeliDoughRewards.txt', 'JPLicksRewards.txt', 'com.thanx.club801.txt']
#Families2 = read_txt(path2 + 'sort.txt')
#Families1 = ['graph_ML_CitybBQ_punchh.txt', 'graph_ML_freebirdrestaurant_punchh.txt']
#Families1 = ["graph_ML_SnappySalads_Punchh.txt"]
#Families2 = ["CityGreens.txt"]
#Families1 = ["DogfishOff.txt", "CPKRewards.txt"]
#Families1 = read_txt(path1 + 'sort.txt')
#Families2 = ['graph_ML_costavida_punchh.txt']
#Families = ['graph_ML_LYFEKITCHENRewards.txt', 'Beefsteak1.txt']
#Families1 = ['graph_ML_PieFivePizza_Punchh.txt', 'graph_ML_FarmerBoys_punchh.txt']
#Families = ['graph_ML_LYFEKITCHENRewards.txt', 'graph_ML_MoesRewards_Punchh.txt']
#two_d_array = [[0 for j in range(len(Families))] for i in range(len(Families))]

#print(Families)

distance_matrix = np.zeros((len(Families1), len(Families1)))

dic = {}
for i in range(0, len(Families1)):
    
    list1 =[]
    #print(Families[i])

    for j in range(i + 1, len(Families1)):  

        if i == j:
            edit_distance = 0

            continue

        graph1 = read_file(path1 + Families1[i])
        #print(Families1[j])
        graph2 = read_file(path1 + Families1[j])
        parent1 = ['IMEI', 'IMSI', 'AndroidID', 'SERIAL', 'MacAddress', 'AdvertisingID']
        parent2 = ['IMEI', 'IMSI', 'AndroidID', 'SERIAL', 'MacAddress', 'AdvertisingID']
        G1, nei1 = create_graph(graph1, parent1)
        G2, nei2 = create_graph(graph2, parent2)
        #print(Families1[j])   
        #nx.draw_networkx(G1)
        #plt.show()
        #nx.draw_networkx(G2)           
        #plt.show()

        names1 = str(Families1[i].split(".txt")[0])
        names2 = str(Families1[j].split(".txt")[0])

        
        edit_distance  = print_loop(nei1, nei2, names1, names2, G1, G2)
        

        if edit_distance < 0:
            edit_distance = 0
        
        distance_matrix[i][j] = edit_distance
        distance_matrix[j][i] = edit_distance
#print(dic)
        
import csv
row_list = 1 - distance_matrix

#############write similarity matrix
with open('/Users/sujon335/PycharmProjects/CFG_analyzer/TopFreeApps/similarity2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)
file.close()

############clustering ##############
############set eps #############
clustering = DBSCAN(eps = 0.5, min_samples = 2, metric = "precomputed").fit(distance_matrix)
print(clustering.labels_)
for j in range(0, 30):
    print("clustering ",j+1)
    for i in range(0, len(Families1)):
    
        if clustering.labels_[i] == j:
            print(Families1[i].replace(".txt", ""))
            #if Families1[i].replace(".txt", "") in dic:
            #    print(set(dic[Families1[i].replace(".txt", "")]))
#print(dic)
