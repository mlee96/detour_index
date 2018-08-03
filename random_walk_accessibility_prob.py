
import networkx as nx
import matplotlib.pyplot as plt
import shapely
import fiona
import numpy as np
import math
import sys
import os



R = 6371
def haversine(lon1,lat1,lon2,lat2): #x,y
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


class find_next:
    def __init__(self,start):
        self.s = start
    def next_node(self):
        start = self.s
        neighbors = G1.neighbors(start)
        neighbors = [nbor for nbor in neighbors if nbor !=start]
        visited_edges=[]
        if len(neighbors) == 0:
            return False
        else:
            ## prob
            distlist = [haversine(neighbors[nbor][0],neighbors[nbor][1],start[0],start[1]) for nbor in range(len(neighbors))]
            problist = [dist/sum(distlist) for dist in distlist]
#             print problist,neighbors
            ##
            nextidx=np.random.choice(len(neighbors),1,p=problist)[0]
            nextnode = neighbors[nextidx]
            edge = (start,nextnode)
            if edge in visited_edges or (edge[1],edge[0]) in visited_edges:
                idx = neighbors.index(nextnode)
                neighbors.remove(nextnode)
                if len(neighbors) == 0:
                    running = False
                else:
                    ## prob
                    del problist[idx]
                    nextidx=np.random.choice(len(neighbors),1,p=problist)[0]
                    nextnode = neighbors[nextidx]
                    edge = (start,nextnode)
                    start = nextnode
                    visited_edges.append(edge)
                    return(nextnode)
            else:
                start = nextnode
                visited_edges.append(edge)
                return(nextnode)



city_center = np.loadtxt('cities_center_coordinate_input.txt', dtype={'names':('city','lat','lon'),'formats':('S20','f4','f4')})

idx = int(sys.argv[1])
# idx = 0
# citylist = os.listdir('./data/')
# for idx in range(len(citylist)):
city = city_center[idx][0]
city=city.lower()
city=city.replace("_","")
result_file = "./street_network/"+city+"_accessibility_result_prob.txt"

filename = './street_network/data/test/' +city+'/edges/edges.shp'
print filename
if os.path.isfile(filename) == True:

    G = nx.read_shp(filename)
    G1 = nx.Graph(G)
    center = (city_center[idx][1],city_center[idx][2])

    for start in G1.nodes():
        endnode=[]
        pilist=[]
        sum_accessibility=0
        for m in range(1000):
            for n in range(20):
                f=find_next(start)
                start = f.next_node()
            endnode.append(start)

        for i in set(endnode):
            number = endnode.count(i)
            pi = float(number)/float(len(endnode))
            pilist.append(pi)
            ind_accessibility = pi*math.log(pi)
            sum_accessibility+=ind_accessibility
        accessibility = math.exp((-1.)*sum_accessibility)
        od = haversine(center[1],center[0],start[0],start[1])
        with open(result_file,'a') as f_output:
            f_output.write("%s,%f,%f,%f,%f\n"%(city,start[0],start[1],od, accessibility))

    

