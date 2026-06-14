"""Safe-enough Python execution for beginner Mompy missions.

This runner is intentionally small and conservative. It executes simple
educational code in a separate process, captures stdout, blocks dangerous AST
nodes and names, and kills slow code after a short timeout.
"""

from __future__ import annotations

import ast
import contextlib
import io
import multiprocessing
import queue
import traceback
from dataclasses import dataclass
from types import MappingProxyType


TIMEOUT_SECONDS = 1.5
MAX_CODE_LENGTH = 4_000
MAX_OUTPUT_LENGTH = 2_000

ALLOWED_BUILTINS = MappingProxyType(
    {
        "abs": abs,
        "bool": bool,
        "dict": dict,
        "enumerate": enumerate,
        "float": float,
        "int": int,
        "len": len,
        "list": list,
        "max": max,
        "min": min,
        "print": print,
        "range": range,
        "round": round,
        "set": set,
        "str": str,
        "sum": sum,
        "tuple": tuple,
        "True": True,
        "False": False,
        "None": None,
    }
)

BLOCKED_NAMES = {
    "__builtins__",
    "__import__",
    "breakpoint",
    "compile",
    "delattr",
    "dir",
    "eval",
    "exec",
    "getattr",
    "globals",
    "help",
    "input",
    "locals",
    "memoryview",
    "open",
    "setattr",
    "type",
    "vars",
}

BLOCKED_NODES = (
    ast.AsyncFor,
    ast.AsyncFunctionDef,
    ast.AsyncWith,
    ast.Await,
    ast.ClassDef,
    ast.Delete,
    ast.Global,
    ast.Import,
    ast.ImportFrom,
    ast.Lambda,
    ast.Nonlocal,
    ast.Raise,
    ast.Try,
    ast.With,
)


@dataclass(frozen=True)
class SafetyIssue:
    message: str


def _find_safety_issue(tree: ast.AST) -> SafetyIssue | None:
    for node in ast.walk(tree):
        if isinstance(node, BLOCKED_NODES):
            return SafetyIssue("Este recurso ainda nao e permitido nas missoes.")

        if isinstance(node, ast.Name) and node.id in BLOCKED_NAMES:
            return SafetyIssue(f"O nome '{node.id}' nao pode ser usado aqui.")

        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            return SafetyIssue("Acesso interno com __ nao e permitido.")

    return None


def _execute_in_child(user_code: str, result_queue: multiprocessing.Queue) -> None:
    stdout = io.StringIO()
    execution_scope = {"__builtins__": dict(ALLOWED_BUILTINS)}

    try:
        compiled = compile(user_code, "<mompy-user-code>", "exec")
        with contextlib.redirect_stdout(stdout):
            exec(compiled, execution_scope, execution_scope)
    except Exception as error:
        result_queue.put(
            {
                "ok": False,
                "output": stdout.getvalue()[:MAX_OUTPUT_LENGTH],
                "error": f"{error.__class__.__name__}: {error}",
                "traceback": traceback.format_exc(limit=1),
                "timeout": False,
            }
        )
        return

    result_queue.put(
        {
            "ok": True,
            "output": stdout.getvalue()[:MAX_OUTPUT_LENGTH].rstrip("\n"),
            "error": "",
            "traceback": "",
            "timeout": False,
        }
    )


def run_user_code_safely(user_code: str, timeout: float = TIMEOUT_SECONDS) -> dict:
    code = user_code or ""
    if len(code) > MAX_CODE_LENGTH:
        return {
            "ok": False,
            "output": "",
            "error": "Codigo muito longo para esta missao.",
            "timeout": False,
            "implemented": True,
        }

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return {
            "ok": False,
            "output": "",
            "error": f"SyntaxError: {error.msg}",
            "timeout": False,
            "implemented": True,
        }

    safety_issue = _find_safety_issue(tree)
    if safety_issue:
        return {
            "ok": False,
            "output": "",
            "error": safety_issue.message,
            "timeout": False,
            "implemented": True,
        }

    context = multiprocessing.get_context("spawn")
    result_queue: multiprocessing.Queue = context.Queue(maxsize=1)
    process = context.Process(target=_execute_in_child, args=(code, result_queue))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join(0.5)
        return {
            "ok": False,
            "output": "",
            "error": "Tempo limite excedido.",
            "timeout": True,
            "implemented": True,
        }

    try:
        result = result_queue.get_nowait()
    except queue.Empty:
        result = {
            "ok": False,
            "output": "",
            "error": "Execucao finalizada sem resposta.",
            "timeout": False,
        }

    result["implemented"] = True
    return result
