from qgis.core import QgsExpressionFunction, QgsFeature, QgsGeometry, QgsField, QgsExpression
import math
import numpy as np

@qgsfunction(args='auto', group='Custom', referenced_columns=[])
def FloorByMajority(feature, parent):
    ratioes=[feature['PF[1]'],feature['PF[2]'],feature['PF[3]'],feature['PF[4+]']]
    Magiority_percentage=max(ratioes)
    if(feature['PF[1]']==Magiority_percentage):
        result=1
    if(feature['PF[2]']==Magiority_percentage):
        result=2 
    if(feature['PF[3]']==Magiority_percentage):
        result=3
    if(feature['PF[4+]']==Magiority_percentage):
        result=4
    return result
    
@qgsfunction(args='auto', group='Custom', referenced_columns=[])
def FloorByStatistics(feature, parent):
    mu=feature['Mu_floor']
    std=feature['Std_floor']
    result= np.random.lognormal(mu,std)
    return result
    
@qgsfunction(args='auto', group='Custom', referenced_columns=[])
def HeightCalc(mode,feature, parent):
    height=feature['Height_mean']
    mode=int(mode)
    if height == None:
        if mode==1:
            height=3.5*feature['Floors_by_majority']
        if mode==0:
            height=3.5*feature['Floors_by_Statistics']
    return height
    
@qgsfunction(args='auto', group='Custom', referenced_columns=[])
def FloorCalc(mode,feature, parent):
    height_gp=feature['Height_mean']
    heightt=feature['Height']
    if (height_gp!=None):
        floor=feature['Height']//3.5
        if(floor==0):
            floor=1
    else:
        mode=int(mode)
        if mode==1:
            floor=feature['Floors_by_majority']
        if mode==0:
            floor=feature['Floors_by_Statistics']
    return floor
