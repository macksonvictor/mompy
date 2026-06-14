"""Guided briefings shown before mission blocks.

The frontend currently animates these lessons. This Python representation keeps
the educational content available to the backend before phase 10.3 connects both
layers through pywebview.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class BriefingStep:
    type: str
    title: str | None = None
    text: str | None = None
    retry_text: str | None = None
    question: str | None = None
    options: tuple[dict, ...] = ()
    success_text: str | None = None
    fail_text: str | None = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["options"] = [dict(option) for option in self.options]
        return {key: value for key, value in data.items() if value not in (None, (), [])}


@dataclass(frozen=True)
class Briefing:
    id: str
    title: str
    subtitle: str
    before_mission_index: int
    missions_range: str
    steps: tuple[BriefingStep, ...]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "before_mission_index": self.before_mission_index,
            "missions_range": self.missions_range,
            "steps": [step.to_dict() for step in self.steps],
        }


BRIEFINGS: tuple[Briefing, ...] = (
    Briefing(
        id="briefing_001",
        title="Preparacao do Bloco 01",
        subtitle="Primeiros comandos em Python",
        before_mission_index=0,
        missions_range="1-5",
        steps=(
            BriefingStep(
                type="lesson",
                title="O que e Python?",
                text="Python e uma linguagem de programacao. Voce escreve instrucoes, e o computador executa uma por uma.",
                retry_text="Pense em Python como uma forma de conversar com o computador por comandos escritos.",
            ),
            BriefingStep(
                type="lesson",
                title="Instrucoes",
                text="Uma instrucao e uma ordem pequena. O computador segue exatamente o que foi escrito.",
                retry_text="Uma linha de codigo pode ser como uma ordem: faca isso agora.",
            ),
            BriefingStep(
                type="check",
                question="Python e usado para:",
                options=(
                    {"label": "A", "text": "escrever instrucoes para o computador", "correct": True},
                    {"label": "B", "text": "decorar a tela do computador", "correct": False},
                    {"label": "C", "text": "ligar cabos fisicos", "correct": False},
                ),
                success_text="Certo. Python permite escrever instrucoes para o computador executar.",
                fail_text="Quase. Python nao e decoracao nem cabo fisico. E uma linguagem para escrever instrucoes.",
            ),
            BriefingStep(
                type="lesson",
                title="Texto e aspas",
                text="Quando queremos que Python trate algo como texto, normalmente usamos aspas.",
                retry_text="Com aspas, Python entende uma palavra como texto.",
            ),
            BriefingStep(
                type="lesson",
                title="Mostrar na tela",
                text="Em Python, print e o comando basico para mostrar uma mensagem.",
                retry_text="print envia uma mensagem para o console e ajuda voce a ver o resultado.",
            ),
        ),
    ),
    Briefing(
        id="briefing_002",
        title="Preparacao do Bloco 02",
        subtitle="Variaveis e valores",
        before_mission_index=5,
        missions_range="6-10",
        steps=(
            BriefingStep(
                type="lesson",
                title="Guardar informacao",
                text="Uma variavel e um nome que guarda um valor. Voce usa esse nome depois para recuperar a informacao.",
                retry_text="Imagine uma etiqueta em uma caixa. A etiqueta e o nome, o conteudo e o valor.",
            ),
            BriefingStep(
                type="lesson",
                title="Atribuicao",
                text="Em Python, o sinal de igual coloca um valor dentro de um nome.",
                retry_text="Quando voce escreve nome = valor, esta guardando este valor neste nome.",
            ),
            BriefingStep(
                type="check",
                question="Em uma variavel, o sinal = significa:",
                options=(
                    {"label": "A", "text": "guardar um valor em um nome", "correct": True},
                    {"label": "B", "text": "mostrar uma tela", "correct": False},
                    {"label": "C", "text": "apagar o programa", "correct": False},
                ),
                success_text="Certo. O sinal de igual atribui um valor a um nome.",
                fail_text="Aqui o igual serve para guardar um valor em uma variavel.",
            ),
            BriefingStep(
                type="lesson",
                title="Usar o valor",
                text="Depois que uma variavel existe, voce pode usar o nome dela em comandos.",
                retry_text="Use o nome da variavel, e Python pega o valor guardado nela.",
            ),
        ),
    ),
    Briefing(
        id="briefing_003",
        title="Preparacao do Bloco 03",
        subtitle="Decisoes",
        before_mission_index=10,
        missions_range="11-15",
        steps=(
            BriefingStep(
                type="lesson",
                title="Condicao",
                text="Uma condicao e uma pergunta com resposta verdadeira ou falsa.",
                retry_text="Se a condicao for verdadeira, o programa segue um caminho.",
            ),
            BriefingStep(
                type="lesson",
                title="If",
                text="O if executa um bloco apenas quando a condicao e verdadeira.",
                retry_text="if significa se. Se algo for verdadeiro, execute as linhas indentadas.",
            ),
            BriefingStep(
                type="check",
                question="Um if serve para:",
                options=(
                    {"label": "A", "text": "tomar uma decisao no programa", "correct": True},
                    {"label": "B", "text": "trocar a fonte do editor", "correct": False},
                    {"label": "C", "text": "criar som ambiente", "correct": False},
                ),
                success_text="Certo. O if cria caminhos diferentes no programa.",
                fail_text="O if nao muda o visual. Ele decide se um bloco deve executar.",
            ),
            BriefingStep(
                type="lesson",
                title="Comparacoes",
                text="Comparacoes como maior que, menor que ou igual a geram True ou False.",
                retry_text="Comparar e perguntar: isto e maior? isto e igual?",
            ),
        ),
    ),
    Briefing(
        id="briefing_004",
        title="Preparacao do Bloco 04",
        subtitle="Repeticoes",
        before_mission_index=15,
        missions_range="16-20",
        steps=(
            BriefingStep(
                type="lesson",
                title="Repetir acoes",
                text="Programas muitas vezes precisam repetir uma acao. Loops evitam copiar a mesma linha varias vezes.",
                retry_text="Quando uma tarefa se repete, um loop ajuda o computador a fazer isso em sequencia.",
            ),
            BriefingStep(
                type="lesson",
                title="For",
                text="O for percorre uma sequencia. A cada volta, ele trabalha com um item ou numero.",
                retry_text="Pense no for como uma esteira: cada item passa uma vez.",
            ),
            BriefingStep(
                type="check",
                question="Um loop ajuda principalmente a:",
                options=(
                    {"label": "A", "text": "repetir acoes sem copiar codigo", "correct": True},
                    {"label": "B", "text": "desligar o monitor", "correct": False},
                    {"label": "C", "text": "mudar o nome do usuario", "correct": False},
                ),
                success_text="Certo. Loops repetem acoes de forma organizada.",
                fail_text="Loop e sobre repeticao de codigo, nao sobre interface.",
            ),
            BriefingStep(
                type="lesson",
                title="Indentacao",
                text="As linhas indentadas pertencem ao loop. Isso mostra ao Python o que deve repetir.",
                retry_text="A indentacao e o recuo no comeco da linha.",
            ),
        ),
    ),
    Briefing(
        id="briefing_005",
        title="Preparacao do Bloco 05",
        subtitle="Listas",
        before_mission_index=20,
        missions_range="21-25",
        steps=(
            BriefingStep(
                type="lesson",
                title="Colecoes",
                text="Listas guardam varios valores em uma unica variavel.",
                retry_text="Quando ha muitos valores relacionados, uma lista organiza tudo em ordem.",
            ),
            BriefingStep(
                type="lesson",
                title="Indices",
                text="O primeiro item de uma lista fica na posicao 0.",
                retry_text="Em Python, a contagem de posicoes comeca em zero.",
            ),
            BriefingStep(
                type="check",
                question="Em Python, o primeiro indice de uma lista e:",
                options=(
                    {"label": "A", "text": "0", "correct": True},
                    {"label": "B", "text": "1", "correct": False},
                    {"label": "C", "text": "10", "correct": False},
                ),
                success_text="Certo. Listas comecam no indice 0.",
                fail_text="Ainda nao. O primeiro item fica no indice 0.",
            ),
        ),
    ),
    Briefing(
        id="briefing_006",
        title="Preparacao do Bloco 06",
        subtitle="Funcoes",
        before_mission_index=25,
        missions_range="26-30",
        steps=(
            BriefingStep(
                type="lesson",
                title="Nomear tarefas",
                text="Uma funcao permite dar nome a uma tarefa e chamar essa tarefa quando precisar.",
                retry_text="Funcoes ajudam a nao repetir a mesma ideia varias vezes.",
            ),
            BriefingStep(
                type="lesson",
                title="Parametros",
                text="Parametros sao entradas que a funcao recebe para trabalhar.",
                retry_text="Um parametro funciona como uma informacao que entra na funcao.",
            ),
            BriefingStep(
                type="check",
                question="Uma funcao serve para:",
                options=(
                    {"label": "A", "text": "organizar uma tarefa reutilizavel", "correct": True},
                    {"label": "B", "text": "mudar a cor da moldura", "correct": False},
                    {"label": "C", "text": "criar um arquivo de audio", "correct": False},
                ),
                success_text="Certo. Funcoes organizam tarefas reutilizaveis.",
                fail_text="Funcao e sobre organizar codigo com nome.",
            ),
        ),
    ),
)


BRIEFINGS_BY_ID: dict[str, Briefing] = {briefing.id: briefing for briefing in BRIEFINGS}


def get_briefings() -> list[dict]:
    return [briefing.to_dict() for briefing in BRIEFINGS]


def get_briefing(briefing_id: str) -> dict | None:
    briefing = BRIEFINGS_BY_ID.get(briefing_id)
    return briefing.to_dict() if briefing else None


def briefing_for_mission_index(mission_index: int) -> dict | None:
    for briefing in BRIEFINGS:
        if briefing.before_mission_index == mission_index:
            return briefing.to_dict()
    return None
