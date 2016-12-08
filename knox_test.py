import pysal
import numpy as np
import processing
from processing.tools.vector import VectorWriter
from qgis.core import *
from PyQt4.QtCore import *
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import *
from processing.core.outputs import *
from processing.tools import dataobjects
from PyQt4 import QtGui
from qgis.utils import iface
from pysal.spatial_dynamics.interaction import knox
import pysal.spatial_dynamics.interaction as interaction
np.random.seed(100)

class KnoxTest(GeoAlgorithm):

    INPUT = 'INPUT'
    FIELD = 'FIELD'
    OUTPUT = 'OUTPUT'
    P_SIM = 'P_SIM'
    TIME = 'TIME'
    S_COORDS = 'S_COORDS'
    T_COORDS = 'T_COORDS'
    DELTA = 'DELTA'
    TAU = 'TAU'

    def defineCharacteristics(self):
        self.name = "Knox Test"
        self.group = 'Spatial Dynamics'

        ##input=vector
        ##field=field input
        ##p_sim=output string

		### Here we add parameters from an input layer directory
        self.addParameter(ParameterVector(self.INPUT,
            self.tr('Input layer directory'), [ParameterVector.VECTOR_TYPE_POLYGON]))
        self.addParameter(ParameterTableField(self.FIELD,
            self.tr('Space Coordinate X'), self.INPUT))        
		self.addParameter(ParameterTableField(self.FIELD,
            self.tr('Space Coordinate Y'), self.INPUT))
        self.addParameter(ParameterTableField(self.FIELD,
            self.tr('Time Field'), self.INPUT))

			
		### Here we declare the outpiuts
        self.addOutput(OutputVector(self.OUTPUT, self.tr('Result')))
        self.addOutput(OutputString(self.P_SIM, self.tr('p_sim')))

    def processAlgorithm(self, progress):

        field = self.getParameterValue(self.FIELD)
        field = field[0:10] # try to handle Shapefile field length limit
        filename = self.getParameterValue(self.INPUT)
        layer = dataobjects.getObjectFromUri(filename)
        filename = dataobjects.exportVectorLayer(layer)
        provider = layer.dataProvider()
		
		### Input for attribute table fields 
        fields = provider.fields()
        fields.append(QgsField('STAT', QVariant.Float))
        fields.append(QgsField('PVALUE', QVariant.Float))
        fields.append(QgsField('COUNTS', QVariant.Int))
		
        writer = self.getOutputFromName(self.OUTPUT).getVectorWriter(
            fields, provider.geometryType(), layer.crs() )

		events = interaction.SpaceTimeEvents(self.INPUT,'T')

        f = pysal.open(filename.replace('.shp','.dbf'))
        y=np.array(f.by_col[str(field)])
        kt = interaction.knox(events.space, events.t, delta=20, tau=5, permutations=99)

        self.setOutputValue(self.P_SIM, str(kt.p_sim))

		outFeat = QgsFeature()
        i = 0
        for inFeat in processing.features(layer):
            inGeom = inFeat.geometry()
            outFeat.setGeometry(inGeom)
            attrs = inFeat.attributes()
            attrs.append(float(kt.p_sim[i]))
            outFeat.setAttributes(attrs)
            writer.addFeature(outFeat)
            i+=1

        del writer

		print(kt['stat'])
		print("%2.2f"%kt['pvalue'])
