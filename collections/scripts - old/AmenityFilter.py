from qgis.core import *
from qgis.gui import *
from qgis.utils import qgsfunction

@qgsfunction(args='auto', group='Custom', referenced_columns=[])
def AmenFilter(feature, parent):
    ENDUSES={
    "services":["public_building","post_office","bank","police","fire_station","fuel","community_centre","townhall","prison","courthouse","funeral_hall","crematorium","grave_yard","bicycle_parking","driving_school"],
    "cultural":["cinema","theatre","events_venue","planetarium","library"],
    "school":["kindergarten","college","childcare","school"],
    "medical":["doctors","hospital"],
    "commerce":["pharmacy"],
    "All_Commerce":["car_wash","mall","supermarket"],
    "Night_Life":["pub","nightclub"],
    "Food":["restaurant","cafe","canteen","bar","fast_food","ice_cream"],
    "Worship":["place_of_worship","monastery"],
    "University":["university"],
    }
    variable=feature["amenity"]
    for key, values in ENDUSES.items():
        if variable in values:
            return key
            break
    return None
