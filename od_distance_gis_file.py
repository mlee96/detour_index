import numpy as np
import pandas as pd
import math
import os

def haversine(lon1,lat1,lon2,lat2):
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

city_center = np.loadtxt('cities_center_coordinate_input.txt', dtype={'names':('city','lat','lon'),'formats':('S20','f4','f4')})


# cityname = city_center[idx][0]
# lat, lon = city_center[idx][1],city_center[idx][2]
# cent_pos = (lon, lat)


radius = [2,5,10,15,20,30]
citylist= os.listdir('./cities_shortest_result_random')
stat_result = '/home/mlee/travel_route_2/df_data_random_2.csv'
for c in citylist:
	print c
	dirname = '/home/mlee/travel_route_2/cities_shortest_result_random/'+c
	if os.path.isdir(dirname)==True:
		if len(os.listdir(dirname))>5:
			gis_result = '/home/mlee/travel_route_2/cities_shortest_result_random/gis_data/'+c+'_gis.csv'
			if os.path.isfile(gis_result) ==True:
				continue
			else:
				print c, 'running'
				path_idx = 0
				for r in radius:
					filename = dirname+'/'+c+'_'+str(r)+'km_path_coordinate_shortest_2.txt'
					f = open(filename)
					c_idx = np.where(city_center['city']==c)[0][0]
					lat,lon = city_center[c_idx][1],city_center[c_idx][2]
					rmin,rmax = r*0.9, r*1.1
					for line in f.readlines():
						if path_idx ==0:
							angle, o,d = int(line.split()[3]),int(line.split()[1]),int(line.split()[2])
							path=[] 
							if angle>180:
								angle = 360-angle
							path_idx += 1
						else:
							if len(line.split())>2:
								if len(path)>2:
									st = haversine(path[0][0],path[0][1],path[-1][0],path[-1][1])
									oc,dc = haversine(lon,lat,path[0][0],path[0][1]),haversine(lon,lat,path[-1][0],path[-1][1])
									if st==0. :
										print c,path,st
									else:
										tr = sum(haversine(path[n][0],path[n][1],path[n+1][0],path[n+1][1]) for n in range(len(path)-1))
										df = tr/st
										with open(stat_result,'a') as f_output:
											f_output.write("%s,%d,%f,%f,%d,%d,%d,%f,%f,%f\n"%(c,r,oc,dc,angle, o,d,st,tr,df))
										if oc<rmin or oc>rmax or dc<rmin or dc>rmax :
											pass
										else:
											for p in path:
												with open(gis_result,'a') as f_gis:
													f_gis.write("%d,%d,%d,%f,%f\n"%(r,path_idx,angle,p[0],p[1]))


								else:
									pass
								angle, o,d = int(line.split()[3]),int(line.split()[1]),int(line.split()[2])
								if angle>180:
									angle = 360-angle
								path=[]
								path_idx += 1

							else:
								coords = (float(line.split()[0]),float(line.split()[1]))
								path.append(coords)
		else:
			print c, 'not enough data'
			continue
	else:
		print c, 'no directory'
		continue
