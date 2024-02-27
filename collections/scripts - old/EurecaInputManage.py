from qgis.core import *
from qgis.gui import *
from qgis.utils import qgsfunction
import numpy as np

@qgsfunction(args='auto', group='Custom', referenced_columns=[])
def GetEnvelope(feature, parent):
    age_class=feature['Age_Class']
    Envelope=age_class
    randomn=np.random.rand()
    if age_class=="0000-1919":
        Envelope="Before 1930"
    if age_class=="1920-1945":
        if randomn<0.4:
            Envelope="Before 1930"
        else:
            Envelope="1930-1945"
    if age_class == "1946-1960":
        Envelope="1945-1960"
    if age_class == "2001-2005":
        Envelope="2000-2005"
    if age_class == "2006-3000":
        if randomn<(5/6):
            Envelope="2005-2010"
        else:
            Envelope="After 2010"

    return Envelope
