from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from refactorings.gen.Java9_v2Parser import Java9_v2Parser
from refactorings.gen.Java9_v2Listener import Java9_v2Listener


class MoveClassRefactoringListener(Java9_v2Listener):
    """
    To implement the move class refactoring
    a stream of tokens is sent to the listener, to build an object token_stream_rewriter
    and we move all class methods and fields from the source package to the target package
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, class_identifier: str = None,
                 source_package: str = None, target_package: str = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

        self.moved_fields = []
        self.moved_methods = []

        if class_identifier is not None:
            self.class_identifier = class_identifier
        else:
            raise ValueError("class_identifier is None")

        if source_package is not None:
            self.source_package = source_package
        else:
            raise ValueError("source_package is None")

        if target_package is not None:
            self.target_package = target_package
        else:
            raise ValueError("target_package is None")

    # Enter a parse tree produced by Java9_v2Parser#normalClassDeclaration.
    def enterNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        if ctx.identifier().getText() != self.class_identifier:
            return
        self.enter_class = True

    # Exit a parse tree produced by Java9_v2Parser#normalClassDeclaration.
    def exitNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        self.enter_class = False
        print("----------------------------")
        print("Class attributes: ", str(self.moved_fields))
        print("Class methods: ", str(self.moved_methods))
        print("----------------------------")
        self.moved_fields = []
        self.moved_methods = []

    # when exiting from a class attribute (field) declaration this method is invoked.
    # This method adds attributes of the target class to a dictionary
    def enterFieldDeclaration(self, ctx: Java9_v2Parser.FieldDeclarationContext):
        if not self.enter_class:
            return
        field_name = ctx.variableDeclaratorList().variableDeclarator(i=0).getText()
        self.moved_fields.append(field_name)
