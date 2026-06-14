"""Mission catalog for Mompy.

The current frontend already ships twenty playable missions. This module keeps
the Python-side source of truth for the same learning path, so future phases can
move validation, progress, XP, and execution out of JavaScript.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict


PLANNED_TOTAL_MISSIONS = 30


@dataclass(frozen=True)
class Mission:
    id: str
    number: int
    level: int
    block: int
    title: str
    concept: str
    description: str
    objective: str
    starter_code: str
    expected_output: str
    help: str
    expected_concepts: tuple[str, ...]
    xp: int

    def to_dict(self) -> dict:
        data = asdict(self)
        data["expected_concepts"] = list(self.expected_concepts)
        return data


def mission_xp(level: int) -> int:
    """Return the same progressive mission XP used by the frontend."""

    return 35 + max(0, level - 1) * 5


MISSIONS: tuple[Mission, ...] = (
    Mission(
        id="mission_001",
        number=1,
        level=1,
        block=1,
        title="Mission 01 - First Output",
        concept="print",
        description="Primeiro passo: faca o programa escrever uma mensagem no console.",
        objective="Use print() para mostrar exatamente: Hello, Mompy!",
        starter_code="# escreva aqui\n",
        expected_output="Hello, Mompy!",
        help='Use aspas dentro do print: print("Hello, Mompy!")',
        expected_concepts=("print", "string"),
        xp=mission_xp(1),
    ),
    Mission(
        id="mission_002",
        number=2,
        level=2,
        block=1,
        title="Mission 02 - Variable",
        concept="variables",
        description="Variaveis guardam valores para voce usar depois.",
        objective='Crie name = "Mompy" e depois mostre name com print().',
        starter_code='name = "Mompy"\n',
        expected_output="Mompy",
        help='Depois de criar a variavel, use print(name). Nao coloque name entre aspas no print.',
        expected_concepts=("variable", "print", "string"),
        xp=mission_xp(2),
    ),
    Mission(
        id="mission_003",
        number=3,
        level=3,
        block=1,
        title="Mission 03 - Sum",
        concept="math",
        description="Python consegue fazer contas simples direto no codigo.",
        objective="Some 2 + 3 e mostre o resultado no console.",
        starter_code="a = 2\nb = 3\n",
        expected_output="5",
        help="Voce pode usar print(a + b) depois de criar as variaveis.",
        expected_concepts=("number", "addition", "print"),
        xp=mission_xp(3),
    ),
    Mission(
        id="mission_004",
        number=4,
        level=4,
        block=1,
        title="Mission 04 - If",
        concept="conditionals",
        description="O if executa um bloco de codigo apenas quando uma condicao e verdadeira.",
        objective="Use if para mostrar exatamente: Ready",
        starter_code="power = True\n",
        expected_output="Ready",
        help='Use if power: e, dentro dele, print("Ready").',
        expected_concepts=("if", "boolean", "print"),
        xp=mission_xp(4),
    ),
    Mission(
        id="mission_005",
        number=5,
        level=5,
        block=1,
        title="Mission 05 - For Loop",
        concept="for",
        description="O for repete comandos para uma sequencia de valores.",
        objective="Use range(3) para mostrar 0, 1 e 2.",
        starter_code="for i in range(3):\n    ",
        expected_output="0\n1\n2",
        help="Dentro do for, use print(i). A linha do print precisa ficar indentada.",
        expected_concepts=("for", "range", "print"),
        xp=mission_xp(5),
    ),
    Mission(
        id="mission_006",
        number=6,
        level=6,
        block=2,
        title="Mission 06 - List Item",
        concept="lists",
        description="Listas guardam varios valores em ordem.",
        objective='Crie uma lista com "onion", "terminal", "python" e mostre o segundo item.',
        starter_code='items = ["onion", "terminal", "python"]\n',
        expected_output="terminal",
        help="O primeiro item e indice 0. O segundo item e items[1].",
        expected_concepts=("list", "index", "print"),
        xp=mission_xp(6),
    ),
    Mission(
        id="mission_007",
        number=7,
        level=7,
        block=2,
        title="Mission 07 - Length",
        concept="len",
        description="len() conta quantos itens ou caracteres existem em um valor.",
        objective='Mostre o tamanho da palavra "Mompy".',
        starter_code='word = "Mompy"\n',
        expected_output="5",
        help='Use print(len(word)) ou print(len("Mompy")).',
        expected_concepts=("len", "string", "print"),
        xp=mission_xp(7),
    ),
    Mission(
        id="mission_008",
        number=8,
        level=8,
        block=2,
        title="Mission 08 - Function",
        concept="functions",
        description="Funcoes guardam uma pequena tarefa para reutilizar depois.",
        objective="Crie greet(user) e mostre: Hello, Mompy",
        starter_code="def greet(user):\n    ",
        expected_output="Hello, Mompy",
        help='Retorne ou imprima "Hello, " + user, depois chame greet("Mompy").',
        expected_concepts=("function", "parameter", "return", "print"),
        xp=mission_xp(8),
    ),
    Mission(
        id="mission_009",
        number=9,
        level=9,
        block=2,
        title="Mission 09 - Boolean",
        concept="booleans",
        description="Booleanos representam verdadeiro ou falso.",
        objective="Crie is_ready = True e mostre esse valor.",
        starter_code="is_ready = True\n",
        expected_output="True",
        help="Use print(is_ready). Em Python, True comeca com T maiusculo.",
        expected_concepts=("boolean", "variable", "print"),
        xp=mission_xp(9),
    ),
    Mission(
        id="mission_010",
        number=10,
        level=10,
        block=2,
        title="Mission 10 - Uppercase",
        concept="string methods",
        description="Strings tem metodos que transformam texto.",
        objective='Transforme "mompy" em letras maiusculas.',
        starter_code='name = "mompy"\n',
        expected_output="MOMPY",
        help="Use name.upper() dentro do print.",
        expected_concepts=("string", "method", "upper", "print"),
        xp=mission_xp(10),
    ),
    Mission(
        id="mission_011",
        number=11,
        level=11,
        block=3,
        title="Mission 11 - Append",
        concept="append",
        description="append() adiciona um item no final de uma lista.",
        objective="Adicione 4 em [1, 2, 3] e mostre a lista.",
        starter_code="numbers = [1, 2, 3]\n",
        expected_output="[1, 2, 3, 4]",
        help="Use numbers.append(4), depois print(numbers).",
        expected_concepts=("list", "append", "print"),
        xp=mission_xp(11),
    ),
    Mission(
        id="mission_012",
        number=12,
        level=12,
        block=3,
        title="Mission 12 - Dictionary",
        concept="dictionaries",
        description="Dicionarios guardam valores com nomes de chave.",
        objective='Crie um dicionario com name = "Mompy" e mostre esse valor.',
        starter_code='profile = {"name": "Mompy"}\n',
        expected_output="Mompy",
        help='Use print(profile["name"]).',
        expected_concepts=("dict", "key", "print"),
        xp=mission_xp(12),
    ),
    Mission(
        id="mission_013",
        number=13,
        level=13,
        block=3,
        title="Mission 13 - While",
        concept="while",
        description="while repete enquanto uma condicao continuar verdadeira.",
        objective="Use while para mostrar 0, 1 e 2.",
        starter_code="count = 0\nwhile count < 3:\n    ",
        expected_output="0\n1\n2",
        help="Dentro do while, use print(count) e depois count += 1.",
        expected_concepts=("while", "comparison", "increment", "print"),
        xp=mission_xp(13),
    ),
    Mission(
        id="mission_014",
        number=14,
        level=14,
        block=3,
        title="Mission 14 - F-String",
        concept="f-strings",
        description="f-strings colocam variaveis dentro de textos.",
        objective='Com user = "Mackson", mostre: Hello, Mackson',
        starter_code='user = "Mackson"\n',
        expected_output="Hello, Mackson",
        help='Use print(f"Hello, {user}").',
        expected_concepts=("f-string", "variable", "print"),
        xp=mission_xp(14),
    ),
    Mission(
        id="mission_015",
        number=15,
        level=15,
        block=3,
        title="Mission 15 - Comparison",
        concept="comparisons",
        description="Comparacoes retornam True ou False.",
        objective="Mostre se 10 e maior que 3.",
        starter_code="",
        expected_output="True",
        help="Use print(10 > 3).",
        expected_concepts=("comparison", "print"),
        xp=mission_xp(15),
    ),
    Mission(
        id="mission_016",
        number=16,
        level=16,
        block=4,
        title="Mission 16 - Modulo",
        concept="modulo",
        description="O operador % mostra o resto de uma divisao.",
        objective="Mostre o resto de 8 dividido por 2.",
        starter_code="",
        expected_output="0",
        help="Use print(8 % 2).",
        expected_concepts=("modulo", "print"),
        xp=mission_xp(16),
    ),
    Mission(
        id="mission_017",
        number=17,
        level=17,
        block=4,
        title="Mission 17 - List Comprehension",
        concept="list comprehensions",
        description="List comprehensions criam listas novas em uma linha.",
        objective="Dobre [1, 2, 3] e mostre [2, 4, 6].",
        starter_code="numbers = [1, 2, 3]\n",
        expected_output="[2, 4, 6]",
        help="Use print([n * 2 for n in numbers]).",
        expected_concepts=("list comprehension", "for", "print"),
        xp=mission_xp(17),
    ),
    Mission(
        id="mission_018",
        number=18,
        level=18,
        block=4,
        title="Mission 18 - Return Value",
        concept="return",
        description="Uma funcao pode devolver um resultado com return.",
        objective="Crie add(a, b) e mostre add(2, 3).",
        starter_code="def add(a, b):\n    ",
        expected_output="5",
        help="A funcao deve retornar a + b. Depois use print(add(2, 3)).",
        expected_concepts=("function", "return", "addition", "print"),
        xp=mission_xp(18),
    ),
    Mission(
        id="mission_019",
        number=19,
        level=19,
        block=4,
        title="Mission 19 - Split",
        concept="split",
        description="split() separa uma frase em uma lista de palavras.",
        objective='Separe "Python is fun" em palavras e mostre a lista.',
        starter_code='phrase = "Python is fun"\n',
        expected_output="['Python', 'is', 'fun']",
        help="Use print(phrase.split()).",
        expected_concepts=("string", "split", "list", "print"),
        xp=mission_xp(19),
    ),
    Mission(
        id="mission_020",
        number=20,
        level=20,
        block=4,
        title="Mission 20 - Small Loop",
        concept="loop plus string method",
        description="Voce ja consegue combinar loop, texto e metodo de string.",
        objective='Mostre as letras de "py" em maiusculas, uma por linha.',
        starter_code='for letter in "py":\n    ',
        expected_output="P\nY",
        help="Dentro do for, use print(letter.upper()).",
        expected_concepts=("for", "string", "upper", "print"),
        xp=mission_xp(20),
    ),
)


MISSIONS_BY_ID: dict[str, Mission] = {mission.id: mission for mission in MISSIONS}


def get_mission(mission_id: str) -> Mission | None:
    return MISSIONS_BY_ID.get(mission_id)


def get_missions() -> list[dict]:
    return [mission.to_dict() for mission in MISSIONS]


def get_current_mission(index: int) -> Mission:
    if index < 0:
        return MISSIONS[0]
    if index >= len(MISSIONS):
        return MISSIONS[-1]
    return MISSIONS[index]
