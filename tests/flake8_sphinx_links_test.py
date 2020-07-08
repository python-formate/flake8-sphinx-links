# stdlib
import ast

# this package
import pathlib
from pprint import pprint

from flake8_sphinx_links import Plugin
#
#
# def results(s):
# 	return {"{}:{}: {}".format(*r) for r in Plugin(ast.parse(s)).run()}
#
#
# def test_linux_specific():
# 	assert results('print(f"{now:%Y/%-m/%-d %H:%M}")') == {  # noqa: sphinx_links001
# 		"1:9: sphinx_links001 Linux-specific sphinx_links code used.",
# 		"1:13: sphinx_links001 Linux-specific sphinx_links code used.",
# 		}
#
# 	assert results('print(now.sphinx_links("%Y/%-m/%-d %H:%M"))') == {  # noqa: sphinx_links001
# 		"1:22: sphinx_links001 Linux-specific sphinx_links code used.",
# 		"1:26: sphinx_links001 Linux-specific sphinx_links code used.",
# 		}
#
#
# def test_windows_specific():
# 	assert results('print(f"{now:%Y/%#m/%#d %H:%M}")') == {  # noqa: sphinx_links002
# 		"1:9: sphinx_links002 Windows-specific sphinx_links code used.",
# 		"1:13: sphinx_links002 Windows-specific sphinx_links code used.",
# 		}
#
# 	assert results('print(now.sphinx_links("%Y/%#m/%#d %H:%M"))') == {  # noqa: sphinx_links002
# 		"1:22: sphinx_links002 Windows-specific sphinx_links code used.",
# 		"1:26: sphinx_links002 Windows-specific sphinx_links code used.",
# 		}


class BadDocstring:
	"""
	``True``

	``False``

	``None``

	"""


pprint(list(Plugin(ast.parse(pathlib.Path(__file__).read_text())).run()))