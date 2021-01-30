from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from refactorings.gen.Java9_v2Parser import Java9_v2Parser
from refactorings.gen.Java9_v2Listener import Java9_v2Listener

class ReplaceExceptionWithTestClassRefactoringListener(Java9_v2Listener):
    def __init__(self):
        pass
    pass