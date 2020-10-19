#!/usr/bin/env python3
#
#  __init__.py
"""
A flake8 plugin which checks for use of platform specific sphinx_links codes.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on flake8_2020
#  Copyright (c) 2019 Anthony Sottile
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#

# stdlib
import ast
import platform
import re
import sys
from typing import Any, Dict, Generator, List, Pattern, Tuple, Type, Union

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT"
__version__: str = "0.1.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = [
		"SXL001",
		"Visitor",
		"Plugin",
		"py_obj",
		"py_obj_python",
		"exc",
		"class_",
		"regex",
		]

SXL001: str = "SXL001 Double backticked strings should be a link to Python documentation."  # noqa: E501

#: List of keywords that should become :file:`:py:obj:\`{<keyword>}\``
py_obj: List[str] = [
		"True",
		"False",
		"None",
		"NotImplemented",
		"Ellipsis",
		"__debug__",
		"quit",
		"exit",
		"credits",
		"license",
		]

py_obj_python: List[str] = ["copyright"]
"""
List of keywords that should become :file:`:py:obj:\`python:{<keyword>}\``
to prevent conflict with Sphinx objects.
"""

#: List of keywords that should become :file:`:py:exc:\`{<keyword>}\``
exc: List[str] = [
		"BaseException",
		"Exception",
		"ArithmeticError",
		"BufferError",
		"LookupError",
		"AssertionError",
		"AttributeError",
		"EOFError",
		"FloatingPointError",
		"GeneratorExit",
		"ImportError",
		"ModuleNotFoundError",
		"IndexError",
		"KeyError",
		"KeyboardInterrupt",
		"MemoryError",
		"NameError",
		"NotImplementedError",
		"OSError",
		"OverflowError",
		"RecursionError",
		"ReferenceError",
		"RuntimeError",
		"StopIteration",
		"StopAsyncIteration",
		"SyntaxError",
		"IndentationError",
		"TabError",
		"SyntaxError",
		"IndentationError",
		"TabError",
		"SystemError",
		"SystemExit",
		"TypeError",
		"UnboundLocalError",
		"UnicodeError",
		"UnicodeEncodeError",
		"UnicodeDecodeError",
		"UnicodeTranslateError",
		"ValueError",
		"ZeroDivisionError",
		"EnvironmentError",
		"IOError",
		"WindowsError",
		"BlockingIOError",
		"ChildProcessError",
		"ConnectionError",
		"BrokenPipeError",
		"ConnectionAbortedError",
		"ConnectionRefusedError",
		"ConnectionResetError",
		"FileExistsError",
		"FileNotFoundError",
		"InterruptedError",
		"IsADirectoryError",
		"NotADirectoryError",
		"PermissionError",
		"ProcessLookupError",
		"TimeoutError",
		"Warning",
		"UserWarning",
		"DeprecationWarning",
		"PendingDeprecationWarning",
		"SyntaxWarning",
		"RuntimeWarning",
		"FutureWarning",
		"ImportWarning",
		"UnicodeWarning",
		"BytesWarning",
		"ResourceWarning",
		]

class_: List[str] = [
		"int",
		"float",
		"complex",
		"list",
		"tuple",
		"range",
		"str",
		"bytes",
		"bytearray",
		"memoryview",
		"set",
		"frozenset",
		"dict",
		]

# TODO: Check for wrong links too

all_objs: str = '|'.join(py_obj + py_obj_python + exc + class_)

#: Regex to match keywords that should be Sphinx links.
regex: Pattern = re.compile(fr"(``)({all_objs})(``)")


class Visitor(ast.NodeVisitor):
	"""
	Class to traverse an Abstract Syntax Tree (AST), extract docstrings and check them.
	"""

	def __init__(self) -> None:
		"""
		Initialise the AST NodeVisitor.
		"""

		self.errors: List[Tuple[int, int, str]] = []
		self._from_imports: Dict[str, str] = {}

	def _check_docstring(self, node: Union[ast.ClassDef, ast.FunctionDef, ast.Module]) -> None:
		docstring = ast.get_docstring(node, clean=False)

		if docstring:

			split_docstring = docstring.splitlines()
			doc_line_length = len(split_docstring)
			# print(f"|{docstring}|")

			# Special casing for docstrings where the final line doesn't have indentation.
			# (Usually module docstring)
			if not re.match(r"^\s+$", split_docstring[-1]):
				doc_line_length += 1

			if (
					sys.version_info < (3, 8) and platform.python_implementation() != "PyPy"
					):  # pragma: no cover (>=PY38)
				doc_end_lineno = node.body[0].value.lineno  # type: ignore

				# Calculate the start line
				doc_start_lineno = doc_end_lineno - doc_line_length

				# If docstring is only a single line the start_lineno is 1 less than the end_lineno.
				# (-1 because docutils start counting at 1)
				if len(split_docstring) == 1:
					doc_start_lineno = doc_end_lineno - 1

				doc_start_lineno += 1

			else:  # pragma: no cover (<PY38)
				doc_start_lineno = node.body[0].value.lineno  # type: ignore

			for offset, line in enumerate(docstring.splitlines()):

				for match in regex.finditer(line):
					self.errors.append((
							doc_start_lineno + offset,
							match.span()[0],
							SXL001,
							))

	def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
		"""Check the docstring of a function, or a method of a class."""
		self._check_docstring(node)
		super().generic_visit(node)

	def visit_ClassDef(self, node: ast.ClassDef) -> None:
		"""Check the docstring of a class."""
		self._check_docstring(node)
		super().generic_visit(node)

	def visit_Module(self, node: ast.Module) -> None:
		"""Check the module-level docstring."""
		self._check_docstring(node)
		super().generic_visit(node)


class Plugin:
	name: str = __name__
	version: str = __version__

	def __init__(self, tree: ast.AST):
		self._tree = tree

	def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
		"""
		Traverse the Abstract Syntax Tree, extract docstrings and check them.

		Yields a tuple of (line number, column offset, error message, type(self))
		"""

		visitor = Visitor()
		visitor.visit(self._tree)

		for line, col, msg in visitor.errors:
			yield line, col, msg, type(self)
