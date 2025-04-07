import os
import json
import random

import pandas as pd
import geopandas as gpd
import numpy as np

with open("sc_complete.json", "r") as f:
    scorecards = json.load(f)


def select_from_dist(dist):
    keys = []
    values = []    
    v0 = 0
    
    rv = random.random()
    
    for k,v in dist.items():
        keys.append(k)
                
        values.append((v+v0)/100)
        v0 += v

        if rv <= v0/100:
            return k
        
    return keys[-1]
        



city_model = gpd.read_file(os.path.join("Input_files","EurecaInputAranellaVomero.geojson"))


########### Scorecard assignment ####################
city_model["Scorecard"] = "RES_APPBLOCK_1961-1970_B_SIC"
city_model["Scorecard"].loc[city_model["Envelope"].isin(["1945-1960","Before 1930","1930-1945"])] = "RES_APPBLOCK_1951-1960_B_SIC"

########### Input assignment     ####################
for i in city_model.index:
    
    sc = scorecards[city_model["Scorecard"].loc[i]]
    city_model["Envelope"].loc[i] = city_model["Scorecard"].loc[i]
    
    ##################### COOOLING SYSTEM ################
    cs_gen = {
        "Air-cooled chiller":"A-A split",
        "Absorption chiller":"A-A split",
        "Absent":"IdealLoad",
        "Unknown":"A-A split",
        "Water-cooled chiller":"A-W chiller",
     }[select_from_dist(sc["cooling system"]["type"])]
    
    
    cs_em = {
        "Chilled beams ":"Fan coil",
        "Fan coil":"Fan coil",
        "Mechanical ventilation Vents":"Fan coil",
        "Multisplit":"",
        "Passive chilled beams ":"Fan coil",
        "Radiant panels":"Radiant surface",
        "Unknown ":"Fan coil",
     }[select_from_dist(sc["cooling system"]["emission"])]
    
    if cs_gen == "A-W chiller":
        cs_gen = cs_gen + ", Centralized, " + cs_em
        
    city_model["Cooling System"].loc[i] = cs_gen
        
    ##################### HEATING SYSTEM ################
    hs_lay = {
        "Autonomous":"Single",
        "Centralized":"Centralized",
        "Absent":"IdealLoad",
        "Unknown":"Single",
     }[select_from_dist(sc["heating system"]["type"])]
    
    hs_gen = {
        "Air-source heat pump":"A-W HP Staffel",
        "Water-source heat pump":"G-W HP Staffel",
        "Air source heat pump":"A-W HP Staffel",
        "Ground-source heat pump ":"G-W HP Staffel",
        "Boiler (unknown type)":"Traditional Gas Boiler",
        "Boiler (unknown)":"Traditional Gas Boiler",
        "Condensing Boiler":"Condensing Gas Boiler",
        "Traditional Boiler":"Traditional Gas Boiler",
        "Fireplace":"Stove",
        "Heat exchanger of district heating/cooling":"",
        "DHC":"District Heating",
        "Unknown":"Traditional Gas Boiler",
     }[select_from_dist(sc["heating system"]["generator"])]
        
    hs_em = {
        "Air Heater":"Fan coil",
        "Convectors":"Fan coil",
        "Fan coil":"Fan coil",
        "Mechanical ventilation Vents":"Fan coil",
        "Radiant panles":"Radiant surface",
        "Radiators":"High Temp Radiator",
        "Radiator":"High Temp Radiator",
        "Air Heaters":"Fan coil",
        "Unknown ":"High Temp Radiator",
     }[select_from_dist(sc["heating system"]["emission"])]
    
    # TODO: VERIFY FUEL
    
    hs_tot = ""
    
    if hs_lay == "IdealLoad":
        hs_tot = "IdealLoad"
    else:
        if hs_gen == "Distric Heating":
            hs_lay = "Centralized"
            
        hs_tot =  hs_gen + ", " + hs_lay + ", " + hs_em
        
           
    city_model["Heating System"].loc[i] = hs_tot
    
city_model.to_file(os.path.join("Input_files","EurecaInputAranellaVomero_input.geojson"), driver = "GeoJSON")
    
    
    
    
    
        
        