import os

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from refactorings.gen.Java9_v2Parser import Java9_v2Parser
from refactorings.gen.Java9_v2Listener import Java9_v2Listener


class RemoveFieldRefactoringListener(Java9_v2Listener):
    def __init__(self, common_token_stream: CommonTokenStream = None, class_identifier: str = None,
                 fieldname: str = None, filename: str = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        self.class_number = 0

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

        self.class_fields = []
        self.class_methods = []

        if class_identifier is not None:
            self.class_identifier = class_identifier
        else:
            raise ValueError("class_identifier is None")

        if filename is not None:
            self.filename = filename
        else:
            raise ValueError("filename is None")

        if fieldname is not None:
            self.fieldname = fieldname
        else:
            raise ValueError("fieldname is None")

    def enterNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        print("Refactoring started, please wait...")
        self.class_number += 1
        if ctx.identifier().getText() != self.class_identifier:
            return
        self.enter_class = True

    # Exit a parse tree produced by Java9_v2Parser#normalClassDeclaration.
    def exitNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        self.enter_class = False
        if ctx.identifier().getText() != self.class_identifier:
            return

        old_file = open(self.filename, 'w')
        old_file.write(self.token_stream_rewriter.getDefaultText().replace("\r", ""))

        # print("----------------------------")
        # print("Class attributes: ", str(self.class_fields))
        # print("Class methods: ", str(self.class_methods))
        # print("----------------------------")

    # Enter a parse tree produced by Java9_v2Parser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx: Java9_v2Parser.FieldDeclarationContext):
        if not self.enter_class:
            return

        list_of_fields = ctx.variableDeclaratorList().getText().split(",")

        for field in list_of_fields:
            self.class_fields.append(field)
