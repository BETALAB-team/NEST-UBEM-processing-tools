''' IMPORTING MODULES '''

import os

from eureca_building.config import load_config
load_config(os.path.join("InputAux","config.json"))

from eureca_ubem.city import City

weather_file = os.path.join(".","InputAux","ITA_Venezia-Tessera.161050_IGDG.epw")
schedules_file = os.path.join(".","InputAux","Schedules.xlsx")
materials_file = os.path.join(".","InputAux","total envelope types.xlsx")
city_model_file = os.path.join(".","Input Geojson","Padova_City_Center.geojson")

city_geojson = City(
    city_model=city_model_file,
    epw_weather_file=weather_file,
    end_uses_types_file=schedules_file,
    envelope_types_file=materials_file,
    shading_calculation=True,
    building_model = "2C",
    output_folder=os.path.join(".","Sample Output")
)
city_geojson.loads_calculation()
city_geojson.simulate(print_single_building_results=False, output_type="csv")
