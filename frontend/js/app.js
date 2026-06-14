const ASSETS = {
  idle: "./assets/mompy_idle.png",
  talk1: "./assets/mompy_talk_1.png",
  talk2: "./assets/mompy_talk_2.png",
  success: "./assets/mompy_happy.png",
  error: "./assets/mompy_sad.png",
  blank: "./assets/desligando5.png",
  shutdown: "./assets/desligando5.png",
  shutdown2: "./assets/desligando2.png",
  shutdown3: "./assets/desligando3.png",
  shutdown4: "./assets/desligando4.png",
  clickSfx: "./assets/audio/click.wav",
  runSfx: "./assets/audio/run.wav",
  successSfx: "./assets/audio/success.wav",
  errorSfx: "./assets/audio/error.wav",
  shutdownSfx: "./assets/audio/shutdown.wav",
  ambientLoop: "./assets/audio/mompy_crt_ambient_loop_minimal.wav",
};

const USER_PROFILE_KEY = "mompy_user_profile_v1";
const PROGRESS_KEY = "mompy_progress_v1";
const BRIEFING_PROGRESS_KEY = "mompy_briefing_progress_v1";
const DEFAULT_USER_NAME = "Guest";
const PLANNED_TOTAL_MISSIONS = 30;
const BASE_MISSION_XP = 35;
const MISSION_LEVEL_XP_STEP = 5;

const defaultProgressState = {
  currentMissionIndex: 0,
  completedMissionIds: [],
  totalXp: 0,
  lastUpdatedAt: null,
};

const currentUser = {
  name: DEFAULT_USER_NAME,
  level: "01 · Beginner",
  levelNumber: 1,
  xp: 0,
  xpToNextLevel: 100,
  missionsCompleted: 0,
  totalMissions: PLANNED_TOTAL_MISSIONS,
};

const settingsState = {
  ambientMusic: true,
  musicVolume: 10,
  soundEffects: true,
  effectsVolume: 45,
  crtBrightness: 70,
  mompyAnimations: true,
};

let pythonBackendConnected = false;

const PYTHON_HTTP_ROUTES = {
  get_bootstrap_state: { method: "GET", path: "/api/bootstrap" },
  validate_mission: { method: "POST", path: "/api/validate", body: ([missionId, userCode]) => ({ mission_id: missionId, user_code: userCode }) },
  complete_mission: { method: "POST", path: "/api/complete", body: ([missionId]) => ({ mission_id: missionId }) },
  reset_progress: { method: "POST", path: "/api/reset", body: () => ({}) },
  save_profile: { method: "POST", path: "/api/profile/save", body: ([profile]) => ({ profile }) },
  logout_profile: { method: "POST", path: "/api/profile/logout", body: () => ({}) },
};

function getPythonBackend() {
  return window.pywebview?.api || null;
}

async function callPythonBackend(method, ...args) {
  const backend = getPythonBackend();

  if (backend && typeof backend[method] === "function") {
    try {
      const result = await backend[method](...args);
      pythonBackendConnected = true;
      return result;
    } catch (error) {
      console.warn(`Mompy Python backend call failed: ${method}`, error);
    }
  }

  const route = PYTHON_HTTP_ROUTES[method];
  const canUseHttpBackend = route && ["http:", "https:"].includes(window.location.protocol);

  if (!canUseHttpBackend) {
    return null;
  }

  try {
    const response = await fetch(route.path, {
      method: route.method,
      headers: route.method === "POST" ? { "Content-Type": "application/json" } : undefined,
      body: route.method === "POST" ? JSON.stringify(route.body(args)) : undefined,
    });

    if (!response.ok) {
      return null;
    }

    const result = await response.json();
    pythonBackendConnected = true;
    return result;
  } catch (error) {
    console.warn(`Mompy Python HTTP backend call failed: ${method}`, error);
    return null;
  }
}

function applyPythonProgress(progress) {
  if (!progress || typeof progress !== "object") {
    return;
  }

  const completedIds = progress.completed_mission_ids || progress.completedMissionIds;
  const missionIndex = progress.current_mission_index ?? progress.currentMissionIndex;
  const xp = progress.total_xp ?? progress.totalXp;

  if (Number.isInteger(missionIndex)) {
    currentMissionIndex = clampMissionIndex(missionIndex);
  }

  if (Array.isArray(completedIds)) {
    completedMissionIds = sanitizeCompletedMissionIds(completedIds);
  }

  if (Number.isFinite(Number(xp))) {
    totalXp = Number(xp);
  } else {
    totalXp = calculateXpFromCompletedMissions(completedMissionIds);
  }

  updateProgressUI();
}

function applyPythonProfile(profile) {
  if (!profile || typeof profile !== "object" || !profile.name) {
    return;
  }

  applyUserProfile({ firstName: profile.name });
  renderStartUserInfo();
}

function normalizePythonMission(mission) {
  return {
    id: mission.id,
    level: mission.level,
    title: mission.title,
    description: mission.description,
    objective: mission.objective,
    starterCode: mission.starterCode ?? mission.starter_code ?? "",
    expectedOutput: mission.expectedOutput ?? mission.expected_output ?? "",
    help: mission.help,
    blocks: mission.blocks,
    xp: mission.xp,
  };
}

function applyPythonMissions(pythonMissions) {
  if (!Array.isArray(pythonMissions) || pythonMissions.length === 0) {
    return;
  }

  missions.splice(0, missions.length, ...pythonMissions.map(normalizePythonMission));
  currentMissionIndex = clampMissionIndex(currentMissionIndex);
}

async function syncPythonBackendState() {
  const state = await callPythonBackend("get_bootstrap_state");

  if (!state) {
    return;
  }

  applyPythonMissions(state.missions);
  applyPythonProfile(state.profile);
  applyPythonProgress(state.progress);

  const codeEditor = document.getElementById("codeEditor");
  if (codeEditor) {
    renderMission(currentMission());
    codeEditor.value = currentMission().starterCode || codeEditor.value;
    updateLineNumbers();
  }
}

function schedulePythonBackendSync() {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", syncPythonBackendState, { once: true });
    return;
  }

  setTimeout(syncPythonBackendState, 0);
}

document.addEventListener("pywebviewready", () => {
  schedulePythonBackendSync();
});

if (["http:", "https:"].includes(window.location.protocol)) {
  schedulePythonBackendSync();
}

const learningBriefings = [
  {
    id: "briefing_001",
    title: "Preparação do Bloco 01",
    subtitle: "Primeiros comandos em Python",
    beforeMissionIndex: 0,
    missionsRange: "1-5",
    steps: [
      {
        type: "lesson",
        title: "O que é Python?",
        text: "Python é uma linguagem de programação. Você escreve instruções, e o computador executa uma por uma.",
        retryText: "Pense em Python como uma forma de conversar com o computador por comandos escritos. Cada comando precisa ser claro.",
      },
      {
        type: "lesson",
        title: "Instruções",
        text: "Uma instrução é uma ordem pequena. O computador não adivinha intenção. Ele segue exatamente o que foi escrito.",
        retryText: "Uma linha de código pode ser como uma ordem: faça isso agora. Se a ordem estiver errada, o resultado também sai errado.",
      },
      {
        type: "check",
        question: "Python é usado para:",
        options: [
          { label: "A", text: "escrever instruções para o computador", correct: true },
          { label: "B", text: "decorar a tela do computador", correct: false },
          { label: "C", text: "ligar cabos físicos", correct: false },
        ],
        successText: "Certo. Python permite escrever instruções para o computador executar.",
        failText: "Quase. Python não é decoração nem cabo físico. É uma linguagem para escrever instruções.",
      },
      {
        type: "lesson",
        title: "Texto e aspas",
        text: "Quando queremos que Python trate algo como texto, normalmente usamos aspas. As aspas dizem: isto é uma mensagem.",
        retryText: "Sem aspas, Python tenta entender a palavra como nome de alguma coisa. Com aspas, ele entende como texto.",
      },
      {
        type: "lesson",
        title: "Mostrar na tela",
        text: "Uma das primeiras ideias é pedir que o programa mostre uma mensagem. Em Python, print é o comando básico para isso.",
        retryText: "print é uma forma simples de enviar uma mensagem para o console. Ele ajuda você a ver o resultado do programa.",
      },
    ],
  },
  {
    id: "briefing_002",
    title: "Preparação do Bloco 02",
    subtitle: "Variáveis e valores",
    beforeMissionIndex: 5,
    missionsRange: "6-10",
    steps: [
      {
        type: "lesson",
        title: "Guardar informação",
        text: "Uma variável é um nome que guarda um valor. Você usa esse nome depois para recuperar a informação.",
        retryText: "Imagine uma etiqueta em uma caixa. A etiqueta é o nome da variável. O que está dentro é o valor.",
      },
      {
        type: "lesson",
        title: "Atribuição",
        text: "Em Python, o sinal de igual coloca um valor dentro de um nome. Isso se chama atribuição.",
        retryText: "Quando você escreve nome = valor, está dizendo: guarde este valor neste nome.",
      },
      {
        type: "check",
        question: "Em uma variável, o sinal = significa:",
        options: [
          { label: "A", text: "guardar um valor em um nome", correct: true },
          { label: "B", text: "mostrar uma tela", correct: false },
          { label: "C", text: "apagar o programa", correct: false },
        ],
        successText: "Certo. O sinal de igual atribui um valor a um nome.",
        failText: "Ainda não. Aqui o igual serve para guardar um valor em uma variável.",
      },
      {
        type: "lesson",
        title: "Usar o valor",
        text: "Depois que uma variável existe, você pode usar o nome dela em comandos. O Python busca o valor guardado.",
        retryText: "Você não precisa repetir o valor toda hora. Use o nome da variável, e Python pega o valor dela.",
      },
    ],
  },
  {
    id: "briefing_003",
    title: "Preparação do Bloco 03",
    subtitle: "Decisões",
    beforeMissionIndex: 10,
    missionsRange: "11-15",
    steps: [
      {
        type: "lesson",
        title: "Condição",
        text: "Uma condição é uma pergunta com resposta verdadeira ou falsa. Programas usam isso para escolher caminhos.",
        retryText: "Pense em uma porta: se a condição for verdadeira, o programa entra. Se for falsa, ele segue outro caminho.",
      },
      {
        type: "lesson",
        title: "If",
        text: "O if executa um bloco apenas quando a condição é verdadeira. A indentação mostra o que pertence a esse bloco.",
        retryText: "if significa se. Se algo for verdadeiro, execute as linhas indentadas abaixo.",
      },
      {
        type: "check",
        question: "Um if serve para:",
        options: [
          { label: "A", text: "tomar uma decisão no programa", correct: true },
          { label: "B", text: "trocar a fonte do editor", correct: false },
          { label: "C", text: "criar som ambiente", correct: false },
        ],
        successText: "Certo. O if cria caminhos diferentes no programa.",
        failText: "Quase. O if não muda o visual. Ele decide se um bloco deve executar.",
      },
      {
        type: "lesson",
        title: "Comparações",
        text: "Comparações como maior que, menor que ou igual a geram respostas verdadeiras ou falsas.",
        retryText: "Comparar é perguntar: isto é maior? isto é igual? A resposta ajuda o programa a decidir.",
      },
    ],
  },
  {
    id: "briefing_004",
    title: "Preparação do Bloco 04",
    subtitle: "Repetições",
    beforeMissionIndex: 15,
    missionsRange: "16-20",
    steps: [
      {
        type: "lesson",
        title: "Repetir ações",
        text: "Programas muitas vezes precisam repetir uma ação. Loops evitam copiar a mesma linha várias vezes.",
        retryText: "Quando uma tarefa se repete, um loop ajuda o computador a fazer isso em sequência.",
      },
      {
        type: "lesson",
        title: "For",
        text: "O for percorre uma sequência. A cada volta, ele trabalha com um item ou número da sequência.",
        retryText: "Pense no for como uma esteira: cada item passa uma vez, e o bloco de código roda para ele.",
      },
      {
        type: "check",
        question: "Um loop ajuda principalmente a:",
        options: [
          { label: "A", text: "repetir ações sem copiar código", correct: true },
          { label: "B", text: "desligar o monitor", correct: false },
          { label: "C", text: "mudar o nome do usuário", correct: false },
        ],
        successText: "Certo. Loops repetem ações de forma organizada.",
        failText: "Ainda não. Loop é sobre repetição de código, não sobre interface.",
      },
      {
        type: "lesson",
        title: "Indentação",
        text: "As linhas indentadas pertencem ao loop. Isso mostra ao Python o que deve repetir.",
        retryText: "A indentação é o recuo no começo da linha. Ela marca o bloco que fica dentro do loop.",
      },
    ],
  },
  {
    id: "briefing_005",
    title: "Preparação do Bloco 05",
    subtitle: "Listas",
    beforeMissionIndex: 20,
    missionsRange: "21-25",
    steps: [
      {
        type: "lesson",
        title: "Vários valores",
        text: "Uma lista guarda vários valores em uma ordem. Cada valor é um item.",
        retryText: "Lista é como uma prateleira: vários itens ficam juntos, cada um em uma posição.",
      },
      {
        type: "lesson",
        title: "Posição",
        text: "Itens de lista têm posição. Em Python, a primeira posição costuma ser zero.",
        retryText: "O primeiro item fica na posição 0, o segundo na posição 1, e assim por diante.",
      },
      {
        type: "check",
        question: "Uma lista serve para:",
        options: [
          { label: "A", text: "guardar vários valores em ordem", correct: true },
          { label: "B", text: "salvar senha online", correct: false },
          { label: "C", text: "aumentar volume do som", correct: false },
        ],
        successText: "Certo. Listas organizam vários valores.",
        failText: "Quase. Lista é uma estrutura para guardar vários valores.",
      },
    ],
  },
  {
    id: "briefing_006",
    title: "Preparação do Bloco 06",
    subtitle: "Funções",
    beforeMissionIndex: 25,
    missionsRange: "26-30",
    steps: [
      {
        type: "lesson",
        title: "Código com nome",
        text: "Uma função é um bloco de código com nome. Você cria uma vez e chama quando precisar.",
        retryText: "Função é como uma ferramenta: tem um nome e executa uma tarefa quando você chama.",
      },
      {
        type: "lesson",
        title: "Organização",
        text: "Funções ajudam a evitar repetição e deixam o programa mais organizado.",
        retryText: "Quando uma tarefa aparece muitas vezes, colocar essa tarefa em uma função deixa tudo mais limpo.",
      },
      {
        type: "check",
        question: "Uma função ajuda a:",
        options: [
          { label: "A", text: "organizar e reutilizar código", correct: true },
          { label: "B", text: "criar uma imagem nova", correct: false },
          { label: "C", text: "instalar Python sozinha", correct: false },
        ],
        successText: "Certo. Funções organizam tarefas reutilizáveis.",
        failText: "Ainda não. Função é sobre organizar código com nome.",
      },
    ],
  },
];

const missions = [
  {
    id: "mission_001",
    level: 1,
    title: "Mission 01 — First Output",
    description: "Primeiro passo: faça o programa escrever uma mensagem no console.",
    objective: "Use print() para mostrar exatamente: Hello, Mompy!",
    starterCode: "# escreva aqui\n",
    expectedOutput: "Hello, Mompy!",
    help: 'Use aspas dentro do print: print("Hello, Mompy!")',
    blocks: [
      [
        {
          text: "Primeiro passo: faça o programa escrever uma mensagem no console.",
        },
      ],
      [
        { text: "Escreva um " },
        { text: "print()", tag: "code" },
        { text: " que mostre exatamente: " },
        { text: "Hello, Mompy!", tag: "strong" },
      ],
    ],
  },
  {
    id: "mission_002",
    level: 2,
    title: "Mission 02 — Variable",
    description: "Variáveis guardam valores para você usar depois.",
    objective: 'Crie name = "Mompy" e depois mostre name com print().',
    starterCode: 'name = "Mompy"\n',
    expectedOutput: "Mompy",
    help: 'Depois de criar a variável, use print(name). Não coloque name entre aspas no print.',
  },
  {
    id: "mission_003",
    level: 3,
    title: "Mission 03 — Sum",
    description: "Python consegue fazer contas simples direto no código.",
    objective: "Some 2 + 3 e mostre o resultado no console.",
    starterCode: "a = 2\nb = 3\n",
    expectedOutput: "5",
    help: "Você pode usar print(a + b) depois de criar as variáveis.",
  },
  {
    id: "mission_004",
    level: 4,
    title: "Mission 04 — If",
    description: "O if executa um bloco de código apenas quando uma condição é verdadeira.",
    objective: 'Use if para mostrar exatamente: Ready',
    starterCode: "power = True\n",
    expectedOutput: "Ready",
    help: 'Use if power: e, dentro dele, print("Ready").',
  },
  {
    id: "mission_005",
    level: 5,
    title: "Mission 05 — For Loop",
    description: "O for repete comandos para uma sequência de valores.",
    objective: "Use range(3) para mostrar 0, 1 e 2.",
    starterCode: "for i in range(3):\n    ",
    expectedOutput: "0\n1\n2",
    help: "Dentro do for, use print(i). A linha do print precisa ficar indentada.",
  },
  {
    id: "mission_006",
    level: 6,
    title: "Mission 06 — List Item",
    description: "Listas guardam vários valores em ordem.",
    objective: 'Crie uma lista com "onion", "terminal", "python" e mostre o segundo item.',
    starterCode: 'items = ["onion", "terminal", "python"]\n',
    expectedOutput: "terminal",
    help: "O primeiro item é índice 0. O segundo item é items[1].",
  },
  {
    id: "mission_007",
    level: 7,
    title: "Mission 07 — Length",
    description: "len() conta quantos itens ou caracteres existem em um valor.",
    objective: 'Mostre o tamanho da palavra "Mompy".',
    starterCode: 'word = "Mompy"\n',
    expectedOutput: "5",
    help: "Use print(len(word)) ou print(len(\"Mompy\")).",
  },
  {
    id: "mission_008",
    level: 8,
    title: "Mission 08 — Function",
    description: "Funções guardam uma pequena tarefa para reutilizar depois.",
    objective: 'Crie greet(user) e mostre: Hello, Mompy',
    starterCode: "def greet(user):\n    ",
    expectedOutput: "Hello, Mompy",
    help: 'Retorne ou imprima "Hello, " + user, depois chame greet("Mompy").',
  },
  {
    id: "mission_009",
    level: 9,
    title: "Mission 09 — Boolean",
    description: "Booleanos representam verdadeiro ou falso.",
    objective: "Crie is_ready = True e mostre esse valor.",
    starterCode: "is_ready = True\n",
    expectedOutput: "True",
    help: "Use print(is_ready). Em Python, True começa com T maiúsculo.",
  },
  {
    id: "mission_010",
    level: 10,
    title: "Mission 10 — Uppercase",
    description: "Strings têm métodos que transformam texto.",
    objective: 'Transforme "mompy" em letras maiúsculas.',
    starterCode: 'name = "mompy"\n',
    expectedOutput: "MOMPY",
    help: "Use name.upper() dentro do print.",
  },
  {
    id: "mission_011",
    level: 11,
    title: "Mission 11 — Append",
    description: "append() adiciona um item no final de uma lista.",
    objective: "Adicione 4 em [1, 2, 3] e mostre a lista.",
    starterCode: "numbers = [1, 2, 3]\n",
    expectedOutput: "[1, 2, 3, 4]",
    help: "Use numbers.append(4), depois print(numbers).",
  },
  {
    id: "mission_012",
    level: 12,
    title: "Mission 12 — Dictionary",
    description: "Dicionários guardam valores com nomes de chave.",
    objective: 'Crie um dicionário com name = "Mompy" e mostre esse valor.',
    starterCode: 'profile = {"name": "Mompy"}\n',
    expectedOutput: "Mompy",
    help: 'Use print(profile["name"]).',
  },
  {
    id: "mission_013",
    level: 13,
    title: "Mission 13 — While",
    description: "while repete enquanto uma condição continuar verdadeira.",
    objective: "Use while para mostrar 0, 1 e 2.",
    starterCode: "count = 0\nwhile count < 3:\n    ",
    expectedOutput: "0\n1\n2",
    help: "Dentro do while, use print(count) e depois count += 1.",
  },
  {
    id: "mission_014",
    level: 14,
    title: "Mission 14 — F-String",
    description: "f-strings colocam variáveis dentro de textos.",
    objective: 'Com user = "Mackson", mostre: Hello, Mackson',
    starterCode: 'user = "Mackson"\n',
    expectedOutput: "Hello, Mackson",
    help: 'Use print(f"Hello, {user}").',
  },
  {
    id: "mission_015",
    level: 15,
    title: "Mission 15 — Comparison",
    description: "Comparações retornam True ou False.",
    objective: "Mostre se 10 é maior que 3.",
    starterCode: "",
    expectedOutput: "True",
    help: "Use print(10 > 3).",
  },
  {
    id: "mission_016",
    level: 16,
    title: "Mission 16 — Modulo",
    description: "O operador % mostra o resto de uma divisão.",
    objective: "Mostre o resto de 8 dividido por 2.",
    starterCode: "",
    expectedOutput: "0",
    help: "Use print(8 % 2).",
  },
  {
    id: "mission_017",
    level: 17,
    title: "Mission 17 — List Comprehension",
    description: "List comprehensions criam listas novas em uma linha.",
    objective: "Dobre [1, 2, 3] e mostre [2, 4, 6].",
    starterCode: "numbers = [1, 2, 3]\n",
    expectedOutput: "[2, 4, 6]",
    help: "Use print([n * 2 for n in numbers]).",
  },
  {
    id: "mission_018",
    level: 18,
    title: "Mission 18 — Return Value",
    description: "Uma função pode devolver um resultado com return.",
    objective: "Crie add(a, b) e mostre add(2, 3).",
    starterCode: "def add(a, b):\n    ",
    expectedOutput: "5",
    help: "A função deve retornar a + b. Depois use print(add(2, 3)).",
  },
  {
    id: "mission_019",
    level: 19,
    title: "Mission 19 — Split",
    description: "split() separa uma frase em uma lista de palavras.",
    objective: 'Separe "Python is fun" em palavras e mostre a lista.',
    starterCode: 'phrase = "Python is fun"\n',
    expectedOutput: "['Python', 'is', 'fun']",
    help: "Use print(phrase.split()).",
  },
  {
    id: "mission_020",
    level: 20,
    title: "Mission 20 — Small Loop",
    description: "Você já consegue combinar loop, texto e método de string.",
    objective: 'Mostre as letras de "py" em maiúsculas, uma por linha.',
    starterCode: 'for letter in "py":\n    ',
    expectedOutput: "P\nY",
    help: "Dentro do for, use print(letter.upper()).",
  },
];

let currentMissionIndex = 0;
let completedMissionIds = [];
let totalXp = 0;
let completedBriefingIds = [];
let skippedBriefingIds = [];

const loadingScreen = document.querySelector("#loadingScreen");
const loadingBranding = document.querySelector("#loadingBranding");
const loadingProgress = document.querySelector("#loadingProgress");
const machine = document.querySelector(".machine");
const startScreen = document.querySelector("#startScreen");
const startMompySprite = document.querySelector("#startMompySprite");
const startButton = document.querySelector("#startButton");
const continueButton = document.querySelector("#continueButton");
const startUserName = document.querySelector("#startUserName");
const startUserLevel = document.querySelector("#startUserLevel");
const startMissionCount = document.querySelector("#startMissionCount");
const startMompyTerminal = document.querySelector("#startMompyTerminal");
const startMompyTerminalOutput = document.querySelector("#startMompyTerminalOutput");
const onboardingOverlay = document.querySelector("#onboardingOverlay");
const onboardingTerminalOutput = document.querySelector("#onboardingTerminalOutput");
const onboardingNameInput = document.querySelector("#onboardingNameInput");
const onboardingContinueButton = document.querySelector("#onboardingContinueButton");
const onboardingError = document.querySelector("#onboardingError");
const sprite = document.querySelector("#mompySprite");
const missionCopy = document.querySelector("#missionCopy");
const levelValue = document.querySelector("#levelValue");
const levelFill = document.querySelector("#levelFill");
const editor = document.querySelector("#codeEditor");
const lineNumbers = document.querySelector("#lineNumbers");
const output = document.querySelector("#outputConsole");
const runButton = document.querySelector("#runButton");
const backButton = document.querySelector("#backButton");
const helpButton = document.querySelector("#helpButton");
const settingsButton = document.querySelector("#settingsButton");
const fullscreenButton = document.querySelector("#fullscreenButton");
const modalBackdrop = document.querySelector("#modalBackdrop");
const modalTitle = document.querySelector("#modalTitle");
const modalBody = document.querySelector("#modalBody");
const modalActions = document.querySelector("#modalActions");
const modalCloseButton = document.querySelector("#modalCloseButton");
const mompyScreenMessage = document.querySelector("#mompyScreenMessage");
const repeatMissionButton = document.querySelector("#repeatMissionButton");
const nextMissionButton = document.querySelector("#nextMissionButton");

let talkTimer = null;
let settleTimer = null;
let talkFrame = false;
let lastFocusedElement = null;
let typingTimer = null;
let typingToken = 0;
let trainingStarted = false;
let missionCompleted = false;
let completionTimer = null;
let completionPending = false;
let startScreenAnimationActive = false;
let startMompyTerminalTimer = null;
let startMompyTypingTimer = null;
let startMompyTerminalToken = 0;
let startTerminalExampleIndex = 0;
let loadingInterval = null;
let loadingDoneTimer = null;
let hepteraktBootTimers = [];
let mompyShutdownAnimating = false;
let mompyShutdownTimers = [];
let currentProfile = null;
let onboardingActive = false;
let onboardingTypingTimer = null;
let onboardingDelayTimer = null;
let onboardingToken = 0;
let activeBriefingId = null;
let activeBriefingStepIndex = 0;
let activeBriefingRetry = false;
let briefingFinalTimer = null;

const startTerminalWelcome = [
  '>>> print("Welcome")',
  "Welcome",
];

const startTerminalExamples = [
  [
    '>>> name = "Mompy"',
    ">>> print(name)",
    "Mompy",
  ],
  [
    ">>> for i in range(3):",
    "...     print(i)",
    "0",
    "1",
    "2",
  ],
  [
    ">>> def greet(user):",
    '...     return f"Hello, {user}"',
    '>>> greet("Mackson")',
    "'Hello, Mackson'",
  ],
  [
    ">>> numbers = [1, 2, 3, 4]",
    ">>> [n * 2 for n in numbers]",
    "[2, 4, 6, 8]",
  ],
];

const onboardingIntroLines = [
  '>>> print("Bem-vindo ao Mompy")',
  "Bem-vindo ao Mompy",
  '>>> nome = input("Qual é o seu primeiro nome? ")',
];

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function clampAudioVolume(value, fallback) {
  if (value === null || value === undefined || value === "") {
    return fallback;
  }

  const number = Number(value);

  if (!Number.isFinite(number)) {
    return fallback;
  }

  const normalized = number > 1 ? number / 100 : number;
  return Math.min(1, Math.max(0, normalized));
}

const audioManager = {
  sfxEnabled: true,
  musicEnabled: true,
  sfxVolume: 0.45,
  musicVolume: 0.1,
  sounds: {},
  music: null,
  unlocked: false,
  ambientFadeTimer: null,

  init() {
    this.loadSettings();
    this.sounds = {
      click: new Audio(ASSETS.clickSfx),
      run: new Audio(ASSETS.runSfx),
      success: new Audio(ASSETS.successSfx),
      error: new Audio(ASSETS.errorSfx),
      shutdown: new Audio(ASSETS.shutdownSfx),
    };

    Object.values(this.sounds).forEach((sound) => {
      sound.preload = "auto";
    });

    this.music = new Audio(ASSETS.ambientLoop);
    this.music.loop = true;
    this.music.preload = "auto";
    this.music.volume = 0;
  },

  unlock() {
    if (this.unlocked) {
      return;
    }

    this.unlocked = true;

    Object.values(this.sounds).forEach((sound) => {
      try {
        sound.load();
      } catch (error) {
        console.warn(error);
      }
    });

    if (this.music) {
      try {
        this.music.load();
      } catch (error) {
        console.warn(error);
      }
    }

    if (!trainingStarted && loadingScreen?.hidden) {
      this.startAmbientMusic();
    }
  },

  playSfx(name) {
    if (!this.sfxEnabled || !this.unlocked) {
      return;
    }

    const baseSound = this.sounds[name];

    if (!baseSound) {
      return;
    }

    const sound = baseSound.cloneNode(true);
    sound.volume = this.sfxVolume;
    sound.play().catch(() => {});
  },

  playClick() {
    this.playSfx("click");
  },

  playRun() {
    this.playSfx("run");
  },

  playSuccess() {
    this.playSfx("success");
  },

  playError() {
    this.playSfx("error");
  },

  playShutdown() {
    this.playSfx("shutdown");
  },

  startAmbientMusic() {
    if (!this.music || !this.musicEnabled || !this.unlocked || trainingStarted || !loadingScreen?.hidden) {
      return;
    }

    this.fadeInAmbient();
  },

  stopAmbientMusic() {
    this.fadeOutAmbient();
  },

  fadeInAmbient() {
    if (!this.music) {
      return;
    }

    clearInterval(this.ambientFadeTimer);

    const targetVolume = this.musicVolume;

    if (targetVolume <= 0) {
      return;
    }

    this.music.loop = true;
    this.music.play().catch(() => {});
    this.ambientFadeTimer = setInterval(() => {
      if (!this.music || trainingStarted || !this.musicEnabled) {
        this.fadeOutAmbient();
        return;
      }

      this.music.volume = Math.min(targetVolume, this.music.volume + 0.01);

      if (this.music.volume >= targetVolume) {
        clearInterval(this.ambientFadeTimer);
        this.ambientFadeTimer = null;
      }
    }, 70);
  },

  fadeOutAmbient() {
    if (!this.music) {
      return;
    }

    clearInterval(this.ambientFadeTimer);
    this.ambientFadeTimer = setInterval(() => {
      if (!this.music) {
        clearInterval(this.ambientFadeTimer);
        this.ambientFadeTimer = null;
        return;
      }

      this.music.volume = Math.max(0, this.music.volume - 0.015);

      if (this.music.volume <= 0.001) {
        this.music.pause();
        this.music.volume = 0;
        clearInterval(this.ambientFadeTimer);
        this.ambientFadeTimer = null;
      }
    }, 45);
  },

  setSfxEnabled(value) {
    this.sfxEnabled = Boolean(value);
    settingsState.soundEffects = this.sfxEnabled;
    this.saveSettings();
  },

  setMusicEnabled(value) {
    this.musicEnabled = Boolean(value);
    settingsState.ambientMusic = this.musicEnabled;
    this.saveSettings();

    if (this.musicEnabled) {
      this.startAmbientMusic();
    } else {
      this.stopAmbientMusic();
    }
  },

  setSfxVolume(value) {
    this.sfxVolume = clampAudioVolume(value, this.sfxVolume);
    settingsState.effectsVolume = Math.round(this.sfxVolume * 100);
    this.saveSettings();
  },

  setMusicVolume(value) {
    this.musicVolume = clampAudioVolume(value, this.musicVolume);
    settingsState.musicVolume = Math.round(this.musicVolume * 100);

    if (this.music && !this.music.paused) {
      this.music.volume = Math.min(this.music.volume, this.musicVolume);
    }

    this.saveSettings();
  },

  saveSettings() {
    try {
      localStorage.setItem("mompy_music_enabled", String(this.musicEnabled));
      localStorage.setItem("mompy_music_volume", String(this.musicVolume));
      localStorage.setItem("mompy_sfx_enabled", String(this.sfxEnabled));
      localStorage.setItem("mompy_sfx_volume", String(this.sfxVolume));
    } catch (error) {
      console.warn(error);
    }
  },

  loadSettings() {
    try {
      const storedMusicEnabled = localStorage.getItem("mompy_music_enabled");
      const storedMusicVolume = localStorage.getItem("mompy_music_volume");
      const storedSfxEnabled = localStorage.getItem("mompy_sfx_enabled");
      const storedSfxVolume = localStorage.getItem("mompy_sfx_volume");

      this.musicEnabled = storedMusicEnabled === null ? true : storedMusicEnabled === "true";
      this.musicVolume = clampAudioVolume(storedMusicVolume, 0.1);
      this.sfxEnabled = storedSfxEnabled === null ? true : storedSfxEnabled === "true";
      this.sfxVolume = clampAudioVolume(storedSfxVolume, 0.45);
    } catch (error) {
      console.warn(error);
    }

    settingsState.ambientMusic = this.musicEnabled;
    settingsState.musicVolume = Math.round(this.musicVolume * 100);
    settingsState.soundEffects = this.sfxEnabled;
    settingsState.effectsVolume = Math.round(this.sfxVolume * 100);
  },
};

function showLoadingScreen() {
  if (!loadingScreen) {
    return;
  }

  clearInterval(loadingInterval);
  clearTimeout(loadingDoneTimer);
  loadingScreen.hidden = false;
  loadingScreen.classList.remove("is-branding", "is-branding-out", "is-loading");

  if (loadingProgress) {
    loadingProgress.style.width = "0%";
  }
}

function hideLoadingScreen() {
  clearInterval(loadingInterval);
  clearTimeout(loadingDoneTimer);
  loadingInterval = null;
  loadingDoneTimer = null;

  if (loadingScreen) {
    loadingScreen.hidden = true;
    loadingScreen.classList.remove("is-branding", "is-branding-out", "is-loading");
  }
}

function clearHepteraktBootTimers() {
  hepteraktBootTimers.forEach((timer) => clearTimeout(timer));
  hepteraktBootTimers = [];
}

function showHepteraktBoot(onComplete) {
  if (!loadingScreen || !loadingBranding) {
    onComplete();
    return;
  }

  clearHepteraktBootTimers();
  showLoadingScreen();
  audioManager.stopAmbientMusic();
  stopStartScreenMompyAnimation();
  loadingScreen.classList.add("is-branding");

  hepteraktBootTimers.push(
    setTimeout(() => {
      loadingScreen.classList.add("is-branding-out");
    }, 1800),
  );

  hepteraktBootTimers.push(
    setTimeout(() => {
      hideHepteraktBoot();
      onComplete();
    }, 2500),
  );
}

function hideHepteraktBoot() {
  clearHepteraktBootTimers();

  if (loadingScreen) {
    loadingScreen.classList.remove("is-branding", "is-branding-out");
  }
}

function continueAfterHepteraktBoot() {
  if (!loadingScreen || !loadingProgress) {
    showStartScreen();
    return;
  }

  let value = 0;
  audioManager.stopAmbientMusic();
  showLoadingScreen();
  loadingScreen.classList.add("is-loading");
  stopStartScreenMompyAnimation();

  loadingInterval = setInterval(() => {
    value += Math.floor(Math.random() * 7) + 4;
    value = Math.min(value, 100);
    loadingProgress.style.width = `${value}%`;

    if (value >= 100) {
      clearInterval(loadingInterval);
      loadingInterval = null;

      loadingDoneTimer = setTimeout(() => {
        hideLoadingScreen();
        showStartScreen();
      }, 380);
    }
  }, 120);
}

function startLoadingSequence() {
  if (!loadingScreen || !loadingProgress) {
    showStartScreen();
    return;
  }

  showHepteraktBoot(continueAfterHepteraktBoot);
}

function currentMission() {
  return missions[currentMissionIndex];
}

function clampMissionIndex(index) {
  const number = Number(index);

  if (!Number.isInteger(number)) {
    return 0;
  }

  return Math.min(Math.max(number, 0), missions.length - 1);
}

function getCurrentMission() {
  return currentMission();
}

function xpRequiredForLevel(level) {
  if (level <= 1) {
    return 0;
  }

  return Math.floor(100 * Math.pow(level - 1, 1.6));
}

function getMissionXp(mission) {
  return BASE_MISSION_XP + ((mission.level || 1) - 1) * MISSION_LEVEL_XP_STEP;
}

function calculateXpFromCompletedMissions(ids) {
  const completedSet = new Set(ids);
  return missions.reduce((sum, mission) => {
    if (!completedSet.has(mission.id)) {
      return sum;
    }

    return sum + getMissionXp(mission);
  }, 0);
}

function getLevelTitle(level) {
  if (level >= 100) {
    return "Legend";
  }

  if (level >= 30) {
    return "Expert";
  }

  if (level >= 15) {
    return "Builder";
  }

  if (level >= 6) {
    return "Apprentice";
  }

  if (level >= 2) {
    return "Rookie";
  }

  return "Beginner";
}

function getUserLevelInfo(xp = totalXp) {
  let level = 1;

  while (level < 100 && xp >= xpRequiredForLevel(level + 1)) {
    level += 1;
  }

  const currentLevelXp = xpRequiredForLevel(level);
  const nextLevelXp = xpRequiredForLevel(level + 1);
  const levelProgress = nextLevelXp === currentLevelXp
    ? 100
    : ((xp - currentLevelXp) / (nextLevelXp - currentLevelXp)) * 100;

  return {
    level,
    title: getLevelTitle(level),
    label: `${String(level).padStart(2, "0")} · ${getLevelTitle(level)}`,
    currentLevelXp,
    nextLevelXp,
    xpIntoLevel: Math.max(0, xp - currentLevelXp),
    xpToNextLevel: Math.max(0, nextLevelXp - xp),
    progress: Math.min(100, Math.max(0, levelProgress)),
  };
}

function sanitizeCompletedMissionIds(ids) {
  if (!Array.isArray(ids)) {
    return [];
  }

  const validIds = new Set(missions.map((mission) => mission.id));
  return [...new Set(ids.filter((id) => validIds.has(id)))];
}

function sanitizeBriefingIds(ids) {
  if (!Array.isArray(ids)) {
    return [];
  }

  const validIds = new Set(learningBriefings.map((briefing) => briefing.id));
  return [...new Set(ids.filter((id) => validIds.has(id)))];
}

function loadBriefingProgress() {
  try {
    const rawProgress = localStorage.getItem(BRIEFING_PROGRESS_KEY);

    if (!rawProgress) {
      completedBriefingIds = [];
      skippedBriefingIds = [];
      return;
    }

    const progress = JSON.parse(rawProgress);
    completedBriefingIds = sanitizeBriefingIds(progress.completedBriefingIds);
    skippedBriefingIds = sanitizeBriefingIds(progress.skippedBriefingIds);
  } catch (error) {
    console.warn(error);
    completedBriefingIds = [];
    skippedBriefingIds = [];
  }
}

function saveBriefingProgress() {
  try {
    localStorage.setItem(
      BRIEFING_PROGRESS_KEY,
      JSON.stringify({
        completedBriefingIds: [...completedBriefingIds],
        skippedBriefingIds: [...skippedBriefingIds],
      }),
    );
  } catch (error) {
    console.warn(error);
  }
}

function resetBriefingProgress() {
  completedBriefingIds = [];
  skippedBriefingIds = [];
  activeBriefingId = null;
  activeBriefingStepIndex = 0;
  activeBriefingRetry = false;
  clearTimeout(briefingFinalTimer);

  try {
    localStorage.removeItem(BRIEFING_PROGRESS_KEY);
  } catch (error) {
    console.warn(error);
  }
}

function loadProgress() {
  try {
    const rawProgress = localStorage.getItem(PROGRESS_KEY);

    if (!rawProgress) {
      currentMissionIndex = defaultProgressState.currentMissionIndex;
      completedMissionIds = [...defaultProgressState.completedMissionIds];
      totalXp = defaultProgressState.totalXp;
      updateProgressUI();
      return { ...defaultProgressState };
    }

    const progress = JSON.parse(rawProgress);
    currentMissionIndex = clampMissionIndex(progress.currentMissionIndex);
    completedMissionIds = sanitizeCompletedMissionIds(progress.completedMissionIds);
    totalXp = calculateXpFromCompletedMissions(completedMissionIds);
    updateProgressUI();
    return {
      currentMissionIndex,
      completedMissionIds: [...completedMissionIds],
      totalXp,
      lastUpdatedAt: progress.lastUpdatedAt || null,
    };
  } catch (error) {
    console.warn(error);
    currentMissionIndex = defaultProgressState.currentMissionIndex;
    completedMissionIds = [...defaultProgressState.completedMissionIds];
    totalXp = defaultProgressState.totalXp;
    updateProgressUI();
    return { ...defaultProgressState };
  }
}

function saveProgress() {
  const progress = {
    currentMissionIndex,
    completedMissionIds: [...completedMissionIds],
    totalXp,
    lastUpdatedAt: new Date().toISOString(),
  };

  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
  } catch (error) {
    console.warn(error);
  }

  updateProgressUI();
  return progress;
}

function resetProgress(options = {}) {
  currentMissionIndex = 0;
  completedMissionIds = [];
  totalXp = 0;
  missionCompleted = false;
  completionPending = false;
  clearTimeout(completionTimer);
  clearMompyScreenMessage();
  resetBriefingProgress();

  try {
    localStorage.removeItem(PROGRESS_KEY);
  } catch (error) {
    console.warn(error);
  }

  updateProgressUI();
  callPythonBackend("reset_progress").then(applyPythonProgress);

  if (trainingStarted && !options.keepMissionView) {
    openMissionOrBriefing({
      intro: false,
      outputMessage: "Progresso resetado. Missão 01 carregada.",
    });
  }
}

function hasSavedProgress() {
  try {
    return Boolean(localStorage.getItem(PROGRESS_KEY));
  } catch (error) {
    console.warn(error);
    return false;
  }
}

function updateProgressUI() {
  const levelInfo = getUserLevelInfo(totalXp);
  currentUser.level = levelInfo.label;
  currentUser.levelNumber = levelInfo.level;
  currentUser.xp = totalXp;
  currentUser.xpToNextLevel = levelInfo.xpToNextLevel;
  currentUser.missionsCompleted = completedMissionIds.length;
  currentUser.totalMissions = PLANNED_TOTAL_MISSIONS;
  renderStartUserInfo();

  if (trainingStarted) {
    updateLevelDisplay();
  }
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function getBriefingForMission(missionIndex) {
  return learningBriefings.find((briefing) => briefing.beforeMissionIndex === missionIndex) || null;
}

function shouldShowBriefingBeforeMission(missionIndex) {
  const briefing = getBriefingForMission(missionIndex);

  if (!briefing) {
    return false;
  }

  return !completedBriefingIds.includes(briefing.id) && !skippedBriefingIds.includes(briefing.id);
}

function findBriefingById(briefingId) {
  return learningBriefings.find((briefing) => briefing.id === briefingId) || null;
}

function renderMompyScreenPanel({ title, lines = [], actions = [], variant = "" }) {
  stopTalking();
  clearTimeout(settleTimer);
  machine.classList.remove("is-success", "is-error");
  sprite.src = ASSETS.blank;

  mompyScreenMessage.hidden = false;
  mompyScreenMessage.className = "mompy-screen-message is-briefing";

  if (variant) {
    mompyScreenMessage.classList.add(`is-${variant}`);
  }

  const text = document.createElement("div");
  text.className = "mompy-screen-text";

  if (title) {
    const heading = document.createElement("p");
    heading.className = "mompy-screen-heading";
    heading.textContent = title;
    text.append(heading);
  }

  lines.forEach((line) => {
    const paragraph = document.createElement("p");
    paragraph.textContent = line;
    text.append(paragraph);
  });

  const actionShell = document.createElement("div");
  actionShell.className = "mompy-screen-actions";

  if (actions.length > 2) {
    actionShell.classList.add("is-stacked");
  }

  actions.forEach((action) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = action.label;

    if (action.primary) {
      button.classList.add("is-primary");
    }

    button.addEventListener("click", () => {
      audioManager.playClick();
      action.onClick();
    });

    actionShell.append(button);
  });

  mompyScreenMessage.replaceChildren(text, actionShell);
}

function renderMompyCompletionPrompt() {
  mompyScreenMessage.className = "mompy-screen-message";

  const text = document.createElement("div");
  text.className = "mompy-screen-text";

  ["Missão concluída.", "Avançar?"].forEach((line) => {
    const paragraph = document.createElement("p");
    paragraph.textContent = line;
    text.append(paragraph);
  });

  const actionShell = document.createElement("div");
  actionShell.className = "mompy-screen-actions";

  const repeatButton = document.createElement("button");
  repeatButton.type = "button";
  repeatButton.textContent = "Repetir";
  repeatButton.addEventListener("click", repeatMission);

  const nextButton = document.createElement("button");
  nextButton.type = "button";
  nextButton.textContent = "Próxima missão";
  nextButton.addEventListener("click", goToNextMission);

  actionShell.append(repeatButton, nextButton);
  mompyScreenMessage.replaceChildren(text, actionShell);
}

function showLearningBriefing(briefingId) {
  const briefing = findBriefingById(briefingId);

  if (!briefing) {
    renderCurrentMission({ intro: true });
    return;
  }

  activeBriefingId = briefing.id;
  activeBriefingStepIndex = 0;
  activeBriefingRetry = false;
  clearTimeout(briefingFinalTimer);
  stopMissionTyping();
  clearMompyScreenMessage();
  setMissionActionsEnabled(false);
  setMompyState("briefing");
  editor.value = "";
  updateLineNumbers();
  output.textContent = "Mompy: Aula pronta.";
  renderBriefingIntro(briefing);
}

function renderBriefingIntro(briefing) {
  renderMompyScreenPanel({
    title: "Mompy",
    lines: [
      briefing.subtitle,
    ],
    actions: [
      {
        label: "Aprender",
        primary: true,
        onClick: () => {
          activeBriefingStepIndex = 0;
          activeBriefingRetry = false;
          renderBriefingStep(briefing, 0);
        },
      },
      {
        label: "Pular",
        onClick: () => skipBriefing(briefing.id),
      },
    ],
  });
}

function renderBriefingStep(briefing, stepIndex) {
  const step = briefing.steps[stepIndex];

  if (!step) {
    completeBriefing(briefing.id);
    return;
  }

  activeBriefingStepIndex = stepIndex;
  activeBriefingRetry = false;

  if (step.type === "check") {
    renderBriefingCheck(briefing, stepIndex);
    return;
  }

  setMompyState("briefing");
  renderMompyScreenPanel({
    title: step.title,
    lines: [step.text],
    actions: [
      {
        label: "Entendi",
        primary: true,
        onClick: handleBriefingUnderstood,
      },
      {
        label: "Não entendi",
        onClick: handleBriefingNotUnderstood,
      },
    ],
  });
}

function renderBriefingRetry(briefing, stepIndex) {
  const step = briefing.steps[stepIndex];

  if (!step) {
    completeBriefing(briefing.id);
    return;
  }

  activeBriefingRetry = true;
  setMompyState("briefing");
  renderMompyScreenPanel({
    title: step.title,
    lines: [step.retryText || step.text],
    actions: [
      {
        label: "Entendi",
        primary: true,
        onClick: handleBriefingUnderstood,
      },
      {
        label: "Não entendi",
        onClick: handleBriefingNotUnderstood,
      },
    ],
  });
}

function renderBriefingCheck(briefing, stepIndex, feedback = "") {
  const step = briefing.steps[stepIndex];

  if (!step) {
    completeBriefing(briefing.id);
    return;
  }

  activeBriefingStepIndex = stepIndex;
  setMompyState("briefing");
  renderMompyScreenPanel({
    title: step.question,
    lines: [feedback || "Escolha a resposta correta."],
    variant: "check",
    actions: step.options.map((option) => ({
      label: `${option.label} ${option.text}`,
      primary: false,
      onClick: () => handleBriefingCheckAnswer(briefing, stepIndex, option),
    })),
  });
}

function handleBriefingUnderstood() {
  const briefing = findBriefingById(activeBriefingId);

  if (!briefing) {
    closeModal();
    return;
  }

  renderBriefingStep(briefing, activeBriefingStepIndex + 1);
}

function handleBriefingNotUnderstood() {
  const briefing = findBriefingById(activeBriefingId);

  if (!briefing) {
    closeModal();
    return;
  }

  renderBriefingRetry(briefing, activeBriefingStepIndex);
}

function handleBriefingCheckAnswer(briefing, stepIndex, option) {
  const step = briefing.steps[stepIndex];

  if (option.correct) {
    audioManager.playSuccess();
    setMompyState("briefing");
    renderMompyScreenPanel({
      title: "Resposta correta",
      lines: [step.successText],
      actions: [
        {
          label: "Entendi",
          primary: true,
          onClick: () => renderBriefingStep(briefing, stepIndex + 1),
        },
      ],
    });
    return;
  }

  audioManager.playError();
  renderBriefingCheck(briefing, stepIndex, step.failText);
}

function completeBriefing(briefingId) {
  const briefing = findBriefingById(briefingId);

  if (!briefing) {
    renderCurrentMission({ intro: true });
    return;
  }

  if (!completedBriefingIds.includes(briefingId)) {
    completedBriefingIds.push(briefingId);
  }

  skippedBriefingIds = skippedBriefingIds.filter((id) => id !== briefingId);
  saveBriefingProgress();
  activeBriefingId = null;
  activeBriefingStepIndex = 0;
  activeBriefingRetry = false;
  setMompyState("briefing");
  renderMompyScreenPanel({
    title: "Preparação concluída",
    lines: [
      "Preparação concluída.",
      "Conceitos carregados.",
      "Boa sorte, trainee.",
    ],
    actions: [],
  });

  briefingFinalTimer = setTimeout(() => {
    clearMompyScreenMessage();
    renderCurrentMission({ intro: true });
  }, 1200);
}

function skipBriefing(briefingId) {
  if (!skippedBriefingIds.includes(briefingId)) {
    skippedBriefingIds.push(briefingId);
  }

  saveBriefingProgress();
  activeBriefingId = null;
  activeBriefingStepIndex = 0;
  activeBriefingRetry = false;
  clearMompyScreenMessage();
  renderCurrentMission({ intro: true });
}

function openMissionOrBriefing(options = {}) {
  const briefing = getBriefingForMission(currentMissionIndex);

  if (briefing && shouldShowBriefingBeforeMission(currentMissionIndex)) {
    showLearningBriefing(briefing.id);
    return;
  }

  renderCurrentMission(options);
}

function stopTalking() {
  if (talkTimer) {
    clearInterval(talkTimer);
    talkTimer = null;
  }
}

function clearMompyShutdownTimers() {
  mompyShutdownTimers.forEach((timer) => clearTimeout(timer));
  mompyShutdownTimers = [];
}

function stopMompyShutdownAnimation() {
  clearMompyShutdownTimers();
  mompyShutdownAnimating = false;
}

function playShutdownSound() {
  audioManager.playShutdown();
}

function playMompyShutdownAnimation() {
  if (!trainingStarted || !sprite || mompyShutdownAnimating || talkTimer || completionPending || activeBriefingId) {
    return;
  }

  mompyShutdownAnimating = true;
  clearMompyShutdownTimers();
  playShutdownSound();

  const originalSrc = sprite.getAttribute("src") || ASSETS.idle;
  const steps = [
    [0, ASSETS.shutdown2],
    [120, ASSETS.shutdown3],
    [240, ASSETS.shutdown4],
    [420, ASSETS.shutdown4],
    [700, originalSrc],
  ];

  steps.forEach(([delay, source]) => {
    const timer = setTimeout(() => {
      sprite.src = source;

      if (delay === 700) {
        mompyShutdownAnimating = false;
        clearMompyShutdownTimers();
      }
    }, delay);

    mompyShutdownTimers.push(timer);
  });
}

function setMompyState(state, options = {}) {
  stopTalking();
  clearTimeout(settleTimer);
  machine.classList.remove("is-success", "is-error");

  if (state === "talking") {
    talkFrame = false;
    sprite.src = ASSETS.talk1;
    talkTimer = setInterval(() => {
      talkFrame = !talkFrame;
      sprite.src = talkFrame ? ASSETS.talk2 : ASSETS.talk1;
    }, 260);
    return;
  }

  if (state === "briefing") {
    sprite.src = ASSETS.blank;
  } else if (state === "complete") {
    machine.classList.add("is-success");
    sprite.src = ASSETS.shutdown;
  } else if (state === "success") {
    machine.classList.add("is-success");
    sprite.src = ASSETS.success;
  } else if (state === "error") {
    machine.classList.add("is-error");
    sprite.src = ASSETS.error;
  } else {
    sprite.src = ASSETS.idle;
  }

  if (options.returnToIdle) {
    settleTimer = setTimeout(() => setMompyState("idle"), options.returnToIdle);
  }
}

function normalizeName(value) {
  return String(value || "").trim().replace(/\s+/g, " ");
}

function readStoredUserProfile() {
  try {
    const rawProfile = localStorage.getItem(USER_PROFILE_KEY);

    if (!rawProfile) {
      return null;
    }

    const profile = JSON.parse(rawProfile);
    const firstName = normalizeName(profile.firstName);

    if (!firstName) {
      return null;
    }

    return {
      firstName,
      language: profile.language || "pt-BR",
      levelPreference: profile.levelPreference || "beginner",
      email: profile.email || "",
    };
  } catch (error) {
    console.warn(error);
    return null;
  }
}

function applyUserProfile(profile) {
  currentProfile = profile;
  currentUser.name = profile?.firstName || DEFAULT_USER_NAME;
}

function loadUserProfile() {
  const profile = readStoredUserProfile();
  applyUserProfile(profile);
  return profile;
}

function saveUserProfile(firstName) {
  const profile = {
    firstName: normalizeName(firstName),
    language: "pt-BR",
    levelPreference: "beginner",
    email: "",
  };

  localStorage.setItem(USER_PROFILE_KEY, JSON.stringify(profile));
  applyUserProfile(profile);
  renderStartUserInfo();
  callPythonBackend("save_profile", {
    name: profile.firstName,
    language: profile.language,
    level_preference: profile.levelPreference,
    email: profile.email,
  }).then(applyPythonProfile);
  return profile;
}

function clearUserProfile() {
  localStorage.removeItem(USER_PROFILE_KEY);
  applyUserProfile(null);
  renderStartUserInfo();
  callPythonBackend("logout_profile").then(applyPythonProfile);
}

function renderStartUserInfo() {
  startUserName.textContent = currentUser.name;
  startUserLevel.textContent = currentUser.level;
  startMissionCount.textContent = `${currentUser.missionsCompleted} / ${currentUser.totalMissions}`;
}

function clearOnboardingTimers() {
  clearTimeout(onboardingTypingTimer);
  clearTimeout(onboardingDelayTimer);
  onboardingTypingTimer = null;
  onboardingDelayTimer = null;
}

function typeOnboardingLine(line, speed = 36, token = onboardingToken) {
  return new Promise((resolve) => {
    if (!onboardingActive || token !== onboardingToken || !onboardingTerminalOutput) {
      resolve(false);
      return;
    }

    if (onboardingTerminalOutput.textContent) {
      onboardingTerminalOutput.textContent += "\n";
    }

    let index = 0;

    const tick = () => {
      if (!onboardingActive || token !== onboardingToken) {
        resolve(false);
        return;
      }

      onboardingTerminalOutput.textContent += line.charAt(index);
      index += 1;

      if (index >= line.length) {
        resolve(true);
        return;
      }

      onboardingTypingTimer = setTimeout(tick, speed);
    };

    tick();
  });
}

async function typeOnboardingIntro(token = onboardingToken) {
  for (const line of onboardingIntroLines) {
    const completed = await typeOnboardingLine(line, line.startsWith(">>>") ? 34 : 42, token);

    if (!completed) {
      return;
    }

    await wait(line.startsWith(">>>") ? 260 : 460);
  }

  if (!onboardingActive || token !== onboardingToken) {
    return;
  }

  onboardingNameInput.disabled = false;
  onboardingContinueButton.disabled = false;
  onboardingNameInput.focus();
}

function openOnboarding() {
  if (!onboardingOverlay) {
    return;
  }

  onboardingActive = true;
  onboardingToken += 1;
  clearOnboardingTimers();
  stopStartScreenMompyAnimation({ keepFace: true });

  onboardingOverlay.hidden = false;
  onboardingOverlay.setAttribute("aria-hidden", "false");
  onboardingOverlay.classList.remove("is-on");
  onboardingTerminalOutput.textContent = "";
  onboardingNameInput.value = "";
  onboardingNameInput.disabled = true;
  onboardingContinueButton.disabled = true;
  onboardingError.textContent = "";

  const token = onboardingToken;
  onboardingDelayTimer = setTimeout(() => {
    if (!onboardingActive || token !== onboardingToken) {
      return;
    }

    onboardingOverlay.classList.add("is-on");
    typeOnboardingIntro(token);
  }, 520);
}

function closeOnboarding() {
  if (!onboardingOverlay) {
    return;
  }

  onboardingActive = false;
  onboardingToken += 1;
  clearOnboardingTimers();
  onboardingOverlay.hidden = true;
  onboardingOverlay.setAttribute("aria-hidden", "true");
  onboardingOverlay.classList.remove("is-on");
  onboardingTerminalOutput.textContent = "";
  onboardingError.textContent = "";
}

async function submitOnboardingName() {
  const firstName = normalizeName(onboardingNameInput.value);

  if (!firstName) {
    onboardingError.textContent = "Digite seu primeiro nome.";
    onboardingNameInput.focus();
    return;
  }

  onboardingError.textContent = "";
  onboardingNameInput.disabled = true;
  onboardingContinueButton.disabled = true;

  if (onboardingTerminalOutput.textContent) {
    onboardingTerminalOutput.textContent += "\n";
  }

  onboardingTerminalOutput.textContent += `> ${firstName}\n>>> print(nome)\n${firstName}\n\nPerfil salvo.\nCarregando workspace...`;
  saveUserProfile(firstName);
  await wait(720);
  closeOnboarding();
  startStartScreenMompyAnimation();
  audioManager.startAmbientMusic();
}

function showStartMompyFace() {
  startMompySprite.src = ASSETS.idle;
  startMompyTerminal.hidden = true;
  startMompyTerminal.setAttribute("aria-hidden", "true");
}

function showStartMompyTerminal() {
  startMompySprite.src = ASSETS.blank;
  startMompyTerminal.hidden = false;
  startMompyTerminal.setAttribute("aria-hidden", "false");
}

function clearStartMompyTerminal() {
  startMompyTerminalOutput.textContent = "";
}

function terminalLineCount() {
  const text = startMompyTerminalOutput.textContent;
  return text ? text.split("\n").length : 0;
}

function appendTerminalText(text) {
  startMompyTerminalOutput.textContent += text;
}

function typeTerminalLine(line, speed = 45, token = startMompyTerminalToken) {
  return new Promise((resolve) => {
    if (!startScreenAnimationActive || token !== startMompyTerminalToken) {
      resolve(false);
      return;
    }

    if (startMompyTerminalOutput.textContent) {
      appendTerminalText("\n");
    }

    let index = 0;

    const tick = () => {
      if (!startScreenAnimationActive || token !== startMompyTerminalToken) {
        resolve(false);
        return;
      }

      appendTerminalText(line.charAt(index));
      index += 1;

      if (index >= line.length) {
        resolve(true);
        return;
      }

      startMompyTypingTimer = setTimeout(tick, speed);
    };

    tick();
  });
}

function waitStartTerminal(ms, token = startMompyTerminalToken) {
  return new Promise((resolve) => {
    startMompyTypingTimer = setTimeout(() => {
      resolve(startScreenAnimationActive && token === startMompyTerminalToken);
    }, ms);
  });
}

async function typeTerminalBlock(lines, token, options = {}) {
  const nextLineCount = terminalLineCount() + lines.length;

  if (options.clearBefore || nextLineCount > 7) {
    clearStartMompyTerminal();
  }

  for (const line of lines) {
    const completed = await typeTerminalLine(line, line.startsWith("...") ? 34 : 43, token);

    if (!completed) {
      return false;
    }

    const paused = await waitStartTerminal(line.startsWith(">>>") || line.startsWith("...") ? 230 : 420, token);

    if (!paused) {
      return false;
    }
  }

  return true;
}

async function startPythonTerminalLoop(token = startMompyTerminalToken) {
  const welcomed = await typeTerminalBlock(startTerminalWelcome, token, { clearBefore: true });

  if (!welcomed) {
    return;
  }

  await waitStartTerminal(1100, token);

  while (startScreenAnimationActive && token === startMompyTerminalToken) {
    const lines = startTerminalExamples[startTerminalExampleIndex];
    startTerminalExampleIndex = (startTerminalExampleIndex + 1) % startTerminalExamples.length;

    const completed = await typeTerminalBlock(lines, token);

    if (!completed) {
      return;
    }

    await waitStartTerminal(1450, token);
  }
}

function startStartScreenMompyAnimation() {
  stopStartScreenMompyAnimation({ keepFace: true });
  startScreenAnimationActive = true;
  startMompyTerminalToken += 1;
  startTerminalExampleIndex = 0;
  showStartMompyFace();

  const token = startMompyTerminalToken;
  startMompyTerminalTimer = setTimeout(() => {
    if (!startScreenAnimationActive || token !== startMompyTerminalToken) {
      return;
    }

    clearStartMompyTerminal();
    showStartMompyTerminal();
    startPythonTerminalLoop(token);
  }, 2500);
}

function stopStartScreenMompyAnimation(options = {}) {
  startScreenAnimationActive = false;
  startMompyTerminalToken += 1;
  clearTimeout(startMompyTerminalTimer);
  clearTimeout(startMompyTypingTimer);
  startMompyTerminalTimer = null;
  startMompyTypingTimer = null;
  clearStartMompyTerminal();
  startMompyTerminal.hidden = true;
  startMompyTerminal.setAttribute("aria-hidden", "true");

  if (!options.keepFace) {
    startMompySprite.src = ASSETS.idle;
  }
}

function showStartScreen() {
  const profile = loadUserProfile();
  loadProgress();
  loadBriefingProgress();
  trainingStarted = false;
  missionCompleted = false;
  completionPending = false;
  clearTimeout(completionTimer);
  stopMissionTyping();
  stopTalking();
  stopMompyShutdownAnimation();
  clearTimeout(settleTimer);
  clearMompyScreenMessage();
  machine.classList.remove("training-active", "is-success", "is-error");
  startScreen.hidden = false;
  sprite.src = ASSETS.idle;
  setMissionActionsEnabled(true);
  renderStartUserInfo();
  if (profile) {
    closeOnboarding();
    startStartScreenMompyAnimation();
  } else {
    openOnboarding();
  }
  audioManager.startAmbientMusic();
}

function enterTraining() {
  closeOnboarding();
  stopStartScreenMompyAnimation();
  stopMompyShutdownAnimation();
  audioManager.stopAmbientMusic();
  trainingStarted = true;
  missionCompleted = false;
  completionPending = false;
  clearTimeout(completionTimer);
  startScreen.hidden = true;
  machine.classList.add("training-active");
  machine.classList.remove("is-success", "is-error");
  clearMompyScreenMessage();
  setMissionActionsEnabled(true);
  openMissionOrBriefing({ intro: true });
  editor.focus();
}

function startFreshTraining() {
  resetProgress({ keepMissionView: true });
  saveProgress();
  enterTraining();
}

function confirmStartOver() {
  openModal({
    title: "Começar do zero",
    body: "<p>Você já tem progresso salvo.<br>Deseja começar do zero?</p>",
    actions: [
      {
        label: "Cancelar",
        onClick: () => {
          closeModal();
          restoreAfterModal();
        },
      },
      {
        label: "Começar do zero",
        primary: true,
        onClick: () => {
          closeModal();
          startFreshTraining();
        },
      },
    ],
  });
}

function handleStart() {
  loadProgress();
  loadBriefingProgress();

  if (hasSavedProgress()) {
    confirmStartOver();
    return;
  }

  startFreshTraining();
}

function handleContinue() {
  if (hasSavedProgress()) {
    loadProgress();
  } else {
    resetProgress({ keepMissionView: true });
    saveProgress();
  }

  loadBriefingProgress();
  enterTraining();
}

function updateLevelDisplay() {
  const levelInfo = getUserLevelInfo(totalXp);
  levelValue.textContent = String(levelInfo.level).padStart(2, "0");
  levelFill.style.width = `${Math.max(4, levelInfo.progress)}%`;
}

function stopMissionTyping() {
  typingToken += 1;

  if (typingTimer) {
    clearTimeout(typingTimer);
    typingTimer = null;
  }
}

function buildMissionNodes(mission) {
  missionCopy.replaceChildren();

  const targets = [];
  const heading = document.createElement("h2");
  missionCopy.append(heading);
  targets.push({ node: heading, text: mission.title });

  const blocks = mission.blocks || [
    [{ text: mission.description }],
    [{ text: `Objetivo: ${mission.objective}` }],
  ];

  blocks.forEach((block) => {
    const paragraph = document.createElement("p");

    block.forEach((segment) => {
      const node = segment.tag
        ? document.createElement(segment.tag)
        : document.createTextNode("");

      paragraph.append(node);
      targets.push({ node, text: segment.text });
    });

    missionCopy.append(paragraph);
  });

  return targets;
}

function writeNode(node, text) {
  if (node.nodeType === Node.TEXT_NODE) {
    node.nodeValue = text;
    return;
  }

  node.textContent = text;
}

function renderMission(mission) {
  updateLevelDisplay();
  buildMissionNodes(mission).forEach((target) => writeNode(target.node, target.text));
}

function missionIntroText(mission) {
  return `Mompy: ${mission.objective}\nAtalho: Ctrl+Enter também executa.`;
}

function renderCurrentMission(options = {}) {
  const mission = currentMission();
  missionCompleted = false;
  completionPending = false;
  clearTimeout(completionTimer);
  clearMompyScreenMessage();
  stopMissionTyping();
  setMissionActionsEnabled(true);
  setMompyState("idle");
  renderMission(mission);
  editor.value = mission.starterCode || "";
  updateLineNumbers();
  updateProgressUI();
  output.textContent = options.outputMessage || missionIntroText(mission);

  if (options.intro) {
    playMissionIntro();
  }
}

function typeText(target, token) {
  return new Promise((resolve) => {
    let index = 0;

    const tick = () => {
      if (token !== typingToken) {
        resolve(false);
        return;
      }

      writeNode(target.node, target.text.slice(0, index));

      if (index >= target.text.length) {
        resolve(true);
        return;
      }

      index += 1;
      typingTimer = setTimeout(tick, 22);
    };

    tick();
  });
}

async function playMissionIntro() {
  if (!trainingStarted) {
    return;
  }

  const mission = currentMission();
  stopMissionTyping();
  updateLevelDisplay();

  const token = typingToken;
  const targets = buildMissionNodes(mission);
  setMompyState("talking");

  for (const target of targets) {
    const completed = await typeText(target, token);

    if (!completed) {
      return;
    }

    await wait(80);
  }

  setMompyState("idle");
}

function finishMissionIntro() {
  if (!trainingStarted) {
    return;
  }

  stopMissionTyping();
  renderMission(currentMission());
}

function setMissionActionsEnabled(enabled) {
  backButton.disabled = !enabled;
  helpButton.disabled = !enabled;
  runButton.disabled = !enabled;
}

function showMissionCompleteOnMompy() {
  renderMompyCompletionPrompt();
  mompyScreenMessage.hidden = false;
}

function clearMompyScreenMessage() {
  mompyScreenMessage.hidden = true;
  mompyScreenMessage.className = "mompy-screen-message";
}

function restoreAfterModal() {
  if (missionCompleted) {
    if (completionPending) {
      setMompyState("success");
    } else {
      setMompyState("complete");
      showMissionCompleteOnMompy();
    }
    return;
  }

  if (trainingStarted) {
    setMompyState("idle");
  }
}

function completeMission(result) {
  const mission = currentMission();
  missionCompleted = true;
  completionPending = true;
  const alreadyCompleted = completedMissionIds.includes(mission.id);

  if (!alreadyCompleted) {
    completedMissionIds.push(mission.id);
    totalXp += getMissionXp(mission);
  }

  saveProgress();
  callPythonBackend("complete_mission", mission.id).then(applyPythonProgress);
  clearTimeout(completionTimer);
  setMissionActionsEnabled(false);
  clearMompyScreenMessage();
  output.textContent = `Correct output:\n${result.output}\n\nMission completed.`;
  audioManager.playSuccess();
  setMompyState("success");
  completionTimer = setTimeout(() => {
    if (!missionCompleted) {
      return;
    }

    completionPending = false;
    setMompyState("complete");
    showMissionCompleteOnMompy();
  }, 1500);
}

function failMission(result) {
  output.textContent = [
    `> ${result.output}`,
    "",
    "Ainda não foi dessa vez.",
    "Verifique o objetivo da missão e tente novamente.",
    "",
    `Dica: ${result.detail}`,
  ].join("\n");
  audioManager.playError();
  setMompyState("error", { returnToIdle: 3200 });
}

function repeatMission() {
  missionCompleted = false;
  completionPending = false;
  clearTimeout(completionTimer);
  clearMompyScreenMessage();
  setMissionActionsEnabled(true);
  setMompyState("idle");
  editor.value = currentMission().starterCode || "";
  updateLineNumbers();
  output.textContent = "Missão reiniciada. Tente novamente.";
  editor.focus();
}

function goToNextMission() {
  if (currentMissionIndex >= missions.length - 1) {
    missionCompleted = true;
    completionPending = false;
    clearTimeout(completionTimer);
    clearMompyScreenMessage();
    setMissionActionsEnabled(false);
    setMompyState("complete");
    output.textContent = [
      "Todas as missões disponíveis foram concluídas.",
      "Novas missões serão adicionadas em breve.",
    ].join("\n");
    saveProgress();
    return;
  }

  currentMissionIndex = clampMissionIndex(currentMissionIndex + 1);
  missionCompleted = false;
  completionPending = false;
  clearTimeout(completionTimer);
  saveProgress();
  openMissionOrBriefing({ intro: true });
  editor.focus();
}

function updateLineNumbers() {
  const total = Math.max(1, editor.value.split("\n").length);
  lineNumbers.textContent = Array.from({ length: total }, (_, index) => index + 1).join("\n");
}

function extractPrintOutput(code) {
  const printCall = code.match(/print\s*\(\s*(["'`])([\s\S]*?)\1\s*\)/);
  return printCall ? printCall[2] : "";
}

async function validateCode(code) {
  await wait(450);

  const mission = currentMission();
  const trimmed = code.trim();
  if (!trimmed || trimmed === "# escreva aqui") {
    return {
      ok: false,
      output: "Nenhum código para executar.",
      detail: mission.help || "Escreva o código pedido no editor.",
    };
  }

  const backendValidation = await callPythonBackend("validate_mission", mission.id, code);
  if (backendValidation && typeof backendValidation.correct === "boolean") {
    return {
      ok: Boolean(backendValidation.correct),
      output: backendValidation.actual_output || backendValidation.expected_output || mission.expectedOutput,
      detail: backendValidation.correct
        ? backendValidation.message || "Missão concluída."
        : backendValidation.runtime_error || backendValidation.hints?.[0] || backendValidation.message || mission.help,
    };
  }

  const printed = extractPrintOutput(code);
  return {
    ok: false,
    output: printed || "Ainda não foi dessa vez.",
    detail: "Abra o Mompy pelo Python para usar a validação real das missões.",
  };
}

async function runCode() {
  if (!trainingStarted || missionCompleted || runButton.disabled) {
    return;
  }

  finishMissionIntro();
  const code = editor.value;
  runButton.disabled = true;
  output.textContent = "Executando validação...";
  audioManager.playRun();
  setMompyState("talking");

  try {
    const result = await validateCode(code);
    if (result.ok) {
      completeMission(result);
      return;
    }

    failMission(result);
  } catch (error) {
    output.textContent = `Falha inesperada:\n${error.message}`;
    audioManager.playError();
    setMompyState("error", { returnToIdle: 3200 });
  } finally {
    if (!missionCompleted) {
      runButton.disabled = false;
    }

    editor.focus();
  }
}

function openModal({ title, body, actions = [] }) {
  lastFocusedElement = document.activeElement;
  modalTitle.textContent = title;
  modalBody.innerHTML = body;
  modalActions.replaceChildren();

  actions.forEach((action) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = action.primary ? "modal-button primary" : "modal-button";
    button.textContent = action.label;
    button.addEventListener("click", action.onClick);
    modalActions.append(button);
  });

  modalBackdrop.hidden = false;
  const firstAction = modalActions.querySelector("button");

  if (firstAction) {
    firstAction.focus();
  } else {
    modalCloseButton.focus();
  }
}

function closeModal() {
  modalBackdrop.hidden = true;
  modalTitle.textContent = "";
  modalBody.textContent = "";
  modalActions.replaceChildren();

  if (lastFocusedElement instanceof HTMLElement) {
    lastFocusedElement.focus();
  }
}

function showBackConfirmation() {
  if (backButton.disabled) {
    return;
  }

  finishMissionIntro();
  setMompyState("idle");

  if (currentMissionIndex <= 0) {
    output.textContent = "Mompy: Você já está na primeira missão.";
    return;
  }

  openModal({
    title: "Voltar missão",
    body: "<p>Tem certeza que deseja voltar para a missão anterior?</p>",
    actions: [
      {
        label: "Cancelar",
        onClick: () => {
          closeModal();
          setMompyState("idle");
        },
      },
      {
        label: "Confirmar",
        primary: true,
        onClick: () => {
          closeModal();
          currentMissionIndex = clampMissionIndex(currentMissionIndex - 1);
          saveProgress();
          openMissionOrBriefing({ intro: true });
        },
      },
    ],
  });
}

function showHelp() {
  if (helpButton.disabled) {
    return;
  }

  finishMissionIntro();
  setMompyState("talking");
  const mission = currentMission();
  openModal({
    title: "Ajuda da missão",
    body: `
      <p>${mission.help}</p>
      <p><strong>Objetivo:</strong> ${mission.objective}</p>
    `,
    actions: [
      {
        label: "Entendi",
        primary: true,
        onClick: () => {
          closeModal();
          setMompyState("idle");
        },
      },
    ],
  });
}

function toggleLabel(value) {
  return value ? "ON" : "OFF";
}

function settingMeter(settingName) {
  const value = settingsState[settingName];
  return `
    <div class="setting-stepper">
      <button class="setting-step" type="button" data-setting-step="${settingName}" data-delta="-10" aria-label="Diminuir">-</button>
      <span class="setting-meter" data-setting-meter="${settingName}" style="--value: ${value}%">
        <span data-setting-value="${settingName}">${value}%</span>
      </span>
      <button class="setting-step" type="button" data-setting-step="${settingName}" data-delta="10" aria-label="Aumentar">+</button>
    </div>
  `;
}

function renderSettingsBody() {
  return `
    <div class="settings-grid">
      <section class="settings-section">
        <h3>Atalhos</h3>
        <div class="settings-row"><span><code>Ctrl + Enter</code></span><span class="settings-control">Run</span></div>
        <div class="settings-row"><span><code>F1</code></span><span class="settings-control">Help</span></div>
        <div class="settings-row"><span><code>Esc</code></span><span class="settings-control">Fechar</span></div>
      </section>

      <section class="settings-section">
        <h3>Áudio</h3>
        <div class="settings-row">
          <span>Música ambiente</span>
          <button class="settings-control settings-toggle" type="button" data-setting-toggle="ambientMusic" aria-pressed="${settingsState.ambientMusic}">
            ${toggleLabel(settingsState.ambientMusic)}
          </button>
        </div>
        <div class="settings-row"><span>Volume da música</span>${settingMeter("musicVolume")}</div>
        <div class="settings-row">
          <span>Efeitos sonoros</span>
          <button class="settings-control settings-toggle" type="button" data-setting-toggle="soundEffects" aria-pressed="${settingsState.soundEffects}">
            ${toggleLabel(settingsState.soundEffects)}
          </button>
        </div>
        <div class="settings-row"><span>Volume dos efeitos</span>${settingMeter("effectsVolume")}</div>
      </section>

      <section class="settings-section">
        <h3>Interface</h3>
        <div class="settings-row"><span>Brilho CRT</span>${settingMeter("crtBrightness")}</div>
        <div class="settings-row">
          <span>Animações do Mompy</span>
          <button class="settings-control settings-toggle" type="button" data-setting-toggle="mompyAnimations" aria-pressed="${settingsState.mompyAnimations}">
            ${toggleLabel(settingsState.mompyAnimations)}
          </button>
        </div>
      </section>

      <section class="settings-section">
        <h3>Progress</h3>
        <div class="settings-row">
          <span>Missões concluídas</span>
          <span class="settings-control">${completedMissionIds.length} / ${PLANNED_TOTAL_MISSIONS}</span>
        </div>
        <div class="settings-row">
          <span>Missão atual</span>
          <span class="settings-control">${String(currentMissionIndex + 1).padStart(2, "0")}</span>
        </div>
        <div class="settings-row">
          <span>Progresso local</span>
          <button id="resetProgressButton" class="settings-inline-button" type="button">Reset progress</button>
        </div>
      </section>

      <section class="settings-section">
        <h3>Conta</h3>
        <div class="settings-row">
          <span>Usuário atual</span>
          <span class="settings-control">${currentUser.name}</span>
        </div>
        <div class="settings-row">
          <span>Sessão</span>
          <button id="logoutUserButton" class="settings-inline-button" type="button">Sair do usuário</button>
        </div>
      </section>
    </div>
  `;
}

function updateSettingView(settingName) {
  const valueElement = modalBody.querySelector(`[data-setting-value="${settingName}"]`);
  const meter = modalBody.querySelector(`[data-setting-meter="${settingName}"]`);

  if (!valueElement || !meter) {
    return;
  }

  const value = settingsState[settingName];
  valueElement.textContent = `${value}%`;
  meter.style.setProperty("--value", `${value}%`);
}

function bindSettingsControls() {
  modalBody.querySelectorAll("[data-setting-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const settingName = button.dataset.settingToggle;

      if (settingName === "ambientMusic") {
        audioManager.setMusicEnabled(!settingsState.ambientMusic);
      } else if (settingName === "soundEffects") {
        audioManager.setSfxEnabled(!settingsState.soundEffects);
      } else {
        settingsState[settingName] = !settingsState[settingName];
      }

      button.textContent = toggleLabel(settingsState[settingName]);
      button.setAttribute("aria-pressed", String(settingsState[settingName]));
    });
  });

  modalBody.querySelectorAll("[data-setting-step]").forEach((button) => {
    button.addEventListener("click", () => {
      const settingName = button.dataset.settingStep;
      const delta = Number(button.dataset.delta);
      const nextValue = Math.min(100, Math.max(0, settingsState[settingName] + delta));

      if (settingName === "musicVolume") {
        audioManager.setMusicVolume(nextValue / 100);
      } else if (settingName === "effectsVolume") {
        audioManager.setSfxVolume(nextValue / 100);
      } else {
        settingsState[settingName] = nextValue;
      }

      updateSettingView(settingName);
    });
  });

  modalBody.querySelector("#logoutUserButton")?.addEventListener("click", confirmLogoutUser);
  modalBody.querySelector("#resetProgressButton")?.addEventListener("click", confirmResetProgress);
}

function showSettings() {
  finishMissionIntro();

  if (trainingStarted && !missionCompleted) {
    setMompyState("idle");
  }

  openModal({
    title: "Configurações",
    body: renderSettingsBody(),
    actions: [
      {
        label: "Exit",
        onClick: confirmExitApp,
      },
    ],
  });
  bindSettingsControls();
}

function confirmExitApp() {
  openModal({
    title: "Sair do app",
    body: "<p>Tem certeza que deseja sair?</p>",
    actions: [
      {
        label: "Cancelar",
        onClick: showSettings,
      },
      {
        label: "Sair",
        primary: true,
        onClick: () => {
          closeModal();
          exitApp();
        },
      },
    ],
  });
}

function confirmLogoutUser() {
  openModal({
    title: "Sair do usuário",
    body: "<p>Deseja sair deste usuário?</p>",
    actions: [
      {
        label: "Cancelar",
        onClick: showSettings,
      },
      {
        label: "Sair do usuário",
        primary: true,
        onClick: () => {
          logoutUser();
          closeModal();
          showStartScreen();
        },
      },
    ],
  });
}

function confirmResetProgress() {
  openModal({
    title: "Reset progress",
    body: "<p>Tem certeza que deseja resetar o progresso das missões?</p>",
    actions: [
      {
        label: "Cancelar",
        onClick: showSettings,
      },
      {
        label: "Reset progress",
        primary: true,
        onClick: () => {
          resetProgress();
          closeModal();

          if (trainingStarted) {
            output.textContent = "Progresso resetado.";
            editor.focus();
          } else {
            showStartScreen();
          }
        },
      },
    ],
  });
}

function logoutUser() {
  console.log("Sair do usuário atual");
  clearUserProfile();
}

function exitApp() {
  audioManager.playShutdown();
  audioManager.stopAmbientMusic();
  clearMompyScreenMessage();
  stopStartScreenMompyAnimation();
  stopMissionTyping();
  stopTalking();
  stopMompyShutdownAnimation();
  clearTimeout(settleTimer);
  clearTimeout(completionTimer);
  completionPending = false;
  setMompyState("idle");
  startMompySprite.src = ASSETS.idle;

  if (output) {
    output.textContent = "Mompy: Saindo do app.";
  }

  if (document.fullscreenElement) {
    document.exitFullscreen().catch(() => {});
  }

  window.close();
}

async function toggleFullscreen() {
  try {
    if (!document.fullscreenElement) {
      await document.documentElement.requestFullscreen();
    } else {
      await document.exitFullscreen();
    }
  } catch (error) {
    const message = `Mompy: Não consegui alterar a tela cheia.\n${error.message}`;

    if (trainingStarted) {
      output.textContent = message;
      setMompyState("error", { returnToIdle: 2600 });
    } else {
      console.warn(message);
    }
  }
}

function updateFullscreenButton() {
  if (!fullscreenButton) {
    return;
  }

  const isFullscreen = Boolean(document.fullscreenElement);
  fullscreenButton.classList.toggle("is-fullscreen", isFullscreen);
  fullscreenButton.setAttribute(
    "aria-label",
    isFullscreen ? "Sair da tela cheia" : "Expandir janela",
  );
}

function unlockAudioOnFirstInteraction() {
  audioManager.unlock();
}

document.addEventListener("pointerdown", unlockAudioOnFirstInteraction, { once: true, capture: true });
document.addEventListener("keydown", unlockAudioOnFirstInteraction, { once: true, capture: true });

document.addEventListener("click", (event) => {
  const button = event.target.closest("button");

  if (!button || button.id === "runButton") {
    return;
  }

  audioManager.playClick();
});

editor.addEventListener("input", updateLineNumbers);
editor.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    event.preventDefault();

    if (!runButton.disabled) {
      runCode();
    }
  }

  if (event.key === "Tab") {
    event.preventDefault();
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    editor.value = `${editor.value.slice(0, start)}    ${editor.value.slice(end)}`;
    editor.selectionStart = editor.selectionEnd = start + 4;
    updateLineNumbers();
  }
});

startButton.addEventListener("click", handleStart);
continueButton.addEventListener("click", handleContinue);
onboardingContinueButton?.addEventListener("click", submitOnboardingName);
onboardingNameInput?.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    submitOnboardingName();
  }
});
runButton.addEventListener("click", runCode);
backButton.addEventListener("click", showBackConfirmation);
helpButton.addEventListener("click", showHelp);
settingsButton.addEventListener("click", showSettings);
fullscreenButton?.addEventListener("click", toggleFullscreen);
sprite?.addEventListener("click", playMompyShutdownAnimation);
modalCloseButton.addEventListener("click", () => {
  closeModal();
  restoreAfterModal();
});
repeatMissionButton.addEventListener("click", repeatMission);
nextMissionButton.addEventListener("click", goToNextMission);
document.addEventListener("fullscreenchange", updateFullscreenButton);

modalBackdrop.addEventListener("click", (event) => {
  if (event.target === modalBackdrop) {
    closeModal();
    restoreAfterModal();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !modalBackdrop.hidden) {
    event.preventDefault();
    closeModal();
    restoreAfterModal();
  }

  if (event.key === "F1" && trainingStarted && !helpButton.disabled) {
    event.preventDefault();
    showHelp();
  }
});

audioManager.init();
loadUserProfile();
loadProgress();
loadBriefingProgress();
renderMission(currentMission());
editor.value = currentMission().starterCode || editor.value;
updateLineNumbers();
updateFullscreenButton();
startLoadingSequence();

const isLocalPreview = ["localhost", "127.0.0.1"].includes(location.hostname);

if ("serviceWorker" in navigator && isLocalPreview) {
  navigator.serviceWorker
    .getRegistrations()
    .then((registrations) =>
      registrations.forEach((registration) => registration.unregister()),
    )
    .catch(() => {});
}

if ("serviceWorker" in navigator && location.protocol !== "file:" && !isLocalPreview) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}
