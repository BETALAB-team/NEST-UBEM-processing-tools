# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:49:56 2024

@author: khaje
"""
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.ops import unary_union

geojson_path = 'D:/Projects/PNRR/Eureca/PNRR/Eureca input/bb.geojson'

# Read the GeoJSON file into a GeoDataFrame
gdf = gpd.read_file(geojson_path)

#Add geometrical parameters
gdf['area'] = gdf['geometry'].area
gdf['centroid']=gdf['geometry'].centroid
gdf['longitude']=gdf['centroid'].x
gdf['latitude']=gdf['centroid'].y

#Define index_count
index_count=0
while index_count<len(gdf):
    #start with a building
    check_count=0
    curr_building=gdf.iloc[index_count]
    x_curr=curr_building['longitude']
    y_curr=curr_building['latitude']
    gdf_check=gdf.copy()
    #find 
    gdf_check=gdf_check[~(gdf_check["id"]==curr_building["id"])]
    gdf_check['distance']=np.sqrt((gdf_check['latitude']-y_curr)**2+(gdf_check['longitude']-x_curr)**2)
    gdf_check.reset_index(drop=True, inplace=True)
    current_check=gdf_check.iloc[check_count]
    condition_enduse=(curr_building["End Use"]==current_check["End Use"])
    if condition_enduse:
        gdf.at[index_count,"geometry"]=unary_union([curr_building["geometry"],current_check["geometry"]])
        gdf=gdf[~(gdf["id"]==current_check["id"])]
        gdf.reset_index(drop=True, inplace=True)
    else:
        index_count=index_count+1
    # gdf_check.sort_values(by='aa', inplace=True)
    print(f"{index_count}:{condition_enduse}:{curr_building['End Use']}:{current_check['End Use']}")
gdf.drop(["centroid"],inplace=True,axis=1)
gdf.to_file('D:/Projects/PNRR/Eureca/PNRR/Eureca input/cc.geojson', driver='GeoJSON')