<p align="center">
  <img src="assets/branding/mompy-cover.webp" alt="Mompy monitor showing GitHub logo" width="420">
</p>

# Mompy: Learn Python with a Retro Training Console

[![Status](https://img.shields.io/badge/status-in%20development-8cff3a?style=for-the-badge)](#-project-status)
[![Platform](https://img.shields.io/badge/platform-cross--platform-6f42c1?style=for-the-badge)](#-platform--releases)
[![HTML CSS JS](https://img.shields.io/badge/HTML%20%7C%20CSS%20%7C%20JS-f7df1e?style=for-the-badge&logo=javascript&logoColor=black)](#-technology-stack)
[![Electron](https://img.shields.io/badge/desktop-Electron-47848f?style=for-the-badge&logo=electron&logoColor=white)](#-desktop-app)
[![Python](https://img.shields.io/badge/python-training-3776ab?style=for-the-badge&logo=python&logoColor=white)](#-what-mompy-does)
[![Discord](https://img.shields.io/badge/Discord-coming%20soon-5865F2?style=for-the-badge&logo=discord&logoColor=white)](#-community)
[![Issues](https://img.shields.io/github/issues/hepterakt-studios/mompy?style=for-the-badge&logo=github)](https://github.com/hepterakt-studios/mompy/issues)
[![Stars](https://img.shields.io/github/stars/hepterakt-studios/mompy?style=for-the-badge&logo=github)](https://github.com/hepterakt-studios/mompy/stargazers)

[English](https://zdoc.app/en/hepterakt-studios/mompy) | [Português](https://zdoc.app/pt/hepterakt-studios/mompy)

**Mompy** is a retro CRT-style desktop app that helps beginners learn Python through guided missions, instant feedback, local progress, sound effects, and a friendly monitor mascot.

> [!NOTE]
> Mompy is in active development. Source code is available now. Desktop downloads will be published through GitHub Releases when the first builds are ready.

---

## 📦 Download and source

- **Source code:** [github.com/hepterakt-studios/mompy](https://github.com/hepterakt-studios/mompy)
- **Desktop downloads:** [GitHub Releases](https://github.com/hepterakt-studios/mompy/releases)
- **Official website:** [mompy.co](https://mompy.co)
- **Issues and feedback:** [GitHub Issues](https://github.com/hepterakt-studios/mompy/issues)

Mompy is being prepared as a cross-platform desktop app. Each operating system may receive its own package.

| Platform | Package | Status |
| --- | --- | --- |
| Windows | installer / executable | Planned |
| macOS | disk image package | Planned |
| Linux | portable Linux package | Planned |
| Web preview | browser preview or documentation page | Possible later |

---

## 🧠 What Mompy does

Mompy turns beginner Python practice into small interactive missions.

The app is designed to:

- teach Python step by step;
- give the user short coding challenges;
- validate the code written by the user;
- show output and feedback immediately;
- save progress locally;
- react with animations and sounds;
- make learning feel like using an old intelligent training terminal.

The goal is simple: **open Mompy, complete missions, learn Python, and keep progressing.**

---

## 🧩 Core learning loop

1. Open the app.
2. Wait for the CRT-style loading screen.
3. Start or continue training.
4. Read the mission.
5. Write Python code.
6. Run the code.
7. Receive feedback from Mompy.
8. Complete the mission and unlock the next one.

---

## 🖥️ App experience

| Area | Purpose |
| --- | --- |
| Loading screen | CRT-style boot sequence with a real loading bar and no sound. |
| Start screen | Entry point with Start, Continue, local profile, level, and mission count. |
| Mission screen | Main learning area with objective, code editor, output, and controls. |
| Completion flow | Mompy reacts, shows success, and lets the user repeat or continue. |
| Settings | Local profile, language, audio controls, and progress reset. |

---

## 🎨 Visual identity

Mompy uses a retro-futuristic visual style inspired by old terminals, CRT monitors, and industrial control panels.

- dark industrial interface;
- green CRT glow;
- terminal-style typography;
- pixel/scanline effects;
- metallic panels;
- retro monitor mascot;
- old-computer atmosphere.

Mompy should feel like an old intelligent training machine, not a normal website.

---

## 🧭 Feature status

| Area | Status |
| --- | --- |
| Retro CRT interface | In development |
| Loading screen | In development |
| Start screen | In development |
| Mission screen | In development |
| Code editor and output | In development |
| Help / Run / Back buttons | In development |
| Settings modal | In development |
| Local user profile | Planned / in progress |
| Local progress saving | Planned / in progress |
| Mompy mascot states | Planned / in progress |
| Mission completion flow | Planned / in progress |
| Audio system | Planned / in progress |
| Electron packaging | Planned |
| GitHub Releases | Planned |
| Official website | Planned |
| Discord community | Planned |

---

## 🚀 Roadmap

| Stage | Focus |
| --- | --- |
| Now | Finish the core UI, mission flow, local profile, progress system, audio, and mascot behavior. |
| Next | Package Mompy as a desktop app and prepare first test builds for Windows, macOS, and Linux. |
| Later | Publish releases, launch the official website, expand missions, add documentation, and open community channels. |

---

## 🔒 Local-first philosophy

Mompy is designed to work without requiring an online account. For the first version, the user's first name, language preference, current mission, completed missions, audio settings, interface settings, and progress state should stay on the user's computer.

Future online features may exist, but they should be optional.

---

## 💻 Desktop app

Mompy is being built with web technologies, but the final goal is to make it feel like a real installed desktop app.

```txt
HTML + CSS + JavaScript
↓
Electron
↓
Desktop app releases
```

```txt
Mompy app = installable desktop app
mompy.co = official website / download page
GitHub Releases = app downloads
```

---

## 🌍 Platform & releases

Mompy should be cross-platform, not Windows-only.

| Platform | Status |
| --- | --- |
| Windows | Planned |
| macOS | Planned |
| Linux | Planned |
| Web preview | Possible future option, mainly for preview or documentation |

Each operating system may need its own build/package later. GitHub Releases can contain separate downloads for each platform.

---

## 🧰 Requirements

### For users

- Windows, macOS, or Linux depending on the release package;
- keyboard and mouse;
- enough storage for a small desktop app;
- no required online account for the first version.

### For developers

- Git;
- Node.js;
- npm;
- VS Code or another code editor;
- Electron / Electron Builder when desktop packaging is configured.

---

## 🛠️ Technology stack

- HTML;
- CSS;
- JavaScript;
- LocalStorage;
- Electron;
- Electron Builder;
- Git;
- GitHub;
- GitHub Releases.

Possible future additions:

- local file storage;
- cloud sync;
- mission editor;
- AI-assisted hints.

---

## 📁 Project structure

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
      branding/
  electron/
    main.js
    preload.js
  README.md
  package.json
  .gitignore
```

---

## ⚙️ Development

Clone the repository:

```bash
git clone https://github.com/hepterakt-studios/mompy.git
cd mompy
```

Install dependencies:

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

> [!NOTE]
> The development commands may change while the Electron structure is being completed.

---

## 🏗️ Build

When Electron is configured, the app should be built with:

```bash
npm run build
```

Do not commit generated builds, dependency folders, installers, temporary files, or local environment files.

Installers and packaged builds should be published later through **GitHub Releases**.

---

## 🔊 Audio files

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

- Loading screen: no sound;
- Start screen: ambient sound only;
- Mission screen: sound effects only;
- Run: run sound;
- Correct answer: success sound;
- Wrong answer: error sound;
- CRT shutdown animation: shutdown sound.

---

## 🧪 Test checklist

Before a public release:

- [ ] Loading screen appears and transitions correctly.
- [ ] Start and Continue work.
- [ ] Local user profile loads correctly.
- [ ] Mission screen validates code correctly.
- [ ] Output updates correctly.
- [ ] Mompy reacts correctly.
- [ ] Audio behavior is correct per screen.
- [ ] Progress is saved locally.
- [ ] Build folders are not committed.
- [ ] README and project files are updated.

---

## 🌐 Official website

Planned official website:

```txt
https://mompy.co
```

The website can be used for project presentation, screenshots, downloads, release notes, and documentation.

---

## 🤔 Questions? Problems? Suggestions?

Report bugs, request features, or suggest improvements through [GitHub Issues](https://github.com/hepterakt-studios/mompy/issues).

Use the issue templates when opening a new report:

- [Bug report](https://github.com/hepterakt-studios/mompy/issues/new?template=bug_report.md)
- [Feature request](https://github.com/hepterakt-studios/mompy/issues/new?template=feature_request.md)

Security reports should follow the [Security Policy](SECURITY.md).

---

## 💬 Community

Discord community: **coming soon**.

---

## 🤝 Project ecosystem

| Project | Status | Description |
| --- | --- | --- |
| **Mompy Desktop** | Current repository | The main retro Python training app. |
| **Mompy Website** | Planned | Official website for downloads, screenshots, releases, and documentation. |
| **Mompy Missions** | Planned | Future Python lesson and challenge packs. |
| **Mompy Docs** | Planned | Future documentation for users, developers, and contributors. |

---

## ⭐ Stars stats

<p align="center">
  <a href="https://star-history.com/#hepterakt-studios/mompy&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=hepterakt-studios/mompy&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=hepterakt-studios/mompy&type=Date" />
      <img alt="Mompy Star History Chart" src="https://api.star-history.com/svg?repos=hepterakt-studios/mompy&type=Date" />
    </picture>
  </a>
</p>

---

## ⚡ Contributors

<a href="https://github.com/hepterakt-studios/mompy/graphs/contributors" alt="View Contributors">
  <img src="https://contrib.rocks/image?repo=hepterakt-studios/mompy&max=1000&columns=10" alt="Mompy contributors" />
</a>

---

## 📚 Project standards

These files are also available in the GitHub repository navigation when supported by GitHub:

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [License](LICENSE)

---

## 👤 Author

Created by **Mackson Victor**.

GitHub: [macksonvictor](https://github.com/macksonvictor)

Organization: [Hepterakt Studios](https://github.com/hepterakt-studios)

---

## 📌 Project status

Mompy is currently in active development.

This repository may change frequently while the interface, mission system, audio, and desktop packaging are being completed.

---

## 📄 License

Mompy is not currently released under an open-source license.

See [LICENSE](LICENSE) for the current project notice.
