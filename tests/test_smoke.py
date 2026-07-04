"""Smoke tests — AST parse gate + import validation."""
import ast
import pathlib


def test_all_sources_parse():
    root = pathlib.Path(__file__).parent.parent / "src"
    errors = []
    for f in root.rglob("*.py"):
        try:
            ast.parse(f.read_text(encoding="utf-8"))
        except SyntaxError as e:
            errors.append(f"{f}: {e}")
    assert not errors, "\n".join(errors)


def test_package_importable():
    import reli  # noqa: F401
