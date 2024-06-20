import ast
import inspect
import os
from types import get_original_bases
from typing import List, Optional, Tuple, get_args


class HandlerVisitor(ast.NodeVisitor):

    def __init__(self, class_name: str):
        self._class_name = class_name
        self._match: Optional[ast.AST] = None

    @property
    def matched_node(self):
        return self._match

    def visit_ClassDef(self, node: ast.AST):
        match node:
            case ast.ClassDef(name=self._class_name):
                self._match = node

        ast.NodeVisitor.generic_visit(self, node)


class FunctionVisitor(ast.NodeVisitor):

    def __init__(self):
        self._matches: List[str] = []

    @property
    def matches(self):
        return tuple(dict.fromkeys(self._matches))

    def visit_FunctionDef(self, node: ast.FunctionDef):
        match node:
            case ast.FunctionDef(
                decorator_list=[
                    ast.Attribute(value=ast.Name(id="apply"), attr="register")
                ]
            ):
                arguments = node.args.args
                annotations = [arg.annotation for arg in arguments if arg != "self"]
                # noinspection PyUnresolvedReferences
                handled_type = [
                    annotation.id
                    for annotation in annotations
                    if annotation is not None
                ]

                self._matches.extend(handled_type)

        ast.NodeVisitor.generic_visit(self, node)


def _get_abs_path(module_name: str):
    rel_path = "/".join(module_name.split("."))
    file_path = f"{rel_path}.py"

    return os.path.abspath(file_path)


def zip_type_names(module_name: str, types: Tuple[str, ...]):
    return [f"{module_name}.{type_name}" for type_name in types]


def getfull_handledtypes(handler):
    module_name = handler.__module__
    class_name = handler.__name__
    module_path = _get_abs_path(module_name)

    with open(module_path, encoding="UTF-8") as file:
        code = file.read()

    module = ast.parse(code)

    handler_visitor = HandlerVisitor(class_name)
    handler_visitor.visit(module)

    handler_node = handler_visitor.matched_node

    function_visitor = FunctionVisitor()

    function_visitor.visit(handler_node)

    handled_types = function_visitor.matches

    return zip_type_names(module_name, handled_types)


def gethandledtypes(handler):
    class_name = handler.__name__
    module_path = os.path.realpath(inspect.getfile(handler))

    with open(module_path, encoding="UTF-8") as file:
        code = file.read()

    module = ast.parse(code)

    handler_visitor = HandlerVisitor(class_name)
    handler_visitor.visit(module)

    handler_node = handler_visitor.matched_node

    function_visitor = FunctionVisitor()

    function_visitor.visit(handler_node)

    handled_types = function_visitor.matches

    return list(handled_types)


def get_base_name(target):
    bases = get_original_bases(target.__class__)
    args = get_args(bases[0])

    return args[0].__name__


def get_base_type(target):
    bases = get_original_bases(target.__class__)
    args = get_args(bases[0])

    module_name = args[0].__module__
    class_name = args[0].__name__

    return f"{module_name}.{class_name}"


def get_super_name(target):
    bases = get_original_bases(target.__class__)
    supers = get_original_bases(bases[0])
    args = get_args(supers[0])

    return args[0].__name__


def get_super_type(target):
    bases = get_original_bases(target.__class__)
    supers = get_original_bases(bases[0])
    args = get_args(supers[0])

    module_name = args[0].__module__
    class_name = args[0].__name__

    return f"{module_name}.{class_name}"
