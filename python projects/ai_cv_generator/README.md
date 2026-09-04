# 📄 AI Resumix Pro — Intelligent CV & Resume Builder

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![ReportLab PDF](https://img.shields.io/badge/ReportLab-Vector_PDF-007ACC?style=for-the-badge)](https://www.reportlab.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**AI Resumix Pro** is a modern, full-stack Python application that empowers job seekers and engineers to craft high-impact, ATS-optimized CVs and Resumes powered by Generative AI.

Featuring a dark glassmorphism Streamlit UI, real-time PDF generation across multiple design themes, automated STAR-formula bullet point polishing, and an instant ATS Keyword Compatibility Analyzer.

---

## 🌟 Key Features

- **✨ Generative AI Resume Studio**:
  - **AI Executive Summary Generator**: Crafts tailored 60-80 word summary statements matching target roles.
  - **STAR Bullet Point Polisher**: Rewrites raw bullet points into action-driven statements with metrics.
  - **Skill Taxonomy Recommender**: Auto-suggests high-demand technical and soft skills for any job title.
- **🎯 ATS Keyword & Score Analyzer**:
  - Paste any job posting description to receive an instant **ATS Match Score (0–100%)**.
  - Highlights matched keywords vs. missing critical industry keywords.
  - 1-Click auto-merge missing keywords into your resume skill list.
- **📄 Vector PDF Export Engine (ReportLab)**:
  - 3 professional visual themes: **Modern Executive**, **Creative Tech**, and **Minimalist Classic**.
  - Crisp typography, balanced margins, printable vector quality.
- **⚡ Dual AI Mode + Smart Offline Fallback**:
  - Works with **Google Gemini 1.5** or **OpenAI GPT-3.5/4**.
  - Includes a **Smart Heuristic Engine** out-of-the-box so the app functions seamlessly without an API key!
- **💾 Profile Persistence**: Save and reload resume profiles in JSON format for quick updates.

---

## 🏗️ Architecture

```mermaid
graph TD
    User([👤 User / Candidate]) --> UI[🎨 Streamlit Glassmorphism Interface]
    
    subgraph Core Engine
        UI --> Editor[📝 Interactive Resume Form]
        UI --> AI_Studio[✨ AI Enhancement Studio]
        UI --> ATS_Analyzer[🎯 ATS Keyword Matcher]
    end
    
    subgraph AI Processing Layer
        AI_Studio --> Router{API Key Configured?}
        Router -- Yes (Gemini/OpenAI) --> CloudAI[☁️ LLM APIs]
        Router -- No --> OfflineAI[🧠 Smart Heuristic Engine]
    end
    
    subgraph Export Engine
        UI --> PDFGen[📄 ReportLab PDF Generator]
        PDFGen --> Themes[🎨 3 Modern Visual Themes]
        Themes --> PDF[📥 Downloadable Vector PDF]
    end
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-cv-generator.git
cd ai-cv-generator
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. (Optional) Configure Environment Variables
Copy `.env.example` to `.env` and add your Gemini or OpenAI API keys:
```bash
cp .env.example .env
```

### 4. Run the Streamlit Application
```bash
python -m streamlit run app.py
```

The web application will launch at `http://localhost:8501`.

---

## 📲 Ready-to-Post LinkedIn Post Template

> *Copy & paste this exact template to post your project on LinkedIn:*

```markdown
🚀 Excited to launch my latest Python project: AI Resumix Pro! 📄🤖

Creating a standout resume shouldn't take hours of manual formatting or guessing what ATS scanners want. So I built an end-to-end AI-powered Resume & CV Generator with a sleek dark glassmorphism interface!

✨ Key Features:
🔹 AI STAR Bullet Rewriter: Transforms weak descriptions into metric-driven accomplishment statements.
🔹 ATS Keyword & Score Analyzer: Evaluates job description match % and highlights missing key terms.
🔹 Multi-Theme PDF Engine: Renders crisp vector PDFs across 3 modern design styles (Modern Executive, Creative Tech, Minimalist Classic).
🔹 Dual-Engine AI: Supports Google Gemini, OpenAI, and a zero-config Smart Offline engine.

🛠️ Built with Python, Streamlit, Google Gemini AI API, and ReportLab.

Check out the code & star the repo on GitHub! 👇
[Insert your GitHub Repo Link Here]

#Python #AI #MachineLearning #Streamlit #OpenSource #SoftwareEngineering #CareerGrowth #WebDevelopment #GenerativeAI
```

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
