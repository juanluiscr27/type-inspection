import ast
import inspect
import os
from types import get_original_bases
from typing import Any, get_args

ARGUMENT_SELF = "self"
UTF_8_ENCODING = "UTF-8"


class HandlerVisitor(ast.NodeVisitor):
    def __init__(self, class_name: str) -> None:
        self._class_name = class_name
        self._match: ast.AST | None = None

    @property
    def matched_node(self) -> ast.AST | None:
        return self._match

    def visit_ClassDef(self, node: ast.AST) -> Any:
        match node:
            case ast.ClassDef(name=self._class_name):
                self._match = node

        ast.NodeVisitor.generic_visit(self, node)


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self._matches: list[str] = []

    @property
    def matches(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(self._matches))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        match node:
            case ast.FunctionDef(
                decorator_list=[ast.Attribute(value=ast.Name(id="apply"), attr="register")]
            ):
                arguments = node.args.args
                annotations = [arg.annotation for arg in arguments if arg.arg != ARGUMENT_SELF]
                handled_type = [
                    annotation.id  # type: ignore[attr-defined]
                    for annotation in annotations
                    if annotation is not None
                ]

                self._matches.extend(handled_type)

        ast.NodeVisitor.generic_visit(self, node)


def zip_type_names(module_name: str, types: tuple[str, ...]) -> list[str]:
    return [f"{module_name}.{type_name}" for type_name in types]


def get_handled_qualname(handler: type) -> list[str]:
    module_name = handler.__module__
    class_name = handler.__name__
    module_path = os.path.realpath(inspect.getfile(handler))

    with open(module_path, encoding=UTF_8_ENCODING) as file:
        code = file.read()

    module = ast.parse(code)

    handler_visitor = HandlerVisitor(class_name)
    handler_visitor.visit(module)

    handler_node = handler_visitor.matched_node

    function_visitor = FunctionVisitor()

    if handler_node is not None:
        function_visitor.visit(handler_node)

    handled_types = function_visitor.matches

    return zip_type_names(module_name, handled_types)


def get_handled_types(handler: type) -> list[str]:
    class_name = handler.__name__
    module_path = os.path.realpath(inspect.getfile(handler))

    with open(module_path, encoding=UTF_8_ENCODING) as file:
        code = file.read()

    module = ast.parse(code)

    handler_visitor = HandlerVisitor(class_name)
    handler_visitor.visit(module)

    handler_node = handler_visitor.matched_node

    function_visitor = FunctionVisitor()

    if handler_node is not None:
        function_visitor.visit(handler_node)

    handled_types = function_visitor.matches

    return list(handled_types)


def get_base_name(target: Any) -> str:
    bases = get_original_bases(target.__class__)
    args = get_args(bases[0])

    result: str = args[0].__name__
    return result


def get_base_qualname(target: Any) -> str:
    bases = get_original_bases(target.__class__)
    args = get_args(bases[0])

    module_name: str = args[0].__module__
    class_name: str = args[0].__name__

    return f"{module_name}.{class_name}"


def get_super_name(target: Any) -> str:
    bases = get_original_bases(target.__class__)
    supers = get_original_bases(bases[0])
    args = get_args(supers[0])

    result: str = args[0].__name__
    return result


def get_super_qualname(target: Any) -> str:
    bases = get_original_bases(target.__class__)
    supers = get_original_bases(bases[0])
    args = get_args(supers[0])

    module_name: str = args[0].__module__
    class_name: str = args[0].__name__

    return f"{module_name}.{class_name}"
