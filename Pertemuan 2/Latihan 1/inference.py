import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine
from knowledge import PenyakitRules

class DiagnosaPenyakit(KnowledgeEngine, PenyakitRules):
    """Mesin inferensi"""
    pass
