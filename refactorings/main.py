import argparse
import os

from antlr4 import *

from refactorings.extract_class import ExtractClassRecognizerListener, ExtractClassRefactoringListener
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

extensions = []
implementations = []
source_class = 'A'
moved_fields = ['h']
moved_methods = ['printH']
f_iteration_flag = False


def main(args):
    global extensions
    global implementations

    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # Step 2: Create an instance of AssignmentStLexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()
    # Step 6: Create an instance of AssignmentStListener
    if f_iteration_flag:
        recognizer_listener = ExtractClassRecognizerListener(common_token_stream=token_stream, class_identifier='A')
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=recognizer_listener)

        component = sorted(moved_methods + moved_fields)
        if component in sorted(recognizer_listener.connected_components):
            my_listener = ExtractClassRefactoringListener(
                common_token_stream=token_stream, source_class='A', new_class='ANew',
                moved_methods=moved_methods, moved_fields=moved_fields, filename=args.file
            )
            walker.walk(t=parse_tree, listener=my_listener)

            with open(args.file, mode='w', newline='') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText())
        else:
            raise ValueError("Can not refactor!")


def recursive_walk(directory):
    for dirname, dirs, files in os.walk(directory):
        for filename in files:
            if filename != source_class:
                continue
            f_iteration_flag = True
            filename_without_extension, extension = os.path.splitext(filename)
            if extension == '.java':
                process_file("{}/{}".format(dirname, filename))


def process_file(file):
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=file)

    args = argparser.parse_args()
    main(args)


if __name__ == '__main__':
    directory = '../Chess/src'
    recursive_walk(directory)
