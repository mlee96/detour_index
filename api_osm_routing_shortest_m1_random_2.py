import urllib2
import httplib
import os
import numpy as np
from math import radians, cos, sin, asin, sqrt
import math
import time 
import json
import datetime
import sys
import random


R = 6371
def haversine(lon1,lat1,lon2,lat2):
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def find_area(array):
    a = 0
    ox,oy = array[0]
    for x,y in array[1:]:
        a += (x*oy-y*ox)
        ox,oy = x,y
    x,y = array[0]
    a += (x*oy-y*ox)
    return abs(a)/2

def straight_line(o_x,o_y,d_x,d_y):
	slope = (d_y-o_y)/(d_x-o_x)
	intersect = o_y - slope*o_x 
	return slope, intersect


def od_coord(lat1,lon1,angle,d):
	brng = float(angle)*(math.pi / 180)
	lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
	             math.cos(lat1)*math.sin(d/R)*math.cos(brng))
	lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
	                     math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
	lat2 *= 180/math.pi
	lon2 *= 180/math.pi
	# print brng
	return lat2,lon2


######################
# Getting o-d points #
######################
error_log_file = "osmrouting_short_error.txt"
result_log_file = "osmrouting_short_result.txt"

with open(result_log_file,'a') as f_result:
	f_result.write("%s\n"%(datetime.datetime.now()))
#*** INPUT***#
city_center = np.loadtxt('cities_center_coordinate_input.txt', dtype={'names':('city','lat','lon'),'formats':('S20','f4','f4')})
#*** INPUT***#

# idx = 0
idx = int(sys.argv[1])
print idx
cityname = city_center[idx][0]
lat, lon = city_center[idx][1],city_center[idx][2]
cent_pos = (lon, lat)
print cityname,cent_pos
with open(result_log_file,'a') as f_result:
	f_result.write("%s,%f,%f\n"%(cityname, lat,lon))
dir_name = "./cities_shortest_result_random/"+cityname
if not os.path.exists(dir_name):
	os.makedirs(dir_name)

# input_filename = './cities_input_data/travel_route_2/'+cityname+'_radius_coordinate_osm.txt'
lat1 = lat * (math.pi / 180) #Current lat point converted to radians
lon1 = lon * (math.pi / 180) #Current long point converted to radians

# ####################
# #finding direction #
# ####################

output_filename = "./cities_shortest_result_random/"+cityname+"/" +cityname+'_path_coordinate_shortest_random_100000.txt'
if os.path.isfile(output_filename)==True:
	os.remove(output_filename)
routes = []
angles = []
count = 0

while count < 100000:
 	### selecting OD pairs
 	bound1,bound2,bound1,bound2 = od_coord(lat1,lon1,0,10),od_coord(lat1,lon1,90,10),od_coord(lat1,lon1,180,10),od_coord(lat1,lon1,270,10)
	lat= od_coord(lat1,lon1,0,10)[0],od_coord(lat1,lon1,90,10)[0],od_coord(lat1,lon1,180,10)[0],od_coord(lat1,lon1,270,10)[0]
	lon = od_coord(lat1,lon1,0,10)[1],od_coord(lat1,lon1,90,10)[1],od_coord(lat1,lon1,180,10)[1],od_coord(lat1,lon1,270,10)[1]

	orig_coord,dest_coord = (random.uniform(min(lat),max(lat)),random.uniform(min(lon),max(lon))),(random.uniform(min(lat),max(lat)),random.uniform(min(lon),max(lon)))

	### get route

	url = "http://www.yournavigation.org/api/1.0/gosmore.php?flon=" +str(orig_coord[1])+"&flat="+str(orig_coord[0])+ "&tlon="+str(dest_coord[1])+"&tlat="+str(dest_coord[0])+"&v=motorcar&format=geojson&fast=0&instructions=0"
	request = urllib2.Request(url)
	opener = urllib2.build_opener()  
	request.add_header('User-Agent','Research/Sungkyunkyan Univeristy/minjin.lee.9@gmail.com')
	try:
		result = opener.open(request)
	except:
		continue
	try:
		data = json.loads(result.read())
	except :		
		continue


	
	if len(data['coordinates'])<1:
		continue

	result.close()				
	n_via_points = len(data['coordinates'])
	via_points=[]
	for p in range(n_via_points):
		x,y = map(float,data['coordinates'][p])
		sets=(x,y)
		via_points.append(sets)
		with  open(output_filename,'a') as f_output:
			f_output.write("%d,%f,%f\n"%(count,x, y))
		

	routes.append(via_points)
	count += 1




