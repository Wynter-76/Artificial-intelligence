import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine
from knowledge import PadiRules

class DiagnosaPadi(KnowledgeEngine,
                     PadiRules):
    """Mesin Inferensi"""
    pass