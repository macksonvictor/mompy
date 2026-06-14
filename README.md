# Mompy

Mompy e uma plataforma de aprendizado de Python com visual CRT/industrial.

## Estrutura

```txt
mompy/
  frontend/
    index.html
    css/styles.css
    js/app.js
    assets/

  backend/
    missions.py
    lessons.py
    validator.py
    progress.py
    xp.py
    code_runner.py
    storage.py
    api.py

  data/progress.json
  tests/
  main.py
```

## Frontend

O frontend continua cuidando da experiencia visual:

- telas CRT;
- animacoes;
- editor;
- botoes;
- assets;
- audio;
- fluxo visual atual.

Para abrir direto no navegador:

```bash
python main.py --serve --port 8770
```

Depois acesse:

```txt
http://127.0.0.1:8770/
```

## App desktop Python

Instale a dependencia desktop:

```bash
python -m pip install -r requirements.txt
```

Abra o Mompy como aplicativo Python com pywebview:

```bash
python main.py
```

Para apenas verificar o backend sem abrir janela:

```bash
python main.py --check
```

## Backend Python

O backend Python foi criado para assumir gradualmente a logica real do app:

- dados das missoes;
- dados das aulas;
- validacao real das 30 missoes atuais;
- progresso local;
- XP e nivel;
- API interna conectada ao frontend via pywebview;
- API HTTP local para o modo navegador em `python main.py --serve`;
- execucao segura inicial do codigo do aluno em processo isolado.

Nesta fase, o backend valida a estrutura das respostas com AST e regras Python,
executa codigo simples em sandbox conservador, captura o output e compara com o
resultado esperado da missao.

A trilha pedagogica segue uma curva de iniciante real:

1. Primeiros comandos com `print`.
2. Variaveis e valores.
3. Decisoes com `if`.
4. Repeticoes com `for`.
5. Listas.
6. Funcoes.

## Testes

Os testes usam apenas a biblioteca padrao do Python:

```bash
python -m unittest discover -s tests
```

## Roadmap

- 10.1: organizar e salvar versao estavel.
- 10.2: criar arquitetura frontend + backend Python.
- 10.3: conectar frontend com backend Python usando pywebview.
- 10.4: migrar validacao real das missoes para Python.
- 10.5: execucao segura do codigo Python do usuario.
- 10.6: progresso, XP e nivel 100% pelo backend Python.
- 10.7: empacotar app Python instalavel.
