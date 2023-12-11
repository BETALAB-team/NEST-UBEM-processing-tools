from qgis.core import QgsExpressionFunction, QgsFeature, QgsGeometry, QgsField, QgsExpression
import math
import numpy as np
@qgsfunction(args='auto', group='Custom', referenced_columns=[])
def GetAgeClass(feature, parent):
    agerandom=np.random.rand()
    CumulativeProbAge1 = feature['P[0000-1919]']
    CumulativeProbAge2 = feature['P[1920-1945]'] + CumulativeProbAge1
    CumulativeProbAge3 = feature['P[1946-1960]'] + CumulativeProbAge2
    CumulativeProbAge4 = feature['P[1961-1970]'] + CumulativeProbAge3
    CumulativeProbAge5 = feature['P[1971-1980]'] + CumulativeProbAge4
    CumulativeProbAge6 = feature['P[1981-1990]'] + CumulativeProbAge5
    CumulativeProbAge7 = feature['P[1991-2000]'] + CumulativeProbAge6
    CumulativeProbAge8 = feature['P[2001-2005]'] + CumulativeProbAge7
    if(agerandom<CumulativeProbAge1):
        result='0000-1919'
    elif(agerandom<CumulativeProbAge2):
        result='1920-1945'
    elif(agerandom<CumulativeProbAge3):
        result='1946-1960'
    elif(agerandom<CumulativeProbAge4):
        result='1961-1970'
    elif(agerandom<CumulativeProbAge5):
        result='1971-1980'
    elif(agerandom<CumulativeProbAge6):
        result='1981-1990'
    elif(agerandom<CumulativeProbAge7):
        result='1991-2000'
    elif(agerandom<CumulativeProbAge8):
        result='2001-2005'
    else:
        result='2006-3000'
    
    return result
