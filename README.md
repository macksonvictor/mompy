# Mompy: Retro Python Training Console

[![Status](https://img.shields.io/badge/status-in%20development-8cff3a?style=for-the-badge)](#project-status)
[![Platform](https://img.shields.io/badge/platform-Windows-0b5fff?style=for-the-badge&logo=windows&logoColor=white)](#desktop-app)
[![Built with](https://img.shields.io/badge/built%20with-HTML%20%7C%20CSS%20%7C%20JS-f7df1e?style=for-the-badge&logo=javascript&logoColor=black)](#technology-stack)
[![Desktop](https://img.shields.io/badge/desktop-Electron-47848f?style=for-the-badge&logo=electron&logoColor=white)](#desktop-app)
[![Python Training](https://img.shields.io/badge/python-training-3776ab?style=for-the-badge&logo=python&logoColor=white)](#what-is-mompy)

English | Português

---

**Mompy** is a retro CRT-style Python Training Console built to help beginners learn programming through small interactive missions.

It combines a nostalgic old-computer interface, a friendly monitor mascot, terminal-like interactions, mission progress, sound effects, animations, and a local-first desktop experience.

> [!NOTE]
> Mompy is currently in active development.
> The current focus is interface polish, mission flow, local progress, audio, animations, and desktop packaging.

---

## What is Mompy?

Mompy is a learning app designed to make programming feel more alive, focused, and fun.

Instead of being just another normal coding website, Mompy is being built as a **desktop training console** with a retro industrial CRT interface. The user learns Python through guided missions, receives feedback from Mompy, and progresses step by step.

The long-term goal is to make Mompy feel like a small companion that teaches programming in a calm, friendly, and memorable way.

---

## Core Concept

Mompy follows a simple learning loop:

1. The user opens the app.
2. Mompy starts with a CRT-style loading screen.
3. The start screen appears with the user profile and progress.
4. The user starts or continues Python training.
5. Each mission gives a small coding challenge.
6. The user writes code and runs it.
7. Mompy reacts with feedback, sounds, and animations.
8. Progress is saved locally on the user's computer.

---

## Visual Identity

Mompy uses a retro-futuristic visual language inspired by old terminals, industrial control panels, and CRT monitors.

Main visual characteristics:

- Dark industrial interface
- Green CRT glow
- Pixel/scanline effects
- Retro monitor mascot
- Terminal-style text
- Metallic UI panels
- Old-computer atmosphere
- Local desktop app feeling

The goal is to make Mompy feel like an old intelligent training terminal.

---

## Current Features

- CRT-style interface
- Start screen
- Loading screen
- Mission screen
- Code editor area
- Output panel
- Help button
- Run button
- Back button
- Settings modal
- Local user profile
- Mission completion flow
- Mompy mascot states
- Audio system planning
- Progress system planning
- Electron desktop packaging planning

---

## Planned Features

### Learning System

- Python beginner missions
- Step-by-step challenges
- Mission validation
- Mission progress
- Hints per mission
- Completion flow
- Repeat mission
- Next mission
- Level system

### Mompy Character

- Idle state
- Talking animation
- Happy state
- Sad/error state
- CRT shutdown animation
- Terminal animation on the start screen
- Mission completion messages inside Mompy's screen

### Audio

- Button click sound
- Run sound
- Success sound
- Error sound
- CRT shutdown sound
- Calm CRT ambient sound for the start screen only

### User Profile

- First-name setup
- Local profile
- Local settings
- Language preference
- Progress reset
- Future optional cloud sync

### Desktop App

- Electron desktop app
- Windows `.exe`
- Local-first storage
- GitHub Releases
- Official website/download page

---

## Local-First Philosophy

Mompy is designed to work without requiring an online account.

For the first version, the following data should be stored locally:

- User first name
- Language preference
- Current mission
- Completed missions
- Audio settings
- Interface settings
- Progress state

This keeps the app simple, private, and usable offline.

Cloud sync, login, and online accounts may be added later, but they are not required for the first desktop version.

---

## Desktop App

Mompy is being developed with web technologies, but the final goal is to make it feel like a real installed application.

Planned path:

```txt
HTML + CSS + JavaScript
↓
Electron
↓
Mompy.exe
```

The website will be used mainly as the official page for information and downloads.

```txt
Mompy app = installable desktop app
mompy.com.br = official website / download page
GitHub Releases = app installer downloads
```

---

## Technology Stack

Current / planned stack:

- HTML
- CSS
- JavaScript
- LocalStorage
- Electron
- Electron Builder
- Git
- GitHub
- GitHub Releases

Possible future additions:

- Node.js helpers
- Local file storage
- Cloud sync
- Online accounts
- Mission editor
- AI-assisted hints

---

## Project Structure

Planned structure:

```txt
mompy/
  src/
    index.html
    styles.css
    main.js

    assets/
      images/
      audio/
      icons/

  electron/
    main.js
    preload.js

  README.md
  package.json
  .gitignore
```

The structure may change while the project is still in development.

---

## Development

After installing dependencies:

```bash
npm install
```

Run the app in development:

```bash
npm run dev
```

Or, depending on the current setup:

```bash
npm start
```

---

## Build

When Electron is configured, the app should be built with:

```bash
npm run build
```

The generated installer or executable should not be committed directly into the repository.

Installers should be published later through **GitHub Releases**.

---

## GitHub Releases

The repository contains the source code.

GitHub Releases will be used for downloadable versions of the app.

Example future release:

```txt
Mompy v1.0.0
Mompy-Setup.exe
```

Users will be able to download the installer without touching the source code.

---

## Audio Files

Expected audio files:

```txt
assets/audio/click.wav
assets/audio/run.wav
assets/audio/success.wav
assets/audio/error.wav
assets/audio/shutdown.wav
assets/audio/mompy_crt_ambient_loop_minimal.wav
```

Audio behavior:

- Loading screen: no sound
- Start screen: ambient sound only
- Mission screen: sound effects only
- Run: run sound
- Correct answer: success sound
- Wrong answer: error sound
- CRT shutdown animation: shutdown sound

---

## User Profile

Mompy should not use a hardcoded user name.

On first launch, the user should enter at least:

- First name

Optional future profile fields:

- Language
- Level preference
- Email for future sync

For now, the profile is stored locally.

---

## Privacy

Mompy is planned as a local-first app.

In the first version:

- No server is required
- No online login is required
- No password is required
- No cloud sync is required
- Progress is stored locally on the user's computer

If online features are added in the future, they should be optional and clearly explained.

---

## Roadmap

### Phase 1 — Main Layout

Fix the main mission screen layout, alignment, panels, editor, output, and top bar.

### Phase 2 — Buttons

Add and organize Settings, Exit, Back, Help, and Run buttons.

### Phase 3 — Button Functions

Implement modals, shortcuts, confirmation dialogs, and mission completion behavior.

### Phase 4 — Start Screen

Create the entry screen with Mompy, Start, Continue, user information, level, and missions completed.

### Phase 5 — Loading Screen

Create the CRT-style loading screen with Mompy and a real animated progress bar.

### Phase 6 — Mompy Animations

Implement Mompy states, talking animation, happy/sad states, terminal animation, and CRT shutdown interaction.

### Phase 7 — Audio

Implement sound effects and ambient sound behavior.

### Phase 8 — Progress and Missions

Implement local mission data, validation, progress saving, Start, Continue, Reset Progress, and level updates.

### Phase 9 — Polish and Testing

Fix bugs, improve alignment, test screens, test audio, test progress, and create a test checklist.

### Phase 10 — Desktop App and GitHub

Configure Electron, prepare the Windows desktop app, organize the repository, and push the project to GitHub.

---

## Test Checklist

Before release:

### Loading

- [ ] Loading screen appears
- [ ] Loading progress works
- [ ] Loading has no sound
- [ ] Loading transitions to start screen

### Start Screen

- [ ] Start button works
- [ ] Continue button works
- [ ] User name is loaded from local profile
- [ ] Level appears correctly
- [ ] Missions completed count appears correctly
- [ ] Ambient sound works only here

### Mission Screen

- [ ] Run button works
- [ ] Correct code completes mission
- [ ] Wrong code shows hint
- [ ] Help opens mission help
- [ ] Back asks confirmation
- [ ] Output updates correctly
- [ ] Mompy reacts correctly

### Completion Flow

- [ ] Mission completed message appears on Mompy screen
- [ ] Back, Help, and Run disable after completion
- [ ] Repeat works
- [ ] Next Mission works
- [ ] Settings and Exit still work

### Settings

- [ ] Settings modal opens
- [ ] Esc closes modal
- [ ] Audio settings save
- [ ] Progress reset asks confirmation
- [ ] Profile editing works
- [ ] Language preference is saved

### Audio

- [ ] click.wav works
- [ ] run.wav works
- [ ] success.wav works
- [ ] error.wav works
- [ ] shutdown.wav works
- [ ] ambient loop works
- [ ] volume controls work
- [ ] audio preferences save

### GitHub

- [ ] `.gitignore` exists
- [ ] `node_modules` is not committed
- [ ] Build folders are not committed
- [ ] README is updated
- [ ] Project pushes correctly
- [ ] Main branch is stable
- [ ] Dev branch is used for changes

---

## Git Workflow

Recommended workflow:

```txt
main = stable version
dev = development version
```

Before major changes:

```bash
git add .
git commit -m "Save current working version"
git push
```

After a successful feature:

```bash
git add .
git commit -m "Add Mompy audio system"
git push
```

Files that should not be pushed:

```txt
node_modules/
dist/
build/
release/
out/
.env
*.exe
*.log
```

---

## Official Website

Planned official website:

```txt
mompy.com.br
```

The website can be used for:

- Project presentation
- Screenshots
- Download button
- GitHub link
- Release notes
- Future documentation

---

## Português

**Mompy** é um console retrô de treinamento em Python, criado para ajudar iniciantes a aprender programação por meio de pequenas missões interativas.

A ideia é unir:

- Visual de computador antigo
- Interface CRT verde
- Mascote amigável
- Missões de Python
- Feedback visual e sonoro
- Progresso salvo localmente
- Aplicativo instalável para Windows

O objetivo é fazer o aprendizado de programação parecer mais divertido, focado e memorável.

---

## Author

Created by **Mackson Victor**.

GitHub:

```txt
github.com/macksonvictor
```

---

## Project Status

Mompy is currently in active development.

This repository may change frequently while the interface, mission system, audio, and desktop packaging are being completed.

---

## License

License not defined yet.

Until a license is chosen, all rights are reserved by the author.
