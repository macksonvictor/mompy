# Contributing to Mompy

Thank you for your interest in Mompy.

Mompy is still in active development, so contributions should stay focused, simple, and aligned with the project direction.

## Project direction

Mompy is a retro CRT-style Python training app for beginners.

The project priorities are:

- clear beginner-friendly Python lessons and missions;
- a polished retro/CRT interface;
- a Python backend for mission validation, progress, XP, and safe code execution;
- local-first progress and profile storage;
- simple desktop packaging;
- no unnecessary server, login, or cloud dependency for the first version.

## Before contributing

Please open an issue before making large changes.

Good issues include:

- bug reports;
- interface problems;
- mission ideas;
- lesson improvements;
- accessibility improvements;
- documentation improvements;
- packaging improvements.

## Pull request guidelines

When submitting a pull request:

1. Keep the change focused.
2. Do not redesign the interface without discussion.
3. Do not add online accounts, passwords, or cloud sync unless there is an approved plan.
4. Do not commit generated builds, installers, virtual environments, temporary files, or local progress data.
5. Test the app locally before submitting.
6. Explain what changed and why.

## Development setup

```bash
git clone https://github.com/hepter-studios/mompy.git
cd mompy
```

When the Python desktop setup is ready, the expected flow will be:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

The commands may change while the Python backend and desktop bridge are being completed.

## Code style

- Keep HTML, CSS, and JavaScript readable.
- Keep Python modules simple and beginner-friendly.
- Prefer clear names over clever names.
- Keep UI behavior simple and predictable.
- Preserve the current Mompy visual identity unless a visual change is requested.
- Keep mission logic understandable for Python contributors.

## Local-first rule

For the first desktop version, user data should stay local whenever possible.

Do not add server dependencies unless the project explicitly moves to an online/cloud phase.
