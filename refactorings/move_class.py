import os

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
                 source_package: str = None, target_package: str = None, filename: str = None):
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

        if source_package is not None:
            directory = source_package.replace('.', '/')
            if os.path.exists(directory):
                self.source_package = source_package
            else:
                raise ValueError(f"The package \"{source_package}\" NOT FOUND!")
        else:
            raise ValueError("source_package is None")

        if target_package is not None:
            directory = target_package.replace('.', '/')
            if os.path.exists(directory):
                self.target_package = target_package
            else:
                raise ValueError(f"The package \"{target_package}\" NOT FOUND!")
        else:
            raise ValueError("target_package is None")

        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    # Enter a parse tree produced by Java9_v2Parser#packageDeclaration.
    def enterPackageDeclaration(self, ctx: Java9_v2Parser.PackageDeclarationContext):
        package_name = ctx.getText().split("package")[1].replace(';', '')
        if package_name != self.source_package:
            raise ValueError(f"The package {package_name} isn't equal to the source package!")

    # Enter a parse tree produced by Java9_v2Parser#normalClassDeclaration.
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

        start_index = ctx.start.tokenIndex
        stop_index = ctx.stop.tokenIndex

        # get the class body from the token_stream_rewriter
        class_body = self.token_stream_rewriter.getText(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            start=start_index,
            stop=stop_index
        )

        self.code = f"package {self.target_package};"
        self.code += self.NEW_LINE * 2
        self.code += f"// Class \"{self.class_identifier}\" moved here " \
                     f"from package {self.source_package} by CodART" + self.NEW_LINE + \
                     f"{class_body}"

        # delete class declaration from source class
        self.token_stream_rewriter.delete(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=start_index,
            to_idx=stop_index
        )

        old_file = open(self.filename, 'w')
        old_file.write(self.token_stream_rewriter.getDefaultText().replace("\r", ""))

        print("----------------------------")
        print("Class attributes: ", str(self.class_fields))
        print("Class methods: ", str(self.class_methods))
        print("----------------------------")

    # Enter a parse tree produced by Java9_v2Parser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx:Java9_v2Parser.FieldDeclarationContext):
        if not self.enter_class:
            return

        list_of_fields = ctx.variableDeclaratorList().getText().split(",")

        for field in list_of_fields:
            self.class_fields.append(field)

    # Enter a parse tree produced by Java9_v2Parser#methodDeclaration.
    def enterMethodDeclaration(self, ctx: Java9_v2Parser.MethodDeclarationContext):
        if not self.enter_class:
            return
        method_name = ctx.methodHeader().methodDeclarator().identifier().getText()
        self.class_methods.append(method_name)

    # Exit a parse tree produced by Java9_v2Parser#ordinaryCompilation.
    def exitOrdinaryCompilation(self, ctx: Java9_v2Parser.OrdinaryCompilationContext):
        file_address = self.target_package.replace('.', '/') + '/' + self.class_identifier + ".java"
        if self.class_number == 0:
            raise ValueError(f"Class \"{self.class_identifier}\" NOT FOUND!")

        new_file = open(file_address, 'w')
        new_file.write(self.code.replace("\r", ""))
        print(f"The class \"{self.class_identifier}\" moved to the target package.")
        print("Finished Processing...")

    # Enter a parse tree produced by Java9_v2Parser#modularCompilation.
    def exitModularCompilation(self, ctx: Java9_v2Parser.ModularCompilationContext):
        file_address = self.target_package.replace('.', '/') + '/' + self.class_identifier + ".java"
        if self.class_number == 0:
            raise ValueError(f"Class \"{self.class_identifier}\" NOT FOUND!")

        new_file = open(file_address, 'w')
        new_file.write(self.code.replace("\r", ""))
        print(f"The class \"{self.class_identifier}\" moved to the target package.")
        print("Finished Processing...")
