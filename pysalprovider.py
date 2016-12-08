from processing.core.AlgorithmProvider import AlgorithmProvider
from moran import Moran
from moranrate import MoranRate
from moranlocal import MoranLocal
from moranlocalrate import MoranLocalRate
from knox_test import KnoxTest
from modifiedknox_test import ModifiedKnoxTest
from mantel_test import MantelTest
from jacquez_test import JacquezTest

class pysalProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)

        self.activate = False

        self.alglist = [Moran(),MoranRate(), KnoxTest(), ModifiedKnoxTest(),
                        MantelTest(), JacquezTest(), MoranLocal(),MoranLocalRate()]
        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)

    def unload(self):
        AlgorithmProvider.unload(self)

    def getName(self):
        return 'pysal'

    def getDescription(self):
        return 'PySAL'

    def _loadAlgorithms(self):
        self.algs = self.alglist
