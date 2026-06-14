"""Future safe Python execution layer.

Running arbitrary code is intentionally not enabled in this phase. The next
backend phases can implement sandboxing here without touching the frontend.
"""

from __future__ import annotations


def run_user_code_safely(user_code: str) -> dict:
    return {
        "ok": False,
        "output": "",
        "error": "Execucao segura de codigo ainda nao implementada.",
        "implemented": False,
        "received_characters": len(user_code or ""),
    }
