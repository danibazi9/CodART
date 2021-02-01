import os

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MoveClassRefactoringListener(JavaParserLabeledListener):
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
        self.class_found = False

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

    # Enter a parse tree produced by JavaParserLabeled#packageDeclaration.
    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        package_name = ctx.getText().split("package")[1].replace(';', '')
        if package_name != self.source_package:
            raise ValueError(f"The package {package_name} isn't equal to the source package!")

    # Exit a parse tree produced by JavaParserLabeled#importDeclaration.
    def exitImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if ctx.qualifiedName().getText() != self.source_package + '.' + self.class_identifier:
            return

        start_index = ctx.start.tokenIndex
        stop_index = ctx.stop.tokenIndex

        text_to_replace = "import " + self.target_package + '.' + self.class_identifier + ';'
        if ctx.STATIC() is not None:
            text_to_replace = text_to_replace.replace("import", "import static")

        # replace the import source package with target package
        self.token_stream_rewriter.replace(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=start_index,
            to_idx=stop_index,
            text=text_to_replace
        )

    # Enter a parse tree produced by JavaParserLabeled#classDeclaration.
    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.enter_class = False
        if ctx.IDENTIFIER().getText() != self.class_identifier:
            return

        self.class_found = True

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

    # Enter a parse tree produced by JavaParserLabeled#fieldDeclaration.
    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if not self.enter_class:
            return

        list_of_fields = ctx.variableDeclarators().getText().split(",")

        for field in list_of_fields:
            self.class_fields.append(field)

    # Enter a parse tree produced by JavaParserLabeled#methodDeclaration.
    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.enter_class:
            return
        method_name = ctx.IDENTIFIER().getText()
        self.class_methods.append(method_name)

    # Exit a parse tree produced by JavaParserLabeled#compilationUnit.
    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        file_address = self.target_package.replace('.', '/') + '/' + self.class_identifier + ".java"
        if not self.class_found:
            raise ValueError(f"Class \"{self.class_identifier}\" NOT FOUND!")

        new_file = open(file_address, 'w')
        new_file.write(self.code.replace("\r", ""))
        print(f"The class \"{self.class_identifier}\" moved to the target package.")
        print("Finished Processing...")
