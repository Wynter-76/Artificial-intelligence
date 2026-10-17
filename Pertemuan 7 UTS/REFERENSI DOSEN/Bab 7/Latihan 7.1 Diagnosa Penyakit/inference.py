import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine
from knowledge import PenyakitRules


class DiagnosaPenyakit(KnowledgeEngine, PenyakitRules):

    def __init__(self):
        super().__init__()
        self.hasil = []