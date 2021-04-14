"""
Name : Convergence of Evidence Indicators
Group : 
With QGIS : 31801
Author: Federico Gianoli
Description: QGIS Processing Script to prepare the input datasets for the Convergence of Evidence Tools
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsProcessingParameterString

import processing


class CoE_Input(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # Set the input data
        self.addParameter(QgsProcessingParameterRasterLayer('InputIndicator', 'Input Indicator', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Resampled_1km', 'resampled_1Km', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterString('method', 'Resampling method', defaultValue='near', optional=True ))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}
        
        tra_extra = "-of Gtiff -co COMPRESS=DEFLATE -co PREDICTOR=2 -co ZLEVEL=9 "
        tra_extra += " -te -18041000.0 -9000000.0 18041000.0 9000000.0 "
        tra_extra += " -r " + str(parameters['method'])
        
        # Riproiezione
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': tra_extra,
            'INPUT': parameters['InputIndicator'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'SOURCE_CRS': parameters['InputIndicator'],
            'TARGET_CRS': QgsCoordinateReferenceSystem('ESRI:54009'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': QgsCoordinateReferenceSystem('ESRI:54009'),
            'TARGET_RESOLUTION': 1000,
            'OUTPUT': parameters['Resampled_1km']
        }
        outputs['Riproiezione'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Resampled_1km'] = outputs['Riproiezione']['OUTPUT']
        return results

    def name(self):
        return 'CoE_Input'

    def displayName(self):
        return 'CoE_Input'

    def group(self):
        return 'Convergence of Evidence'

    def groupId(self):
        return ''

    def createInstance(self):
        return CoE_Input()
