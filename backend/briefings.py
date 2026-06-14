"""Guided briefings shown before mission blocks."""

from __future__ import annotations

from dataclasses import asdict, dataclass


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


def check(question: str, correct: str, wrong_a: str, wrong_b: str, success: str, fail: str) -> BriefingStep:
    return BriefingStep(
        type="check",
        question=question,
        options=(
            {"label": "A", "text": wrong_a, "correct": False},
            {"label": "B", "text": correct, "correct": True},
            {"label": "C", "text": wrong_b, "correct": False},
        ),
        success_text=success,
        fail_text=fail,
    )


BRIEFINGS: tuple[Briefing, ...] = (
    Briefing(
        id="briefing_001",
        title="Mompy",
        subtitle="Primeiros comandos em Python",
        before_mission_index=0,
        missions_range="1-5",
        steps=(
            BriefingStep(
                type="lesson",
                title="Python",
                text="Python e uma linguagem criada por Guido van Rossum. Ela ficou conhecida por ser legivel: o codigo tenta parecer claro para pessoas.",
                retry_text="Pense em Python como uma forma clara de escrever ordens para o computador. A ideia e ler o codigo sem sofrimento.",
            ),
            BriefingStep(
                type="lesson",
                title="Comandos",
                text="Um programa e feito de comandos. Executar codigo significa pedir ao Python para seguir esses comandos em ordem.",
                retry_text="Cada linha importante e uma instrucao. O Python le e tenta executar exatamente o que esta escrito.",
            ),
            BriefingStep(
                type="lesson",
                title="Texto",
                text="Quando queremos escrever uma mensagem, usamos texto. Em Python, texto normalmente fica entre aspas.",
                retry_text='Sem aspas, Python pensa que a palavra e um nome de codigo. Com aspas, ele entende como mensagem, como "Hello".',
            ),
            BriefingStep(
                type="lesson",
                title="print",
                text="print e o comando basico para mostrar algo na saida do console. Ele usa parenteses para receber o que sera mostrado.",
                retry_text='A forma e print("mensagem"). O comando e print; o texto fica entre aspas; tudo fica dentro dos parenteses.',
            ),
            check(
                "Para mostrar texto na tela, usamos:",
                "print com texto entre aspas",
                "if com comparacao",
                "for com range",
                "Certo. print mostra mensagens e resultados no console.",
                "Ainda nao. Neste bloco, a ferramenta principal e print com texto entre aspas.",
            ),
            check(
                "Se esquecer as aspas em um texto, Python pode:",
                "tentar ler a palavra como nome de codigo",
                "transformar em numero sozinho",
                "repetir a mensagem",
                "Certo. Aspas dizem ao Python que aquilo e texto.",
                "Quase. Aspas sao o sinal de que o conteudo e uma mensagem.",
            ),
        ),
    ),
    Briefing(
        id="briefing_002",
        title="Mompy",
        subtitle="Variaveis e valores",
        before_mission_index=5,
        missions_range="6-10",
        steps=(
            BriefingStep(
                type="lesson",
                title="Variavel",
                text="Uma variavel e um nome que guarda um valor. Voce usa o nome depois para recuperar esse valor.",
                retry_text="Imagine uma etiqueta em uma caixa. A etiqueta e o nome da variavel; o que esta dentro e o valor.",
            ),
            BriefingStep(
                type="lesson",
                title="Atribuicao",
                text="Em Python, = guarda um valor em um nome. Isso se chama atribuicao.",
                retry_text='Quando voce escreve name = "Mompy", esta guardando o texto "Mompy" no nome name.',
            ),
            BriefingStep(
                type="lesson",
                title="Nome ou texto",
                text='name sem aspas e uma variavel. "name" com aspas e texto literal. Essa diferenca muda tudo.',
                retry_text='print(name) mostra o valor guardado. print("name") mostra a palavra name.',
            ),
            BriefingStep(
                type="lesson",
                title="Numeros e soma",
                text="Variaveis tambem podem guardar numeros. Voce pode somar valores e mostrar o resultado com print.",
                retry_text="Se a = 2 e b = 3, print(a + b) mostra 5.",
            ),
            check(
                "O sinal = em uma variavel significa:",
                "guardar um valor em um nome",
                "comparar dois valores",
                "mostrar uma mensagem",
                "Certo. = atribui um valor.",
                "Ainda nao. Comparar vem depois; aqui = guarda valor.",
            ),
            check(
                "Qual diferenca importa?",
                "name e variavel; \"name\" e texto",
                "name e sempre texto",
                "aspas apagam variaveis",
                "Certo. Sem aspas, Python procura a variavel.",
                "Quase. Aspas transformam conteudo em texto literal.",
            ),
        ),
    ),
    Briefing(
        id="briefing_003",
        title="Mompy",
        subtitle="Decisoes",
        before_mission_index=10,
        missions_range="11-15",
        steps=(
            BriefingStep(
                type="lesson",
                title="Condicao",
                text="Uma condicao e uma pergunta que resulta em verdadeiro ou falso. Programas usam isso para escolher caminhos.",
                retry_text="Perguntas como 10 > 3 ou code == \"py\" viram True ou False.",
            ),
            BriefingStep(
                type="lesson",
                title="if",
                text="Um if executa um bloco apenas se a condicao for verdadeira. Em Python, a linha do if termina com dois pontos.",
                retry_text="if significa se. Se a pergunta for verdadeira, o bloco indentado roda.",
            ),
            BriefingStep(
                type="lesson",
                title="Indentacao",
                text="Indentado significa afastado para a direita. As linhas indentadas pertencem ao if ou ao else.",
                retry_text="Sem indentacao, Python nao sabe quais linhas fazem parte da decisao.",
            ),
            BriefingStep(
                type="lesson",
                title="Comparar",
                text="Use == para comparar igualdade. Use >, <, >= e <= para comparar tamanho ou ordem.",
                retry_text="= guarda valor. == pergunta se dois valores sao iguais.",
            ),
            BriefingStep(
                type="lesson",
                title="else",
                text="else e o outro caminho. Ele roda quando a condicao do if nao e verdadeira.",
                retry_text="Se o if nao entrar, o else pode cuidar do caso contrario.",
            ),
            check(
                "O que o if faz?",
                "executa um bloco se uma condicao for verdadeira",
                "repete uma acao para sempre",
                "guarda um texto em uma variavel",
                "Certo. if e escolha baseada em condicao.",
                "Ainda nao. if decide; repeticao vem no proximo bloco.",
            ),
            check(
                "Em Python, o bloco que pertence ao if precisa estar:",
                "indentado",
                "sem aspas",
                "fora do arquivo",
                "Certo. Indentacao mostra pertencimento.",
                "Quase. O bloco do if fica afastado para a direita.",
            ),
            check(
                "Qual operador compara igualdade?",
                "==",
                "=",
                ">=",
                "Certo. == compara; = atribui.",
                "Ainda nao. = guarda valor. Para perguntar se e igual, use ==.",
            ),
        ),
    ),
    Briefing(
        id="briefing_004",
        title="Mompy",
        subtitle="Repeticoes",
        before_mission_index=15,
        missions_range="16-20",
        steps=(
            BriefingStep(
                type="lesson",
                title="Repetir",
                text="Repeticoes existem para evitar copiar e colar comandos iguais. O programa faz o mesmo bloco varias vezes.",
                retry_text="Se algo precisa acontecer muitas vezes, um loop organiza isso.",
            ),
            BriefingStep(
                type="lesson",
                title="for",
                text="for percorre uma sequencia. A cada volta, uma variavel recebe o valor atual.",
                retry_text="Em for i in range(3), i vale 0, depois 1, depois 2.",
            ),
            BriefingStep(
                type="lesson",
                title="range",
                text="range cria uma sequencia de numeros. range(3) gera 0, 1 e 2. range(1, 4) gera 1, 2 e 3.",
                retry_text="O final do range nao entra. range(1, 4) para antes do 4.",
            ),
            BriefingStep(
                type="lesson",
                title="Bloco do loop",
                text="O que fica indentado dentro do for roda em cada volta.",
                retry_text="Se print estiver dentro do for, ele pode mostrar algo varias vezes.",
            ),
            BriefingStep(
                type="lesson",
                title="Atualizar valor",
                text="Um loop pode atualizar uma variavel. total = total + number soma um novo valor ao total antigo.",
                retry_text="Isso e comum quando juntamos resultados de varias voltas.",
            ),
            check(
                "Um loop ajuda principalmente a:",
                "repetir acoes sem copiar codigo",
                "comparar igualdade",
                "criar uma funcao",
                "Certo. Loop e repeticao organizada.",
                "Ainda nao. Neste bloco, o foco e repetir acoes.",
            ),
            check(
                "Em for i in range(3), os valores de i sao:",
                "0, 1 e 2",
                "1, 2 e 3",
                "3, 2 e 1",
                "Certo. range(3) comeca em 0 e para antes de 3.",
                "Quase. range(3) gera 0, 1 e 2.",
            ),
        ),
    ),
    Briefing(
        id="briefing_005",
        title="Mompy",
        subtitle="Listas",
        before_mission_index=20,
        missions_range="21-25",
        steps=(
            BriefingStep(
                type="lesson",
                title="Lista",
                text="Uma lista guarda varios valores em uma unica variavel. Ela usa colchetes.",
                retry_text='Exemplo: items = ["onion", "python"]. Os textos ficam entre aspas e separados por virgula.',
            ),
            BriefingStep(
                type="lesson",
                title="Itens",
                text="Cada valor dentro da lista e um item. Virgulas separam os itens.",
                retry_text="Se esquecer virgula, Python pode nao entender onde um item termina e outro comeca.",
            ),
            BriefingStep(
                type="lesson",
                title="Indice",
                text="Listas tem posicoes. Em Python, a primeira posicao e 0, entao o segundo item fica no indice 1.",
                retry_text="items[0] pega o primeiro item. items[1] pega o segundo.",
            ),
            BriefingStep(
                type="lesson",
                title="append e len",
                text="append adiciona um item ao final. len conta quantos itens existem.",
                retry_text="numbers.append(4) adiciona 4. len(numbers) conta os itens.",
            ),
            BriefingStep(
                type="lesson",
                title="Percorrer lista",
                text="Voce tambem pode usar for para passar por cada item de uma lista.",
                retry_text="for item in items: faz item receber um valor da lista por vez.",
            ),
            check(
                "Em Python, o primeiro indice de uma lista e:",
                "0",
                "1",
                "-1 sempre",
                "Certo. Listas comecam no indice 0.",
                "Ainda nao. O primeiro item fica no indice 0.",
            ),
            check(
                "Para adicionar um item no final da lista, usamos:",
                "append",
                "if",
                "def",
                "Certo. append adiciona no final.",
                "Quase. if decide e def cria funcao; append mexe na lista.",
            ),
        ),
    ),
    Briefing(
        id="briefing_006",
        title="Mompy",
        subtitle="Funcoes",
        before_mission_index=25,
        missions_range="26-30",
        steps=(
            BriefingStep(
                type="lesson",
                title="Funcao",
                text="Uma funcao e um bloco de codigo com nome. Ela ajuda a organizar uma tarefa.",
                retry_text="Pense em uma funcao como uma pequena maquina: voce chama pelo nome e ela faz a tarefa.",
            ),
            BriefingStep(
                type="lesson",
                title="def",
                text="Em Python, criamos funcao com def, nome, parenteses e dois pontos. O bloco da funcao fica indentado.",
                retry_text="def say_hello(): cria a funcao. A linha de dentro precisa ficar afastada para a direita.",
            ),
            BriefingStep(
                type="lesson",
                title="Chamar",
                text="Criar uma funcao nao executa ela automaticamente. Voce precisa chamar a funcao pelo nome com parenteses.",
                retry_text="Depois de def say_hello():, escreva say_hello() para rodar.",
            ),
            BriefingStep(
                type="lesson",
                title="Parametros",
                text="Parametros sao informacoes que entram na funcao. Em greet(user), user recebe o valor passado na chamada.",
                retry_text='greet("Mompy") faz user valer "Mompy" dentro da funcao.',
            ),
            BriefingStep(
                type="lesson",
                title="return",
                text="return devolve um valor. Depois voce pode mostrar esse valor com print.",
                retry_text="return a + b devolve a soma para quem chamou add(a, b).",
            ),
            check(
                "Criar uma funcao com def:",
                "nao executa a funcao sozinho",
                "executa sempre duas vezes",
                "apaga os parametros",
                "Certo. Depois de criar, ainda precisa chamar.",
                "Ainda nao. def cria a funcao; a chamada executa.",
            ),
            check(
                "return serve para:",
                "devolver um valor da funcao",
                "mostrar texto direto na tela sempre",
                "criar uma lista",
                "Certo. return entrega um resultado.",
                "Quase. print mostra; return devolve.",
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
