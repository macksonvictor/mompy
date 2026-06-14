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

## Backend Python

O backend Python foi criado para assumir gradualmente a logica real do app:

- dados das missoes;
- dados das aulas;
- validacao simples das respostas;
- progresso local;
- XP e nivel;
- API interna preparada para pywebview;
- estrutura futura de execucao segura de codigo.

Nesta fase, o backend ainda nao executa codigo livre do usuario. Isso fica para a fase de sandbox.

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
