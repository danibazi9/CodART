from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from refactorings.gen.Java9_v2Parser import Java9_v2Parser
from refactorings.gen.Java9_v2Listener import Java9_v2Listener

class ReplaceExceptionWithTestClassRefactoringListener(Java9_v2Listener):
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None, filename: str = None):
        self.IOOBE = False # IndexOutOfBoundException
        self.ASE = False # ArrayStoreException
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier

        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

        if class_identifier is not None:
            self.class_identifier = class_identifier
        else:
            raise ValueError("class_identifier is None")

        if filename is not None:
            self.filename = filename
        else:
            raise ValueError("filename is None")


    def enterTryStatement1(self, ctx:Java9_v2Parser.TryStatement1Context):
        print("'enterTryStatement1'")
        pass

    def exitTryStatement1(self, ctx:Java9_v2Parser.TryStatement1Context):
        print("'exitTryStatement1'")
        pass

    def enterTryStatement2(self, ctx:Java9_v2Parser.TryStatement2Context):
        print("'enterTryStatement2'")
        pass

    def exitTryStatement2(self, ctx:Java9_v2Parser.TryStatement2Context):
        catches = ctx.catches();
        # temp0 = ctx.catches().catchClause(0).catchFormalParameter().catchType().unannClassType().getText()
        for catch in catches.catchClause():
            exception  = catch.catchFormalParameter().catchType().unannClassType().getText()
            if (exception == "IndexOutOfBoundsException"):
                print("IndexOutOfBoundsException")
                self.IOOBE = True
            if (exception == "ArrayStoreException"):
                print("ArrayStoreException")
                self.ASE = True
            # print(catch.catchFormalParameter().catchType().unannClassType().getText())
        # print(temp0)
        # print(temp1)

        print("'exitTryStatement2'")
        pass

    def enterTryStatement3(self, ctx:Java9_v2Parser.TryStatement3Context):
        print("'enterTryStatement3'")
        pass

    def exitTryStatement3(self, ctx:Java9_v2Parser.TryStatement3Context):
        print("'exitTryStatement3'")
        pass

# ====================================================================================================
    def enterArrayAccess(self, ctx:Java9_v2Parser.ArrayAccessContext):
        print("'enterArrayAccess'")

    def exitArrayAccess(self, ctx:Java9_v2Parser.ArrayAccessContext):
        # if not self.IOOBE:
        #     return
        print(f"ArrayName: {ctx.expressionName().identifier().getText()}; ArrayIndex: {ctx.expression(0).getText()};")
        print("'exitArrayAccess'")

    def enterArrayAccess_lfno_primary(self, ctx:Java9_v2Parser.ArrayAccess_lfno_primaryContext):
        print("'enterArrayAccess_lfno_primary'")

    def exitArrayAccess_lfno_primary(self, ctx:Java9_v2Parser.ArrayAccess_lfno_primaryContext):
        print(f"ArrayName: {ctx.expressionName().identifier().getText()}; ArrayIndex: {ctx.expression(0).getText()};")
        print("'exitArrayAccess_lfno_primary'")


# ====================================================================================================

    pass