# Spot Problem Solver Platform 🚀

**Tagline**: *“Spot a Problem. Build a Solution. Create an Impact.”*

Spot Problem Solver is a modern, collaborative problem-solving platform connecting real-world challenges from government bodies, universities, companies, NGOs, and communities with innovators, researchers, developers, startups, and technology.

---

## 📁 File Structure

```text
spot_problem_solver/
├── start_spot_solver.bat         # 1-Click Launcher script for Windows
├── app.py                         # Flask Web Server & REST API Backend
├── database.py                    # SQLite Database Schema & Demo Data Seed Script
├── spot_solver.db                 # SQLite Database file
├── spot_problem_solver_standalone.html # Single-file standalone HTML version
├── static/
│   ├── css/
│   │   └── custom.css             # Brand styling, glassmorphism & animations
│   └── js/
│       └── app.js                 # SPA Router, state management & AI logic
└── templates/
    └── index.html                 # Main Single Page Application shell
```

---

## ⚡ How to Run

1. **Option A: 1-Click Launcher**
   - Double-click `start_spot_solver.bat` in the project folder.
   - The web server will start and automatically open `http://127.0.0.1:5000` in your web browser.

2. **Option B: Command Line**
   ```bash
   python database.py
   python app.py
   ```
   Then open `http://127.0.0.1:5000` in your browser.

3. **Option C: Standalone Single File**
   - Double-click `spot_problem_solver_standalone.html` to open the full interactive platform directly in any web browser without running a server.

---

## ✨ Features Included

- **Marketplace**: Search & filter real-world problems across 15 categories (Water, Healthcare, Agriculture, AI, Disaster Management, etc.).
- **Multi-step Problem Wizard**: 4-step structured posting form.
- **Solution Submission**: Submit technical proposals with demo links, GitHub repos, costs, and tech stack tags.
- **Challenges**: Organization-sponsored challenges with prize pools and status badges.
- **Team Collaboration**: Team directory, skill tag recruitment, and member join system.
- **Leaderboard & Gamification**: Points rankings and badges (*Problem Spotter, Solution Builder, Innovation Leader, Impact Maker*).
- **AI Problem & Solution Assistants**: Automated root cause analysis, tech approaches, and proposal feedback.
- **Admin Dashboard**: Live editable statistics counters, moderation queue, and Chart.js analytics charts.
