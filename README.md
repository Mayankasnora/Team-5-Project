<div align="center">

<!-- Animated Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=200&section=header&text=EduTutor%20AI&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=Adaptive%20AI%20Tutoring%20System&descAlignY=58&descSize=20&animation=fadeIn" width="100%"/>

<!-- Badges Row 1 -->
<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangGraph-Agent-FF6B35?style=for-the-badge&logo=langchain&logoColor=white"/>
  <img src="https://img.shields.io/badge/GPT--4o--mini-GitHub%20Models-24292e?style=for-the-badge&logo=openai&logoColor=white"/>
</p>

<!-- Badges Row 2 -->
<p>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/SQLite-Persistence-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/github/forks/Mayankasnora/EduTutor-AI?style=for-the-badge&color=764ba2"/>
</p>

<br/>

> 🎓 **An adaptive AI tutoring system** that learns *how you learn* — powered by **LangGraph**, **Streamlit**, and the **GitHub Models API** (completely free).

<br/>

<!-- Quick Nav -->
**[✨ Features](#-key-features) · [🏗️ Architecture](#️-architecture) · [🚀 Setup](#-setup) · [📁 Structure](#-project-structure) · [👥 Team](#-team)**

<br/>

</div>

---

## 🌟 What Makes EduTutor Different?

<table>
<tr>
<td width="50%">

**🧠 It adapts to YOU**
EduTutor doesn't just explain once and move on. It detects *why* you're stuck — no understanding, partial grasp, or almost there — and picks the perfect teaching strategy to address your specific gap.

</td>
<td width="50%">

**🔁 True Interrupt-Resume AI Loop**
Built on LangGraph's `interrupt_before` mechanism, the agent genuinely pauses mid-graph, waits for your answer, then resumes with full context — not a chatbot pretending to think.

</td>
</tr>
<tr>
<td width="50%">

**📈 Tracks mastery across sessions**
SQLite persistence means your progress survives restarts. A leaderboard tracks concept mastery across all sessions.

</td>
<td width="50%">

**🆓 Completely free to run**
Uses `gpt-4o-mini` via the GitHub Models inference endpoint — just a free GitHub account needed.

</td>
</tr>
</table>

---

## ✨ Key Features

<div align="center">

| 🎯 Feature | 📋 Detail |
|:---|:---|
| **5 Teaching Strategies** | Analogy · Example · Step-by-Step · Visual · Socratic |
| **Smart Strategy Selection** | `STRATEGY_PRIORITY` matrix routes based on failure type (`no_understanding` / `partial` / `almost`) |
| **Context-Aware Retry** | Explainer addresses the *specific* misconception from prior feedback |
| **Adaptive Difficulty** | Questions escalate: `recall → application → analysis` |
| **No Answer Leakage** | Multi-layer regex filter strips answer-revealing lines from questions |
| **SQLite Persistence** | `SqliteSaver` checkpointer + `concept_mastery` table survive restarts |
| **Cross-Concept Mastery** | Persistent leaderboard across all sessions and concepts |
| **LangGraph Graph Viz** | Sidebar expander shows live `draw_mermaid()` output |
| **Custom Concept Input** | Any CS/math concept via Wikipedia — not limited to presets |
| **Rich Extras** | Plotly charts · worked examples · code snippets · fun facts per concept |

</div>

---

## 🏗️ Architecture
```mermaid
flowchart TD
    A([▶ START]) --> B
    B["📥 topic_loader — Fetches topic via Wikipedia API"] --> C
    C["🧭 strategy_selector — Picks strategy via STRATEGY_PRIORITY matrix"] --> D
    D["💡 explainer — Explains with targeted teaching strategy"] --> E
    E["❓ question_generator — Generates adaptive question, no answer leakage"] --> F
    F{{"⏸ INTERRUPT — interrupt_before=response_evaluator"}}
    F -- "student submits answer" --> G
    G["🔍 response_evaluator — Scores answer, detects misconception type"] --> H
    H{"🚦 decision_gate — confidence ≥ 0.8 OR attempts ≥ 3?"}
    H -- "✅ Yes — done" --> I
    H -- "❌ No — retry" --> C
    I["🏆 mastery_recorder — Writes to concept_mastery SQLite table"] --> J([⏹ END])

    style A fill:#2d1b69,stroke:#7c3aed,color:#fff
    style J fill:#2d1b69,stroke:#7c3aed,color:#fff
    style F fill:#92400e,stroke:#f59e0b,color:#fef3c7
    style H fill:#1e3a5f,stroke:#3b82f6,color:#dbeafe
    style B fill:#1e1b4b,stroke:#6366f1,color:#e0e7ff
    style C fill:#1e1b4b,stroke:#6366f1,color:#e0e7ff
    style D fill:#064e3b,stroke:#10b981,color:#d1fae5
    style E fill:#064e3b,stroke:#10b981,color:#d1fae5
    style G fill:#78350f,stroke:#f59e0b,color:#fef3c7
    style I fill:#14532d,stroke:#22c55e,color:#dcfce7
```
### 🔄 How the Interrupt-Resume Cycle Works

```
Step 1  graph.invoke(init, config)
        └─► topic_loader → strategy_selector → explainer → question_generator
                                                                    │
Step 2                                              Graph PAUSES ◄──┘
                                         interrupt_before=["response_evaluator"]
                                                        │
Step 3                              Student types answer in Streamlit UI
                                                        │
Step 4  graph.invoke(Command(resume=answer), config)    │
        └─► response_evaluator receives answer ◄────────┘
                        │
Step 5          decision_gate routes:
                ├── confidence ≥ 0.8 OR attempts ≥ 3  →  mastery_recorder → END
                └── else  →  strategy_selector (retry with new strategy)
```

---

## 🚀 Setup

### 1. Clone & install

```bash
git clone https://github.com/Mayankasnora/EduTutor-AI.git
cd EduTutor-AI
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your GitHub token:
# GITHUB_TOKEN=ghp_your_token_here
```

> 💡 Get a free token at [github.com/settings/tokens](https://github.com/settings/tokens) — no special scopes needed for GitHub Models.

### 3. Run

```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser. 🎉

---

## 📁 Project Structure

```
EduTutor-AI/
│
├── 📄 app.py                   # Streamlit UI (glassmorphism design)
├── 📄 requirements.txt
├── 📄 .env.example
│
└── 📂 agent/
    ├── 🔗 graph.py             # LangGraph StateGraph + SqliteSaver
    ├── 🧩 nodes.py             # 6 nodes: loader, selector, explainer,
    │                           #          question_gen, evaluator, mastery_recorder
    ├── 📦 state.py             # EduTutorState TypedDict
    ├── 🌐 data_fetcher.py      # Wikipedia MediaWiki API
    └── 🎨 concept_extras.py    # Plotly charts, code, facts per concept

📄 edututor.db                  # SQLite — LangGraph checkpoints + mastery table
                                # (auto-created on first run)
```

---

## 📋 Rubric Checklist

<div align="center">

| ✅ Requirement | 🔧 Implementation |
|:---|:---|
| LangGraph agent with reflection loop | `graph.py` — `strategy_selector ↔ response_evaluator` via `decision_gate` |
| `interrupt_before` pause | `interrupt_before=["response_evaluator"]` |
| True interrupt-resume via `Command(resume=)` | `submit_answer()` uses `g.invoke(Command(resume=answer), cfg)` |
| Persistent checkpointing | `SqliteSaver` with `edututor.db` |
| Confidence shown in UI | Progress bar + percentage in sidebar and explaining phase |
| No strategy repetition | `strategies_used` list tracked in state |
| 4+ explanation strategies | 5: `analogy`, `example`, `step_by_step`, `visual`, `socratic` |
| Adaptive difficulty | 3-tier: `recall → application → analysis` |
| Mastery tracking | `concept_mastery` SQLite table + cross-session leaderboard |
| Graph visualisation | Sidebar "Agent Graph" expander with `draw_mermaid()` |
| Rich extras per concept | Plotly charts · code · worked examples · fun facts |

</div>

---

## 🔑 Environment Variables

| Variable | Description |
|:---|:---|
| `GITHUB_TOKEN` | GitHub personal access token for [GitHub Models API](https://github.com/marketplace/models) |

The app uses `gpt-4o-mini` via the GitHub Models inference endpoint (`https://models.inference.ai.azure.com`) — **completely free** with a GitHub account.

---

## 👥 Team

<div align="center">

**Built with ❤️ by Team 5** — *Deploying and Building AI Agents*

| Member | GitHub |
|:---:|:---:|
| Mayank Asnora | [@Mayankasnora](https://github.com/Mayankasnora) |

</div>

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. Create your feature branch: `git checkout -b feat/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feat/amazing-feature`
5. Open a **Pull Request**

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:764ba2,100:667eea&height=100&section=footer" width="100%"/>

**If you found this project useful, please consider giving it a ⭐ — it means a lot!**

</div>
