"""
Model exported as python.
Name : modello
Group : 
With QGIS : 32812
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modello(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # ISTAT sections (2011) - Vector layer with Polygons
        self.addParameter(QgsProcessingParameterVectorLayer('r20_11_wgs84__r20_11_wgs84_studyarea', 'R20_11_WGS84 — R20_11_WGS84_StudyArea', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        # Vector layer from csv (with no geometry) - ISTAT data (2011)
        self.addParameter(QgsProcessingParameterVectorLayer('r20_indicatori_2011_sezioni_studyarea', 'R20_indicatori_2011_sezioni_StudyArea', types=[QgsProcessing.TypeVector], defaultValue=None))
        # "Volume units" vector layer from Cagliari DBGT (Geotopographic Database)
        self.addParameter(QgsProcessingParameterVectorLayer('st02te01cl01_dbgt_cagliari_uvol_studyarea', 'ST02TE01CL01_DBGT_Cagliari_UVOL_StudyArea', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        # "Building units" vector layer from Cagliari DBGT (Geotopographic Database)
        self.addParameter(QgsProcessingParameterVectorLayer('st02te01cl02_dbgt_cagliari_uedil_studyarea', 'ST02TE01CL02_DBGT_Cagliari_UEDIL_StudyArea', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('R_20_istat_sections', 'R_20_ISTAT_Sections', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('Istatdbgtosm_joinedlayer', 'ISTAT-DBGT-OSM_JoinedLayer', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('Eureca_input', 'EURECA_input', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(55, model_feedback)
        results = {}
        outputs = {}

        # Height calculation
        # Heights calculation of unit volumes
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'UVOL_TotHeight',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if(("A02010101" = -3 OR "A02010102" = -3),0,"A02010101" - "A02010102")',
            'INPUT': parameters['st02te01cl01_dbgt_cagliari_uvol_studyarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['HeightCalculation'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Aggiungi campo autoincrementale
        # Creation of an autoincremental field
        alg_params = {
            'FIELD_NAME': 'AUTO_NUMB',
            'GROUP_FIELDS': [''],
            'INPUT': parameters['st02te01cl02_dbgt_cagliari_uedil_studyarea'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AggiungiCampoAutoincrementale'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # ID creation
        # Creation of an univocal ID
        alg_params = {
            'FIELD_LENGTH': 9,
            'FIELD_NAME': 'UEDIL_ID',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': ' concat( \'UEDIL_\', to_string( "AUTO_NUMB"))',
            'INPUT': outputs['AggiungiCampoAutoincrementale']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IdCreation'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Crea indice spaziale
        # Creation of a spatial index (for faster calculations)
        alg_params = {
            'INPUT': parameters['r20_11_wgs84__r20_11_wgs84_studyarea']
        }
        outputs['CreaIndiceSpaziale'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Delete the autoincremental field
        # Delete unuseful fields
        alg_params = {
            'COLUMN': ['AUTO_NUMB'],
            'INPUT': outputs['IdCreation']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeleteTheAutoincrementalField'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Join ISTAT sections data
        # Join ISTAT sections data
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'SEZ2011',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'SEZ2011',
            'INPUT': outputs['CreaIndiceSpaziale']['OUTPUT'],
            'INPUT_2': parameters['r20_indicatori_2011_sezioni_studyarea'],
            'METHOD': 1,  # Prendi solamente gli attributi del primo elemento corrispondente (uno-a-uno)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinIstatSectionsData'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # OSM_GetEnduseData_UNICA
        # Get OSM data to get more specific end uses
        alg_params = {
            'osm_items': 'TEMPORARY_OUTPUT',
            'r20_11_wgs84__r20_11_wgs84_studyarea': parameters['r20_11_wgs84__r20_11_wgs84_studyarea'],
            'osm_items': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Osm_getendusedata_unica'] = processing.run('project:OSM_GetEnduseData_UNICA', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Rename field "A02010101" as "UVOL_EavesHeight"
        alg_params = {
            'FIELD': 'A02010101',
            'INPUT': outputs['HeightCalculation']['OUTPUT'],
            'NEW_NAME': 'UVOL_EavesHeight',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldA02010101AsUvol_eavesheight'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Add UDEL_EndUse field
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'UEDIL_EndUse',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': 'CASE WHEN "A02010201" = \'00\' \r\nTHEN \'Generic\' \r\nWHEN "A02010201" = \'01\'\r\nTHEN \'Public building\'\r\nWHEN ("A02010201" = \'0120\' OR "A02010201" = \'0121\' OR "A02010201" = \'0124\' OR "A02010201" = \'0125\' OR "A02010201" = \'0126\'OR "A02010201" = \'0127\')\r\nTHEN \'School\'\r\nWHEN "A02010201" = \'0128\'\r\nTHEN \'University\'\r\nWHEN "A02010201" = \'0121\'\r\nTHEN \'Services\'\r\nWHEN ("A02010201" = \'0305\' OR "A02010201" = \'0310\')\r\nTHEN \'Industrial\'\r\nWHEN "A02010201" = \'0403\'\r\nTHEN \'Commercial\'\r\nWHEN "A02010201" = \'05\'\r\nTHEN \'Residential\'\r\nWHEN ("A02010201" = \'0710\' OR "A02010201" = \'0705\' OR "A02010201" = \'0706\')\r\nTHEN \'Sport\'\r\nWHEN ("A02010201" = \'0701\' OR "A02010201" = \'0702\' OR "A02010201" = \'0703\' OR "A02010201" = \'0707\' OR "A02010201" = \'0712\' OR "A02010201" = \'0715\')\r\nTHEN \'Cultural\'\r\nWHEN "A02010201" = \'08\'\r\nTHEN \'Worship\'\r\nEND',
            'INPUT': outputs['DeleteTheAutoincrementalField']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddUdel_enduseField'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Delete ISTAT unuseful fields
        alg_params = {
            'COLUMN': ['COD_ISTAT','PRO_COM','SEZ','COD_STAGNO','COD_FIUME','COD_LAGO','COD_LAGUNA','COD_VAL_P','COD_ZONA_C','COD_IS_AMM','COD_IS_LAC','COD_IS_MAR','COD_AREA_S','COD_MONT_D','LOC2011','COD_LOC','TIPO_LOC','COM_ASC','COD_ASC','ACE','SEZ2011_2'],
            'INPUT': outputs['JoinIstatSectionsData']['OUTPUT'],
            'OUTPUT': parameters['R_20_istat_sections']
        }
        outputs['DeleteIstatUnusefulFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['R_20_istat_sections'] = outputs['DeleteIstatUnusefulFields']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # ISTAT sections with spatial index
        alg_params = {
            'INPUT': outputs['DeleteIstatUnusefulFields']['OUTPUT']
        }
        outputs['IstatSectionsWithSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Rename field "A02010102" as "UVOL_BaseHeight"
        alg_params = {
            'FIELD': 'A02010102',
            'INPUT': outputs['RenameFieldA02010101AsUvol_eavesheight']['OUTPUT'],
            'NEW_NAME': 'UVOL_BaseHeight',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldA02010102AsUvol_baseheight'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings/Total Buildings
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'ResBuild_Ratio',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': '"E3"/"E1"',
            'INPUT': outputs['IstatSectionsWithSpatialIndex']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildingstotalBuildings'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Rename field "A02010103" as "UVOL_RoofPeak"
        alg_params = {
            'FIELD': 'A02010103',
            'INPUT': outputs['RenameFieldA02010102AsUvol_baseheight']['OUTPUT'],
            'NEW_NAME': 'UVOL_RoofPeak',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldA02010103AsUvol_roofpeak'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Rename field "A02010104" as "UVOL_Type"
        alg_params = {
            'FIELD': 'A02010104',
            'INPUT': outputs['RenameFieldA02010103AsUvol_roofpeak']['OUTPUT'],
            'NEW_NAME': 'UVOL_Type',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldA02010104AsUvol_type'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Rename field "A02010208" as "UEDIL_Type"
        alg_params = {
            'FIELD': 'A02010208',
            'INPUT': outputs['AddUdel_enduseField']['OUTPUT'],
            'NEW_NAME': 'UEDIL_Type',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldA02010208AsUedil_type'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings [ante 1919] ratio
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Rat[ante1919]',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("E8"/"E3" = NULL,0,"E8"/"E3")',
            'INPUT': outputs['CalculateResidentialBuildingstotalBuildings']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildingsAnte1919Ratio'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Rename field "Shape_Leng" as "UVOL_ShapeLeng"
        alg_params = {
            'FIELD': 'Shape_Leng',
            'INPUT': outputs['RenameFieldA02010104AsUvol_type']['OUTPUT'],
            'NEW_NAME': 'UVOL_ShapeLeng',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldShape_lengAsUvol_shapeleng'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Rename field "Shape_Area" as "UVOL_ShapeArea"
        alg_params = {
            'FIELD': 'Shape_Area',
            'INPUT': outputs['RenameFieldShape_lengAsUvol_shapeleng']['OUTPUT'],
            'NEW_NAME': 'UVOL_ShapeArea',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldShape_areaAsUvol_shapearea'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Rename field "A02010209" as "UEDIL_Status"
        alg_params = {
            'FIELD': 'A02010209',
            'INPUT': outputs['RenameFieldA02010208AsUedil_type']['OUTPUT'],
            'NEW_NAME': 'UEDIL_Status',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldA02010209AsUedil_status'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings [1919-1945] ratio
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Rat[1919-1945]',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("E9"/"E3" = NULL,0,"E9"/"E3")',
            'INPUT': outputs['CalculateResidentialBuildingsAnte1919Ratio']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildings19191945Ratio'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings [1946-1960] ratio
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Rat[1946-1960]',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("E10"/"E3" = NULL,0,"E10"/"E3")',
            'INPUT': outputs['CalculateResidentialBuildings19191945Ratio']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildings19461960Ratio'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Keep UVOL useful fields
        alg_params = {
            'FIELDS': ['UVOL_EavesHeight','UVOL_BaseHeight','UVOL_RoofPeak','UVOL_Type','UVOL_ShapeLeng','UVOL_ShapeArea','UVOL_TotHeight'],
            'INPUT': outputs['RenameFieldShape_areaAsUvol_shapearea']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['KeepUvolUsefulFields'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Rename field "A02010211" as "UEDIL_Underground"
        alg_params = {
            'FIELD': 'A02010211',
            'INPUT': outputs['RenameFieldA02010209AsUedil_status']['OUTPUT'],
            'NEW_NAME': 'UEDIL_Underground',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldA02010211AsUedil_underground'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # UVOL spatial indexes
        alg_params = {
            'INPUT': outputs['KeepUvolUsefulFields']['OUTPUT']
        }
        outputs['UvolSpatialIndexes'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Rename field "Shape_Leng" as "UEDIL_ShapeLeng"
        alg_params = {
            'FIELD': 'Shape_Leng',
            'INPUT': outputs['RenameFieldA02010211AsUedil_underground']['OUTPUT'],
            'NEW_NAME': 'UEDIL_ShapeLeng',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldShape_lengAsUedil_shapeleng'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings [1961-1970] ratio
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Rat[1961-1970]',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("E11"/"E3" = NULL,0,"E11"/"E3")',
            'INPUT': outputs['CalculateResidentialBuildings19461960Ratio']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildings19611970Ratio'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Rename field "Shape_Area" as "UEDIL_ShapeArea"
        alg_params = {
            'FIELD': 'Shape_Area',
            'INPUT': outputs['RenameFieldShape_lengAsUedil_shapeleng']['OUTPUT'],
            'NEW_NAME': 'UEDIL_ShapeArea',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldShape_areaAsUedil_shapearea'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings [1971-1980] ratio
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Rat[1971-1980]',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("E12"/"E3" = NULL,0,"E12"/"E3")',
            'INPUT': outputs['CalculateResidentialBuildings19611970Ratio']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildings19711980Ratio'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Keep UEDIL useful fields
        alg_params = {
            'FIELDS': ['UEDIL_ID','UEDIL_EndUse','UEDIL_Type','UEDIL_Status','UEDIL_Underground','UEDIL_ShapeLeng','UEDIL_ShapeArea'],
            'INPUT': outputs['RenameFieldShape_areaAsUedil_shapearea']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['KeepUedilUsefulFields'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings [1981-1990] ratio
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Rat[1981-1990]',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("E13"/"E3" = NULL,0,"E13"/"E3")',
            'INPUT': outputs['CalculateResidentialBuildings19711980Ratio']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildings19811990Ratio'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings [1991-2000] ratio
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Rat[1991-2000]',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("E14"/"E3" = NULL,0,"E14"/"E3")',
            'INPUT': outputs['CalculateResidentialBuildings19811990Ratio']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildings19912000Ratio'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings [2001-2005] ratio
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Rat[2001-2005]',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("E15"/"E3" = NULL,0,"E15"/"E3")',
            'INPUT': outputs['CalculateResidentialBuildings19912000Ratio']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildings20012005Ratio'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Calculate Residential Buildings [post 2005] ratio
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Rat[post2005]',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("E16"/"E3" = NULL,0,"E16"/"E3")',
            'INPUT': outputs['CalculateResidentialBuildings20012005Ratio']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateResidentialBuildingsPost2005Ratio'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # UEDIL spatial indexes
        alg_params = {
            'INPUT': outputs['KeepUedilUsefulFields']['OUTPUT']
        }
        outputs['UedilSpatialIndexes'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Join UEDIL with OSM
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UedilSpatialIndexes']['OUTPUT'],
            'JOIN': outputs['Osm_getendusedata_unica']['osm_items'],
            'JOIN_FIELDS': [''],
            'METHOD': 2,  # Prendi solamente gli attributi dell'elemento con maggiore sovrapposizione (uno-a-uno)
            'PREDICATE': [0],  # interseca
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinUedilWithOsm'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Add field "End Use"
        # Add field "End Use" as main end use of the building by comparing data from DBGT UEDIL (building units) and OSM
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'End Use',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': 'CASE WHEN ("UEDIL_EndUse" <> \'Generic\' AND "UEDIL_EndUse" <> \'School\')\r\nTHEN "UEDIL_EndUse"\r\nWHEN ("UEDIL_EndUse" <> \'Generic\' AND "UEDIL_EndUse"  = \'School\' AND ("OSM_building"  = \'university\' OR "OSM_amenity" = \'University\'))\r\nTHEN \'University\'\r\nWHEN ("UEDIL_EndUse" <> \'Generic\' AND "UEDIL_EndUse"  = \'School\' AND ("OSM_building"  <> \'university\' OR "OSM_amenity" <> \'University\'))\r\nTHEN \'School\'\r\nWHEN ("UEDIL_EndUse" = \'Generic\' AND ("OSM_building" = \'yes\' OR "OSM_building" IS NULL) AND "OSM_amenity" IS NULL)\r\nTHEN \'Generic\'\r\nWHEN ("UEDIL_EndUse" = \'Generic\' AND "OSM_building" IS NOT NULL AND "OSM_building" <> \'yes\')\r\nTHEN "OSM_building"\r\nWHEN ("UEDIL_EndUse" = \'Generic\' AND ("OSM_building" = \'yes\' OR "OSM_building" IS NULL) AND "OSM_amenity" IS NOT NULL)\r\nTHEN "OSM_amenity"\r\nELSE \'Generic\'\r\nEND',
            'INPUT': outputs['JoinUedilWithOsm']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddFieldEndUse'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Edit field "End Use"
        # Edit field "End Use" to uniform the values
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'End Use',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': 'CASE WHEN "End Use" = \'sport\'\r\nTHEN \'Sport\'\r\nWHEN ("End Use" = \'apartments\' OR "End Use" = \'residential\')\r\nTHEN \'Residential\'\r\nWHEN ("End Use" = \'school\')\r\nTHEN \'School\'\r\nWHEN "End Use" = \'Food\'\r\nTHEN \'Commercial\'\r\nELSE "End Use"\r\nEND',
            'INPUT': outputs['AddFieldEndUse']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['EditFieldEndUse'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Add field "End Use (ground floor)"
        # Add field "End Use (ground floor)" by checking for different uses with respect to upper floors from OSM shops and food layers
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'End Use (ground floor)',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': 'CASE WHEN ("OSM_shop" IS NULL AND "OSM_food" IS NULL)\r\nTHEN "End Use"\r\nWHEN "OSM_shop" IS NOT NULL OR "OSM_food" IS NOT NULL\r\nTHEN \'Commercial\'\r\nEND',
            'INPUT': outputs['EditFieldEndUse']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddFieldEndUseGroundFloor'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # Add ISTAT section names to OSM-UEDIL
        # Add ISTAT section names to joined OSM- UEDIL with grater overlap
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['AddFieldEndUseGroundFloor']['OUTPUT'],
            'JOIN': outputs['IstatSectionsWithSpatialIndex']['OUTPUT'],
            'JOIN_FIELDS': ['SEZ2011'],
            'METHOD': 2,  # Prendi solamente gli attributi dell'elemento con maggiore sovrapposizione (uno-a-uno)
            'PREDICATE': [0],  # interseca
            'PREFIX': 'ISTAT_',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddIstatSectionNamesToOsmuedil'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Join UVOL (volume units) with UEDIL (building units)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UvolSpatialIndexes']['OUTPUT'],
            'JOIN': outputs['AddIstatSectionNamesToOsmuedil']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 1,  # Prendi solamente gli attributi del primo elemento corrispondente (uno-a-uno)
            'PREDICATE': [0],  # interseca
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinUvolVolumeUnitsWithUedilBuildingUnits'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Add ISTAT calculated attribute
        # Add ISTAT calculated attributes to the UEDIL-UVOL joined layer based on ISTAT section names
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ISTAT_SEZ2011',
            'FIELDS_TO_COPY': ['Rat[ante1919]','Rat[1919-1945]','Rat[1946-1960]','Rat[1961-1970]','Rat[1971-1980]','Rat[1981-1990]','Rat[1991-2000]','Rat[2001-2005]','Rat[post2005]'],
            'FIELD_2': 'SEZ2011',
            'INPUT': outputs['JoinUvolVolumeUnitsWithUedilBuildingUnits']['OUTPUT'],
            'INPUT_2': outputs['CalculateResidentialBuildingsPost2005Ratio']['OUTPUT'],
            'METHOD': 1,  # Prendi solamente gli attributi del primo elemento corrispondente (uno-a-uno)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddIstatCalculatedAttribute'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # Assign age class
        # The prevalent age class in each ISTAT section is assigned to all buildings of the section.
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Age_Class',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': 'CASE WHEN max("Rat[ante1919]","Rat[1919-1945]","Rat[1946-1960]","Rat[1961-1970]","Rat[1971-1980]","Rat[1981-1990]","Rat[1991-2000]","Rat[2001-2005]","Rat[post2005]") = "Rat[ante1919]" THEN \'0000-1918\' WHEN  max("Rat[ante1919]","Rat[1919-1945]","Rat[1946-1960]","Rat[1961-1970]","Rat[1971-1980]","Rat[1981-1990]","Rat[1991-2000]","Rat[2001-2005]","Rat[post2005]") = "Rat[1919-1945]" THEN \'1919-1945\' WHEN  max("Rat[ante1919]","Rat[1919-1945]","Rat[1946-1960]","Rat[1961-1970]","Rat[1971-1980]","Rat[1981-1990]","Rat[1991-2000]","Rat[2001-2005]","Rat[post2005]") = "Rat[1946-1960]" THEN \'1946-1960\' WHEN  max("Rat[ante1919]","Rat[1919-1945]","Rat[1946-1960]","Rat[1961-1970]","Rat[1971-1980]","Rat[1981-1990]","Rat[1991-2000]","Rat[2001-2005]","Rat[post2005]")="Rat[1961-1970]" THEN \'1961-1970\' WHEN  max("Rat[ante1919]","Rat[1919-1945]","Rat[1946-1960]","Rat[1961-1970]","Rat[1971-1980]","Rat[1981-1990]","Rat[1991-2000]","Rat[2001-2005]","Rat[post2005]")="Rat[1971-1980]" THEN \'1971-1980\' WHEN  max("Rat[ante1919]","Rat[1919-1945]","Rat[1946-1960]","Rat[1961-1970]","Rat[1971-1980]","Rat[1981-1990]","Rat[1991-2000]","Rat[2001-2005]","Rat[post2005]") = "Rat[1981-1990]" THEN \'1981-1990\' WHEN max("Rat[ante1919]","Rat[1919-1945]","Rat[1946-1960]","Rat[1961-1970]","Rat[1971-1980]","Rat[1981-1990]","Rat[1991-2000]","Rat[2001-2005]","Rat[post2005]") = "Rat[1991-2000]" THEN \'1991-2000\' WHEN  max("Rat[ante1919]","Rat[1919-1945]","Rat[1946-1960]","Rat[1961-1970]","Rat[1971-1980]","Rat[1981-1990]","Rat[1991-2000]","Rat[2001-2005]","Rat[post2005]") = "Rat[2001-2005]" THEN \'2001-2005\' ELSE \'2006-3000\' END',
            'INPUT': outputs['AddIstatCalculatedAttribute']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AssignAgeClass'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}

        # Delete unuseful fields from UVOL-UEDIL layer
        alg_params = {
            'COLUMN': ['Rat[ante1919]','Rat[1919-1945]','Rat[1946-1960]','Rat[1961-1970]','Rat[1971-1980]','Rat[1981-1990]','Rat[1991-2000]','Rat[2001-2005]','Rat[post2005]'],
            'INPUT': outputs['AssignAgeClass']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeleteUnusefulFieldsFromUvoluedilLayer'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # Calculation of floors number
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Floors',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Intero (32 bit)
            'FORMULA': 'if("UVOL_TotHeight"=0,0, round("UVOL_TotHeight"/3.5))',
            'INPUT': outputs['DeleteUnusefulFieldsFromUvoluedilLayer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculationOfFloorsNumber'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # Add field "Heating System"
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'Heating System',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': "'IdealLoad'",
            'INPUT': outputs['CalculationOfFloorsNumber']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddFieldHeatingSystem'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # Add field "Cooling System"
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'Cooling System',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': "'IdealLoad'",
            'INPUT': outputs['AddFieldHeatingSystem']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddFieldCoolingSystem'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}

        # Add field "ExtWallCoeff"
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ExtWallCoeff',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': '1',
            'INPUT': outputs['AddFieldCoolingSystem']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddFieldExtwallcoeff'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(48)
        if feedback.isCanceled():
            return {}

        # Add field "VolCoeff"
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'VolCoeff',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': '1',
            'INPUT': outputs['AddFieldExtwallcoeff']['OUTPUT'],
            'OUTPUT': parameters['Istatdbgtosm_joinedlayer']
        }
        outputs['AddFieldVolcoeff'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Istatdbgtosm_joinedlayer'] = outputs['AddFieldVolcoeff']['OUTPUT']

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}

        # Calculate EURECA "Envelope" class
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Envelope',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': ' GetEnvelope_2() ',
            'INPUT': outputs['AddFieldVolcoeff']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculateEurecaEnvelopeClass'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(50)
        if feedback.isCanceled():
            return {}

        # Add "Name"
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Name',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': '"UEDIL_ID"',
            'INPUT': outputs['CalculateEurecaEnvelopeClass']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddName'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(51)
        if feedback.isCanceled():
            return {}

        # Add "id"
        alg_params = {
            'FIELD_LENGTH': 5,
            'FIELD_NAME': 'id',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Intero (32 bit)
            'FORMULA': 'CASE WHEN length("Name")=7\r\nTHEN to_int(right( "Name",1))\r\nWHEN length("Name")=8\r\nTHEN to_int(right( "Name",2))\r\nELSE to_int(right( "Name",3))\r\nEND',
            'INPUT': outputs['AddName']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddId'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(52)
        if feedback.isCanceled():
            return {}

        # Rename field "ISTAT_SEZ2011" as "SEZIONE"
        alg_params = {
            'FIELD': 'ISTAT_SEZ2011',
            'INPUT': outputs['AddId']['OUTPUT'],
            'NEW_NAME': 'SEZIONE',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldIstat_sez2011AsSezione'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(53)
        if feedback.isCanceled():
            return {}

        # Rename field "UVOL_TotHeight" as "Height"
        alg_params = {
            'FIELD': 'UVOL_TotHeight',
            'INPUT': outputs['RenameFieldIstat_sez2011AsSezione']['OUTPUT'],
            'NEW_NAME': 'Height',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldUvol_totheightAsHeight'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(54)
        if feedback.isCanceled():
            return {}

        # Keep EURECA input fields
        alg_params = {
            'FIELDS': ['SEZIONE','End Use','Height','Floors','Envelope','id','Name','ExtWallCoeff','VolCoeff','Cooling System','Heating System'],
            'INPUT': outputs['RenameFieldUvol_totheightAsHeight']['OUTPUT'],
            'OUTPUT': parameters['Eureca_input']
        }
        outputs['KeepEurecaInputFields'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Eureca_input'] = outputs['KeepEurecaInputFields']['OUTPUT']
        return results

    def name(self):
        return 'modello'

    def displayName(self):
        return 'modello'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modello()
