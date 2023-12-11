from qgis.core import QgsExpressionFunction, QgsFeature, QgsGeometry, QgsField, QgsExpression
import math
import numpy as np

@qgsfunction(args='auto', group='Custom', referenced_columns=[])
def GetEndUse(feature, parent):
    randomn=np.random.rand()
    result = feature['enduse_amenity']

    if result == None:
        result = feature ['enduse_shop']
        if result != None:
            result = "shop"

    if result == None: 
        result = feature['enduse_food']
        if result != None:
            result = "food"

    if result == None:
        if feature['building']=="industrial":
            result="industrial"

    if result == None:
        if randomn<feature['P[Res]']:
            result="residential"

        else:
            result="services"

            
    
                
        
    return result
