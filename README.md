# 🎓 EduTutor — Adaptive AI Tutor

> An adaptive AI tutoring system built with **LangGraph**, **Streamlit**, and the **GitHub Models API**.

---

## 🏗️ Architecture

```
topic_loader → strategy_selector → explainer → question_generator
                      ↑                               ↓
                (retry edge)         [INTERRUPT before response_evaluator]
                      |                               ↓
                      └──── decision_gate ←── response_evaluator
                                   |
                              (done edge)
                                   ↓
                           mastery_recorder → END
```

### True LangGraph Interrupt-Resume Cycle
1. `graph.invoke(init, config)` runs: `topic_loader → strategy_selector → explainer → question_generator`
2. Graph **pauses** at `interrupt_before=["response_evaluator"]`
3. Student types their answer in the Streamlit UI
4. `graph.invoke(Command(resume=answer), config)` **resumes** — `response_evaluator` receives the answer as its second positional arg
5. `decision_gate` routes: `confidence ≥ 0.8 OR attempts ≥ 3` → `mastery_recorder → END`, else → `strategy_selector` (retry)

---

## ✨ Key Features

| Feature | Detail |
|---------|--------|
| **5 Teaching Strategies** | Analogy, Example, Step-by-Step, Visual, Socratic |
| **Smart Strategy Selection** | STRATEGY_PRIORITY matrix routes based on failure type (no_understanding / partial / almost) |
| **Context-Aware Retry** | Explainer addresses the specific misconception identified in prior feedback |
| **Adaptive Difficulty** | Questions escalate: recall → application → analysis across attempts |
| **No Answer Leakage** | Multi-layer regex filter strips any answer-revealing lines from questions |
| **SQLite Persistence** | `SqliteSaver` checkpointer + `concept_mastery` table survive restarts |
| **Cross-Concept Mastery** | Persistent leaderboard across all sessions and concepts |
| **LangGraph Graph Viz** | Sidebar expander shows `draw_mermaid()` output |
| **Custom Concept Input** | Any CS/math concept via Wikipedia — not just 6 presets |
| **Rich Extras** | Plotly charts, worked examples, code snippets, fun facts per concept |

---

## 🚀 Setup

### 1. Clone & install

```bash
git clone <your-repo-url>
cd EduTutor
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your GitHub token:
# GITHUB_TOKEN=ghp_your_token_here
```

Get a free token at [github.com/settings/tokens](https://github.com/settings/tokens) — no special scopes needed for GitHub Models.

### 3. Run

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
EduTutor/
├── app.py                  # Streamlit UI (glassmorphism design)
├── agent/
│   ├── graph.py            # LangGraph StateGraph + SqliteSaver
│   ├── nodes.py            # 6 nodes: loader, selector, explainer, question_gen, evaluator, mastery_recorder
│   ├── state.py            # EduTutorState TypedDict
│   ├── data_fetcher.py     # Wikipedia MediaWiki API
│   └── concept_extras.py   # Plotly charts, code, facts per concept
├── edututor.db             # SQLite — LangGraph checkpoints + mastery table (auto-created)
├── requirements.txt
└── .env.example
```

---

## 📋 Rubric Checklist

| Rubric Requirement | Implementation |
|-------------------|---------------|
| ✅ LangGraph agent with reflection loop | `graph.py` — `strategy_selector ↔ response_evaluator` via `decision_gate` |
| ✅ `interrupt_before` pause | `interrupt_before=["response_evaluator"]` |
| ✅ True interrupt-resume via `Command(resume=)` | `submit_answer()` uses `g.invoke(Command(resume=answer), cfg)` |
| ✅ Persistent checkpointing | `SqliteSaver` with `edututor.db` |
| ✅ Confidence shown in UI | Progress bar + percentage in sidebar and explaining phase |
| ✅ No strategy repetition | `strategies_used` list tracked in state |
| ✅ 4+ explanation strategies | 5: analogy, example, step_by_step, visual, socratic |
| ✅ Adaptive difficulty | 3-tier difficulty: recall → application → analysis |
| ✅ Mastery tracking | `concept_mastery` SQLite table + cross-session leaderboard |
| ✅ Graph visualisation | Sidebar "Agent Graph" expander with `draw_mermaid()` |
| ✅ Rich extras per concept | Plotly charts, code, worked examples, fun facts tabs |

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub personal access token for [GitHub Models API](https://github.com/marketplace/models) |

The app uses `gpt-4o-mini` via the GitHub Models inference endpoint (`https://models.inference.ai.azure.com`) — **completely free** with a GitHub account.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue if you have suggestions for new teaching strategies or UI improvements.
