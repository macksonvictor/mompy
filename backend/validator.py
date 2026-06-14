"""Simple mission validation.

This phase intentionally does not execute arbitrary user code. The validator
uses AST and regular-expression checks to decide whether the answer has the
expected shape. Real sandboxed execution comes later.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from typing import Callable

from .missions import MISSIONS_BY_ID


@dataclass(frozen=True)
class ValidationResult:
    correct: bool
    message: str
    hints: tuple[str, ...] = ()
    expected_output: str | None = None

    def to_dict(self) -> dict:
        return {
            "correct": self.correct,
            "message": self.message,
            "hints": list(self.hints),
            "expected_output": self.expected_output,
        }


def normalize_code(user_code: str) -> str:
    return "\n".join(line.rstrip() for line in user_code.strip().splitlines())


def parse_python(user_code: str) -> ast.AST | None:
    try:
        return ast.parse(user_code)
    except SyntaxError:
        return None


def matches_any(user_code: str, patterns: tuple[str, ...]) -> bool:
    code = normalize_code(user_code)
    return any(re.search(pattern, code, re.MULTILINE) for pattern in patterns)


def has_print_call(user_code: str) -> bool:
    tree = parse_python(user_code)
    if tree is None:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            return True
    return False


def has_assignment(user_code: str, name: str) -> bool:
    tree = parse_python(user_code)
    if tree is None:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return True
    return False


def _ok(mission_id: str) -> ValidationResult:
    mission = MISSIONS_BY_ID[mission_id]
    return ValidationResult(
        correct=True,
        message="Certo. A resposta tem a estrutura esperada.",
        expected_output=mission.expected_output,
    )


def _fail(mission_id: str, *hints: str) -> ValidationResult:
    mission = MISSIONS_BY_ID.get(mission_id)
    fallback = mission.help if mission else "Revise a estrutura do codigo."
    return ValidationResult(
        correct=False,
        message="Ainda nao. Ajuste o codigo e tente de novo.",
        hints=tuple(hints or (fallback,)),
        expected_output=mission.expected_output if mission else None,
    )


def _mission_001(code: str) -> ValidationResult:
    if matches_any(code, (r'^print\s*\(\s*"Hello,\s*Mompy!"\s*\)$', r"^print\s*\(\s*'Hello,\s*Mompy!'\s*\)$")):
        return _ok("mission_001")
    return _fail("mission_001", 'Use exatamente print("Hello, Mompy!").')


def _mission_002(code: str) -> ValidationResult:
    if matches_any(code, (r"name\s*=\s*[\"']Mompy[\"'][\s\S]*print\s*\(\s*name\s*\)",)):
        return _ok("mission_002")
    return _fail("mission_002", 'Crie name = "Mompy" e depois use print(name).')


def _mission_003(code: str) -> ValidationResult:
    if matches_any(
        code,
        (
            r"print\s*\(\s*(2\s*\+\s*3|3\s*\+\s*2)\s*\)",
            r"a\s*=\s*2[\s\S]*b\s*=\s*3[\s\S]*print\s*\(\s*(a\s*\+\s*b|b\s*\+\s*a)\s*\)",
        ),
    ):
        return _ok("mission_003")
    return _fail("mission_003", "Mostre a soma com print(a + b) ou print(2 + 3).")


def _mission_004(code: str) -> ValidationResult:
    if matches_any(code, (r"if\s+power\s*:\s*[\s\S]*print\s*\(\s*[\"']Ready[\"']\s*\)", r"if\s+True\s*:\s*[\s\S]*print\s*\(\s*[\"']Ready[\"']\s*\)")):
        return _ok("mission_004")
    return _fail("mission_004", 'Use if power: e dentro dele print("Ready").')


def _mission_005(code: str) -> ValidationResult:
    if matches_any(code, (r"for\s+i\s+in\s+range\s*\(\s*3\s*\)\s*:\s*[\s\S]*print\s*\(\s*i\s*\)",)):
        return _ok("mission_005")
    return _fail("mission_005", "Use for i in range(3): e print(i) indentado.")


def _mission_006(code: str) -> ValidationResult:
    if matches_any(code, (r"items\s*=\s*\[[\s\S]*[\"']onion[\"'][\s\S]*[\"']terminal[\"'][\s\S]*[\"']python[\"'][\s\S]*\][\s\S]*print\s*\(\s*items\s*\[\s*1\s*\]\s*\)",)):
        return _ok("mission_006")
    return _fail("mission_006", "Crie a lista items e mostre items[1].")


def _mission_007(code: str) -> ValidationResult:
    if matches_any(code, (r"word\s*=\s*[\"']Mompy[\"'][\s\S]*print\s*\(\s*len\s*\(\s*word\s*\)\s*\)", r"print\s*\(\s*len\s*\(\s*[\"']Mompy[\"']\s*\)\s*\)")):
        return _ok("mission_007")
    return _fail("mission_007", 'Use print(len(word)) ou print(len("Mompy")).')


def _mission_008(code: str) -> ValidationResult:
    if matches_any(
        code,
        (
            r"def\s+greet\s*\(\s*user\s*\)\s*:[\s\S]*(return|print)\s*\(?\s*f?[\"']Hello,\s*\{?user\}?[\"']\s*\)?[\s\S]*print\s*\(\s*greet\s*\(\s*[\"']Mompy[\"']\s*\)\s*\)",
            r"def\s+greet\s*\(\s*user\s*\)\s*:[\s\S]*return\s+[\"']Hello,\s*[\"']\s*\+\s*user[\s\S]*print\s*\(\s*greet\s*\(\s*[\"']Mompy[\"']\s*\)\s*\)",
        ),
    ):
        return _ok("mission_008")
    return _fail("mission_008", 'Crie greet(user), retorne "Hello, " + user e mostre greet("Mompy").')


def _mission_009(code: str) -> ValidationResult:
    if matches_any(code, (r"is_ready\s*=\s*True[\s\S]*print\s*\(\s*is_ready\s*\)",)):
        return _ok("mission_009")
    return _fail("mission_009", "Use is_ready = True e print(is_ready).")


def _mission_010(code: str) -> ValidationResult:
    if matches_any(code, (r"name\s*=\s*[\"']mompy[\"'][\s\S]*print\s*\(\s*name\.upper\s*\(\s*\)\s*\)", r"print\s*\(\s*[\"']mompy[\"']\.upper\s*\(\s*\)\s*\)")):
        return _ok("mission_010")
    return _fail("mission_010", "Use name.upper() dentro do print.")


def _mission_011(code: str) -> ValidationResult:
    if matches_any(code, (r"numbers\s*=\s*\[\s*1\s*,\s*2\s*,\s*3\s*\][\s\S]*numbers\.append\s*\(\s*4\s*\)[\s\S]*print\s*\(\s*numbers\s*\)",)):
        return _ok("mission_011")
    return _fail("mission_011", "Use numbers.append(4), depois print(numbers).")


def _mission_012(code: str) -> ValidationResult:
    if matches_any(code, (r"profile\s*=\s*\{[\s\S]*[\"']name[\"']\s*:\s*[\"']Mompy[\"'][\s\S]*\}[\s\S]*print\s*\(\s*profile\s*\[\s*[\"']name[\"']\s*\]\s*\)",)):
        return _ok("mission_012")
    return _fail("mission_012", 'Use print(profile["name"]).')


def _mission_013(code: str) -> ValidationResult:
    if matches_any(code, (r"count\s*=\s*0[\s\S]*while\s+count\s*<\s*3\s*:\s*[\s\S]*print\s*\(\s*count\s*\)[\s\S]*count\s*(\+=\s*1|=\s*count\s*\+\s*1)",)):
        return _ok("mission_013")
    return _fail("mission_013", "Use while count < 3, print(count) e count += 1.")


def _mission_014(code: str) -> ValidationResult:
    if matches_any(code, (r"user\s*=\s*[\"']Mackson[\"'][\s\S]*print\s*\(\s*f[\"']Hello,\s*\{user\}[\"']\s*\)",)):
        return _ok("mission_014")
    return _fail("mission_014", 'Use print(f"Hello, {user}").')


def _mission_015(code: str) -> ValidationResult:
    if matches_any(code, (r"print\s*\(\s*10\s*>\s*3\s*\)",)):
        return _ok("mission_015")
    return _fail("mission_015", "Use print(10 > 3).")


def _mission_016(code: str) -> ValidationResult:
    if matches_any(code, (r"print\s*\(\s*8\s*%\s*2\s*\)",)):
        return _ok("mission_016")
    return _fail("mission_016", "Use print(8 % 2).")


def _mission_017(code: str) -> ValidationResult:
    if matches_any(code, (r"numbers\s*=\s*\[\s*1\s*,\s*2\s*,\s*3\s*\][\s\S]*print\s*\(\s*\[\s*n\s*\*\s*2\s+for\s+n\s+in\s+numbers\s*\]\s*\)",)):
        return _ok("mission_017")
    return _fail("mission_017", "Use print([n * 2 for n in numbers]).")


def _mission_018(code: str) -> ValidationResult:
    if matches_any(code, (r"def\s+add\s*\(\s*a\s*,\s*b\s*\)\s*:\s*[\s\S]*return\s+a\s*\+\s*b[\s\S]*print\s*\(\s*add\s*\(\s*2\s*,\s*3\s*\)\s*\)",)):
        return _ok("mission_018")
    return _fail("mission_018", "Retorne a + b e mostre print(add(2, 3)).")


def _mission_019(code: str) -> ValidationResult:
    if matches_any(code, (r"phrase\s*=\s*[\"']Python is fun[\"'][\s\S]*print\s*\(\s*phrase\.split\s*\(\s*\)\s*\)",)):
        return _ok("mission_019")
    return _fail("mission_019", "Use print(phrase.split()).")


def _mission_020(code: str) -> ValidationResult:
    if matches_any(code, (r"for\s+letter\s+in\s+[\"']py[\"']\s*:\s*[\s\S]*print\s*\(\s*letter\.upper\s*\(\s*\)\s*\)",)):
        return _ok("mission_020")
    return _fail("mission_020", 'Use for letter in "py": e print(letter.upper()).')


VALIDATORS: dict[str, Callable[[str], ValidationResult]] = {
    f"mission_{number:03d}": validator
    for number, validator in enumerate(
        (
            _mission_001,
            _mission_002,
            _mission_003,
            _mission_004,
            _mission_005,
            _mission_006,
            _mission_007,
            _mission_008,
            _mission_009,
            _mission_010,
            _mission_011,
            _mission_012,
            _mission_013,
            _mission_014,
            _mission_015,
            _mission_016,
            _mission_017,
            _mission_018,
            _mission_019,
            _mission_020,
        ),
        start=1,
    )
}


def validate_mission(mission_id: str, user_code: str) -> dict:
    mission = MISSIONS_BY_ID.get(mission_id)
    if mission is None:
        return ValidationResult(
            correct=False,
            message="Missao desconhecida.",
            hints=("Verifique o id da missao antes de validar.",),
        ).to_dict()

    if not user_code or not user_code.strip():
        return _fail(mission_id, "Escreva algum codigo antes de rodar.").to_dict()

    if parse_python(user_code) is None:
        return _fail(mission_id, "Existe um erro de sintaxe. Confira parenteses, aspas e indentacao.").to_dict()

    validator = VALIDATORS.get(mission_id)
    if validator is None:
        return ValidationResult(
            correct=False,
            message="Validador ainda nao implementado para esta missao.",
            hints=("A estrutura ja esta pronta para adicionar esta validacao.",),
            expected_output=mission.expected_output,
        ).to_dict()

    return validator(user_code).to_dict()
