"""
Model exported as python.
Name : OSM_GetEnduseData_UNICA
Group : 
With QGIS : 32812
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsExpression
import processing


class Osm_getendusedata_unica(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('r20_11_wgs84__r20_11_wgs84_studyarea', 'R20_11_WGS84 — R20_11_WGS84_StudyArea', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Osm_items', 'OSM_items', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(72, model_feedback)
        results = {}
        outputs = {}

        # Dissolve Sections
        # For faster calculation
        alg_params = {
            'FIELD': [''],
            'INPUT': parameters['r20_11_wgs84__r20_11_wgs84_studyarea'],
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DissolveSections'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Buildings
        # Get Query for building query inside the defined borders
        alg_params = {
            'EXTENT': outputs['DissolveSections']['OUTPUT'],
            'KEY': 'building',
            'SERVER': 'https://overpass-api.de/api/interpreter',
            'TIMEOUT': 25,
            'VALUE': ''
        }
        outputs['Buildings'] = processing.run('quickosm:buildqueryextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Sections Spatial Index
        # process for faster calculation
        alg_params = {
            'INPUT': parameters['r20_11_wgs84__r20_11_wgs84_studyarea']
        }
        outputs['SectionsSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Amenities
        alg_params = {
            'EXTENT': outputs['DissolveSections']['OUTPUT'],
            'KEY': 'amenity',
            'SERVER': 'https://overpass-api.de/api/interpreter',
            'TIMEOUT': 25,
            'VALUE': ''
        }
        outputs['Amenities'] = processing.run('quickosm:buildqueryextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Shop
        alg_params = {
            'EXTENT': outputs['DissolveSections']['OUTPUT'],
            'KEY': 'shop',
            'SERVER': 'https://overpass-api.de/api/interpreter',
            'TIMEOUT': 25,
            'VALUE': ''
        }
        outputs['Shop'] = processing.run('quickosm:buildqueryextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Government
        alg_params = {
            'EXTENT': outputs['DissolveSections']['OUTPUT'],
            'KEY': 'government',
            'SERVER': 'https://overpass-api.de/api/interpreter',
            'TIMEOUT': 25,
            'VALUE': ''
        }
        outputs['Government'] = processing.run('quickosm:buildqueryextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Cuisine
        alg_params = {
            'EXTENT': outputs['DissolveSections']['OUTPUT'],
            'KEY': 'cuisine',
            'SERVER': 'https://overpass-api.de/api/interpreter',
            'TIMEOUT': 25,
            'VALUE': ''
        }
        outputs['Cuisine'] = processing.run('quickosm:buildqueryextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Download buildings
        # Download the data from the query of footprints
        alg_params = {
            'DATA': '',
            'METHOD': 0,  # GET
            'URL': outputs['Buildings']['OUTPUT_URL'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DownloadBuildings'] = processing.run('native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Download amenities
        # Get Query, Download and Open Amenities
        alg_params = {
            'DATA': '',
            'METHOD': 0,  # GET
            'URL': outputs['Amenities']['OUTPUT_URL'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DownloadAmenities'] = processing.run('native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Download government
        # Get Query, Download and Open Adminstrative Offices
        alg_params = {
            'DATA': '',
            'METHOD': 0,  # GET
            'URL': outputs['Government']['OUTPUT_URL'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DownloadGovernment'] = processing.run('native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Download shop
        # Get Query, Download and Open Shops
        alg_params = {
            'DATA': '',
            'METHOD': 0,  # GET
            'URL': outputs['Shop']['OUTPUT_URL'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DownloadShop'] = processing.run('native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Open OSM shop
        alg_params = {
            'FILE': outputs['DownloadShop']['OUTPUT'],
            'OSM_CONF': ''
        }
        outputs['OpenOsmShop'] = processing.run('quickosm:openosmfile', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Exp_shop
        # Change "Other fields" attribute to real fields
        alg_params = {
            'EXPECTED_FIELDS': '',
            'FIELD': 'other_tags',
            'INPUT': outputs['OpenOsmShop']['OUTPUT_POINTS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Exp_shop'] = processing.run('native:explodehstorefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Open OSM amenities
        alg_params = {
            'FILE': outputs['DownloadAmenities']['OUTPUT'],
            'OSM_CONF': ''
        }
        outputs['OpenOsmAmenities'] = processing.run('quickosm:openosmfile', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # amen_pg
        # divide osm data into polygons and points
        alg_params = {
            'FIELDS': ['amenity'],
            'INPUT': outputs['OpenOsmAmenities']['OUTPUT_MULTIPOLYGONS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Amen_pg'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Download cuisine
        # Get Query, Download and Open Cuisine
        alg_params = {
            'DATA': '',
            'METHOD': 0,  # GET
            'URL': outputs['Cuisine']['OUTPUT_URL'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DownloadCuisine'] = processing.run('native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Centroids shop
        # Change polygons into points to ease calculation
        alg_params = {
            'ALL_PARTS': True,
            'INPUT': outputs['OpenOsmShop']['OUTPUT_MULTIPOLYGONS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CentroidsShop'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Exp_amenity
        # Change "Other fields" attribute to real fields
        alg_params = {
            'EXPECTED_FIELDS': '',
            'FIELD': 'other_tags',
            'INPUT': outputs['OpenOsmAmenities']['OUTPUT_POINTS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Exp_amenity'] = processing.run('native:explodehstorefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Open OSM buildings
        # Open the downloaded data
        alg_params = {
            'FILE': outputs['DownloadBuildings']['OUTPUT'],
            'OSM_CONF': ''
        }
        outputs['OpenOsmBuildings'] = processing.run('quickosm:openosmfile', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Refine Buildings
        # Remove data (small footprints, huts and roofs)
        # 
        alg_params = {
            'EXPRESSION': '$area < 70 OR "building"=\'roof\' OR "building"=\'hut\' OR "building"=\'shed\' OR "building" is NULL',
            'INPUT': outputs['OpenOsmBuildings']['OUTPUT_MULTIPOLYGONS'],
            'FAIL_OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefineBuildings'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Open OSM cuisine
        alg_params = {
            'FILE': outputs['DownloadCuisine']['OUTPUT'],
            'OSM_CONF': ''
        }
        outputs['OpenOsmCuisine'] = processing.run('quickosm:openosmfile', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Open OSM government
        alg_params = {
            'FILE': outputs['DownloadGovernment']['OUTPUT'],
            'OSM_CONF': ''
        }
        outputs['OpenOsmGovernment'] = processing.run('quickosm:openosmfile', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Refined_Spatial
        # process for faster calculation
        alg_params = {
            'INPUT': outputs['RefineBuildings']['FAIL_OUTPUT']
        }
        outputs['Refined_spatial'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Centroids cuisine
        # Change polygons into points to ease calculation
        alg_params = {
            'ALL_PARTS': True,
            'INPUT': outputs['OpenOsmCuisine']['OUTPUT_MULTIPOLYGONS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CentroidsCuisine'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Buffer pt shop
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression('@buff_dist').evaluate(),
            'END_CAP_STYLE': 0,  # Arrotondato
            'INPUT': outputs['Exp_shop']['OUTPUT'],
            'JOIN_STYLE': 1,  # Seghettato
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferPtShop'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Centroids government
        # Change polygons into points to ease calculation
        alg_params = {
            'ALL_PARTS': True,
            'INPUT': outputs['OpenOsmGovernment']['OUTPUT_MULTIPOLYGONS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CentroidsGovernment'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Shop Pt Spatial Index
        alg_params = {
            'INPUT': outputs['BufferPtShop']['OUTPUT']
        }
        outputs['ShopPtSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Buffer plg gov
        # change points to polygons so they can be spatially indexed
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression('@buff_dist').evaluate(),
            'END_CAP_STYLE': 0,  # Arrotondato
            'INPUT': outputs['CentroidsGovernment']['OUTPUT'],
            'JOIN_STYLE': 1,  # Seghettato
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferPlgGov'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Amenities Plg Spatial Index
        # Faster calculation
        alg_params = {
            'INPUT': outputs['Amen_pg']['OUTPUT']
        }
        outputs['AmenitiesPlgSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Buffer pt amenities
        # change points to polygons so they can be spatially indexed
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression('@buff_dist').evaluate(),
            'END_CAP_STYLE': 0,  # Arrotondato
            'INPUT': outputs['Exp_amenity']['OUTPUT'],
            'JOIN_STYLE': 1,  # Seghettato
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferPtAmenities'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Gov  Plg Spatial Index
        # Faster Calculation
        alg_params = {
            'INPUT': outputs['BufferPlgGov']['OUTPUT']
        }
        outputs['GovPlgSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Buffer plg shop
        # change points to polygons so they can be spatially indexed
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression('@buff_dist').evaluate(),
            'END_CAP_STYLE': 0,  # Arrotondato
            'INPUT': outputs['CentroidsShop']['OUTPUT'],
            'JOIN_STYLE': 1,  # Seghettato
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferPlgShop'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Exp_cuisine
        # Change "Other fields" attribute to real fields
        alg_params = {
            'EXPECTED_FIELDS': '',
            'FIELD': 'other_tags',
            'INPUT': outputs['OpenOsmCuisine']['OUTPUT_POINTS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Exp_cuisine'] = processing.run('native:explodehstorefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Exp_gov
        # Change "Other fields" attribute to real fields
        alg_params = {
            'EXPECTED_FIELDS': '',
            'FIELD': 'other_tags',
            'INPUT': outputs['OpenOsmGovernment']['OUTPUT_POINTS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Exp_gov'] = processing.run('native:explodehstorefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Buffer plg cuisine
        # change points to polygons so they can be spatially indexed
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression('@buff_dist').evaluate(),
            'END_CAP_STYLE': 0,  # Arrotondato
            'INPUT': outputs['CentroidsCuisine']['OUTPUT'],
            'JOIN_STYLE': 1,  # Seghettato
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferPlgCuisine'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Clip buildings
        # clip the downloaded data inside the borders
        alg_params = {
            'INPUT': outputs['Refined_spatial']['OUTPUT'],
            'OVERLAY': outputs['DissolveSections']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClipBuildings'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Amenities Pt Spatial Index
        # Faster Calculation
        alg_params = {
            'INPUT': outputs['BufferPtAmenities']['OUTPUT']
        }
        outputs['AmenitiesPtSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Shop Plg Spatial Index
        # Faster Calculation
        alg_params = {
            'INPUT': outputs['BufferPlgShop']['OUTPUT']
        }
        outputs['ShopPlgSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Buffer pt cuisine
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression('@buff_dist').evaluate(),
            'END_CAP_STYLE': 0,  # Arrotondato
            'INPUT': outputs['Exp_cuisine']['OUTPUT'],
            'JOIN_STYLE': 1,  # Seghettato
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferPtCuisine'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # MtS1
        # make single parts from the data
        alg_params = {
            'INPUT': outputs['ClipBuildings']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Mts1'] = processing.run('native:multiparttosingleparts', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Spatial_buildings
        # process for faster calculation
        alg_params = {
            'INPUT': outputs['Mts1']['OUTPUT']
        }
        outputs['Spatial_buildings'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Buffer pt gov
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression('@buff_dist').evaluate(),
            'END_CAP_STYLE': 0,  # Arrotondato
            'INPUT': outputs['Exp_gov']['OUTPUT'],
            'JOIN_STYLE': 1,  # Seghettato
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferPtGov'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # Cuisine Plg Spatial Index
        # Faster Calculation
        alg_params = {
            'INPUT': outputs['BufferPlgCuisine']['OUTPUT']
        }
        outputs['CuisinePlgSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}

        # Cuisine Pt Spatial Index
        alg_params = {
            'INPUT': outputs['BufferPtCuisine']['OUTPUT']
        }
        outputs['CuisinePtSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # Gov  Pt Spatial Index
        alg_params = {
            'INPUT': outputs['BufferPtGov']['OUTPUT']
        }
        outputs['GovPtSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # Union Amenities
        # Unite data from polygons and points
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['AmenitiesPlgSpatialIndex']['OUTPUT'],
            'OVERLAY': outputs['AmenitiesPtSpatialIndex']['OUTPUT'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnionAmenities'] = processing.run('native:union', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # Insides
        # remove the data that are showing the yards but are mistaken for the buildings
        alg_params = {
            'EXPRESSION': 'overlay_contains(layer:=  @MtS1_OUTPUT  )',
            'INPUT': outputs['Spatial_buildings']['OUTPUT'],
            'FAIL_OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Insides'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}

        # Union cuisine
        # Unite data from polygons and points
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['CuisinePlgSpatialIndex']['OUTPUT'],
            'OVERLAY': outputs['CuisinePtSpatialIndex']['OUTPUT'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnionCuisine'] = processing.run('native:union', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(48)
        if feedback.isCanceled():
            return {}

        # Union shop
        # Unite data from polygons and points
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['ShopPtSpatialIndex']['OUTPUT'],
            'OVERLAY': outputs['ShopPlgSpatialIndex']['OUTPUT'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnionShop'] = processing.run('native:union', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}

        # Union goverment
        # Unite data from polygons and points
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['GovPtSpatialIndex']['OUTPUT'],
            'OVERLAY': outputs['GovPlgSpatialIndex']['OUTPUT'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnionGoverment'] = processing.run('native:union', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(50)
        if feedback.isCanceled():
            return {}

        # cuisinecalc
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'enduse_food',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': 'if("cuisine" is NULL, "cuisine_2","cuisine")',
            'INPUT': outputs['UnionCuisine']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Cuisinecalc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(51)
        if feedback.isCanceled():
            return {}

        # shopcalc
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'enduse_shop',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': 'if("shop" is NULL, "shop_2","shop")',
            'INPUT': outputs['UnionShop']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Shopcalc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(52)
        if feedback.isCanceled():
            return {}

        # Government Spatial Index
        # Faster calculation
        alg_params = {
            'INPUT': outputs['Shopcalc']['OUTPUT']
        }
        outputs['GovernmentSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(53)
        if feedback.isCanceled():
            return {}

        # Shop Spatial Index
        # Faster calculation
        alg_params = {
            'INPUT': outputs['Shopcalc']['OUTPUT']
        }
        outputs['ShopSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(54)
        if feedback.isCanceled():
            return {}

        # amenitycalc
        # Unite data from polygons and points
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'ENDUSE00',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': 'if("amenity" is NULL, "amenity_2","amenity")',
            'INPUT': outputs['UnionAmenities']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Amenitycalc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(55)
        if feedback.isCanceled():
            return {}

        # Cuisine Spatial Index
        # Faster calculation
        alg_params = {
            'INPUT': outputs['Cuisinecalc']['OUTPUT']
        }
        outputs['CuisineSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(56)
        if feedback.isCanceled():
            return {}

        # Spatial_around
        # process for faster calculations
        alg_params = {
            'INPUT': outputs['Insides']['FAIL_OUTPUT']
        }
        outputs['Spatial_around'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(57)
        if feedback.isCanceled():
            return {}

        # amenityfilter
        # FILTERS USEFUL AMENITIES
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'enduse_amenity',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': ' AmenFilter() ',
            'INPUT': outputs['UnionAmenities']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Amenityfilter'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(58)
        if feedback.isCanceled():
            return {}

        # govcalc
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'enduse_gov',
            'FIELD_PRECISION': 1,
            'FIELD_TYPE': 2,  # Testo (stringa)
            'FORMULA': 'if("government" is NULL, "government_2","government")',
            'INPUT': outputs['UnionGoverment']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Govcalc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(59)
        if feedback.isCanceled():
            return {}

        # Amenities Spatial Index
        # Faster calculation
        alg_params = {
            'INPUT': outputs['Amenityfilter']['OUTPUT']
        }
        outputs['AmenitiesSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(60)
        if feedback.isCanceled():
            return {}

        # Merge vector layers
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['ShopSpatialIndex']['OUTPUT'],outputs['GovernmentSpatialIndex']['OUTPUT'],outputs['AmenitiesSpatialIndex']['OUTPUT'],outputs['CuisineSpatialIndex']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeVectorLayers'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(61)
        if feedback.isCanceled():
            return {}

        # Retain fields
        alg_params = {
            'FIELDS': ['enduse_amenity','enduse_shop','enduse_food','enduse_gov'],
            'INPUT': outputs['MergeVectorLayers']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RetainFields'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(62)
        if feedback.isCanceled():
            return {}

        # CleanB1
        # remove duplicate geometries
        alg_params = {
            'INPUT': outputs['Spatial_around']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Cleanb1'] = processing.run('native:deleteduplicategeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(63)
        if feedback.isCanceled():
            return {}

        # OSM building ID
        # give an id to each building
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'OSM_ID',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,  # Decimale (doppia precisione)
            'FORMULA': 'if("osm_id" is NULL, "osm_way_id","osm_id")',
            'INPUT': outputs['Cleanb1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OsmBuildingId'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(64)
        if feedback.isCanceled():
            return {}

        # Retained spatial index
        alg_params = {
            'INPUT': outputs['RetainFields']['OUTPUT']
        }
        outputs['RetainedSpatialIndex'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(65)
        if feedback.isCanceled():
            return {}

        # Rename field 'building'
        # Rename field 'building' as 'OSM_building'
        alg_params = {
            'FIELD': 'building',
            'INPUT': outputs['OsmBuildingId']['OUTPUT'],
            'NEW_NAME': 'OSM_building',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldBuilding'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(66)
        if feedback.isCanceled():
            return {}

        # FieldsOSM
        # retain useful fields
        alg_params = {
            'FIELDS': ['OSM_ID','OSM_building'],
            'INPUT': outputs['RenameFieldBuilding']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Fieldsosm'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(67)
        if feedback.isCanceled():
            return {}

        # Multipart to singleparts
        alg_params = {
            'INPUT': outputs['RetainedSpatialIndex']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MultipartToSingleparts'] = processing.run('native:multiparttosingleparts', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(68)
        if feedback.isCanceled():
            return {}

        # Join OSM buildings with Amenities
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Fieldsosm']['OUTPUT'],
            'JOIN': outputs['MultipartToSingleparts']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 2,  # Prendi solamente gli attributi dell'elemento con maggiore sovrapposizione (uno-a-uno)
            'PREDICATE': [0],  # interseca
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinOsmBuildingsWithAmenities'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(69)
        if feedback.isCanceled():
            return {}

        # Rename field 'enduse_amenity'
        # Rename field 'enduse_amenity' as 'OSM_amenity'
        alg_params = {
            'FIELD': 'enduse_amenity',
            'INPUT': outputs['JoinOsmBuildingsWithAmenities']['OUTPUT'],
            'NEW_NAME': 'OSM_amenity',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldEnduse_amenity'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(70)
        if feedback.isCanceled():
            return {}

        # Rename field 'enduse_shop'
        # Rename field 'enduse_shop' as 'OSM_shop'
        alg_params = {
            'FIELD': 'enduse_shop',
            'INPUT': outputs['RenameFieldEnduse_amenity']['OUTPUT'],
            'NEW_NAME': 'OSM_shop',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameFieldEnduse_shop'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(71)
        if feedback.isCanceled():
            return {}

        # Rename field 'enduse_food'
        # Rename field 'enduse_food' as 'OSM_food'
        alg_params = {
            'FIELD': 'enduse_food',
            'INPUT': outputs['RenameFieldEnduse_shop']['OUTPUT'],
            'NEW_NAME': 'OSM_food',
            'OUTPUT': parameters['Osm_items']
        }
        outputs['RenameFieldEnduse_food'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Osm_items'] = outputs['RenameFieldEnduse_food']['OUTPUT']
        return results

    def name(self):
        return 'OSM_GetEnduseData_UNICA'

    def displayName(self):
        return 'OSM_GetEnduseData_UNICA'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Osm_getendusedata_unica()
