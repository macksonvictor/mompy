"""Guided lesson metadata for Mompy blocks."""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Lesson:
    id: str
    title: str
    block: int
    missions_range: str
    intro_title: str
    goals: tuple[str, ...]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["goals"] = list(self.goals)
        return data


LESSONS: tuple[Lesson, ...] = (
    Lesson(
        id="lesson_001",
        title="Primeiros comandos em Python",
        block=1,
        missions_range="1-5",
        intro_title="Primeiros comandos em Python",
        goals=(
            "Entender que Python executa instrucoes",
            "Usar aspas para criar texto",
            "Mostrar mensagens com print()",
        ),
    ),
    Lesson(
        id="lesson_002",
        title="Variaveis e valores",
        block=2,
        missions_range="6-10",
        intro_title="Variaveis e valores",
        goals=(
            "Guardar valores em nomes",
            "Usar variaveis em print()",
            "Aplicar funcoes simples como len()",
        ),
    ),
    Lesson(
        id="lesson_003",
        title="Decisoes",
        block=3,
        missions_range="11-15",
        intro_title="Decisoes",
        goals=(
            "Ler valores em listas e dicionarios",
            "Usar condicoes e comparacoes",
            "Combinar texto com f-strings",
        ),
    ),
    Lesson(
        id="lesson_004",
        title="Repeticoes",
        block=4,
        missions_range="16-20",
        intro_title="Repeticoes",
        goals=(
            "Repetir tarefas com for e while",
            "Transformar dados com metodos",
            "Criar resultados pequenos e verificaveis",
        ),
    ),
    Lesson(
        id="lesson_005",
        title="Listas",
        block=5,
        missions_range="21-25",
        intro_title="Listas",
        goals=(
            "Criar colecoes",
            "Ler itens por indice",
            "Montar novas listas",
        ),
    ),
    Lesson(
        id="lesson_006",
        title="Funcoes",
        block=6,
        missions_range="26-30",
        intro_title="Funcoes",
        goals=(
            "Nomear tarefas",
            "Receber parametros",
            "Devolver valores com return",
        ),
    ),
)


def get_lessons() -> list[dict]:
    return [lesson.to_dict() for lesson in LESSONS]


def lesson_for_mission_number(mission_number: int) -> Lesson | None:
    for lesson in LESSONS:
        start, end = [int(part) for part in lesson.missions_range.split("-")]
        if start <= mission_number <= end:
            return lesson
    return None
