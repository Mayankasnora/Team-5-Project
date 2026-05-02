"""
EduTutor Agent Nodes — Upgraded AI Logic
- Smart strategy selection (based on failure type)
- Context-aware explanations (addresses prior misconception)
- Adaptive question generation (targets known gaps)
- Rich evaluation (identifies exact misconception + actionable feedback)
- Better data fetching (MediaWiki full intro)
"""
import json
import os
import random
import re

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .state import EduTutorState
from .data_fetcher import fetch_wikipedia_summary

load_dotenv()

# ── Strategy catalogue ────────────────────────────────────────────────────────
STRATEGIES = ["analogy", "example", "step_by_step", "visual", "socratic"]

STRATEGY_PROFILES = {
    "analogy": {
        "description": "Connect the concept to something the student already knows through a vivid, memorable metaphor or real-world comparison.",
        "best_for": "When the student has no mental model — build intuition first.",
        "template": "Use ONE compelling analogy. Introduce it clearly, show exactly how it maps to the concept, then reinforce with a concrete statement.",
    },
    "example": {
        "description": "Walk through 2-3 concrete, fully-worked examples with real numbers, real code, or real scenarios.",
        "best_for": "When the student understands the idea but can't apply it.",
        "template": "Show Example 1 (simple), Example 2 (medium), Example 3 (tricky edge case). Label each. Use code blocks for code.",
    },
    "step_by_step": {
        "description": "Break the concept into a clearly numbered sequence of logical steps like a recipe or algorithm.",
        "best_for": "When the student is lost in the process or skips important steps.",
        "template": "Number each step 1, 2, 3… Keep each step atomic. Add a 'Why this step matters' note for key steps.",
    },
    "visual": {
        "description": "Draw ASCII diagrams, trees, flowcharts, tables, or spatial layouts to make the structure visible.",
        "best_for": "When the concept has structure or flow that words alone can't convey.",
        "template": "Start with a diagram or table. Label all elements. Walk through the diagram step by step.",
    },
    "socratic": {
        "description": "Guide the student to discover the answer themselves through a chain of logical questions and brief answers.",
        "best_for": "When the student partially understands — push them to reason it out.",
        "template": "Ask Q1 → give answer → ask Q2 → give answer → … → arrive at the concept organically. Keep each Q-A pair tight.",
    },
}

# Strategy scoring to pick the BEST next strategy given prior failure
STRATEGY_PRIORITY = {
    "no_understanding": ["analogy", "visual", "step_by_step", "example", "socratic"],
    "partial":          ["example", "step_by_step", "analogy", "socratic", "visual"],
    "almost":           ["socratic", "example", "step_by_step", "visual", "analogy"],
}


def _llm(temperature: float = 0.7) -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=temperature,
        api_key=os.getenv("GITHUB_TOKEN"),
        base_url="https://models.inference.ai.azure.com",
    )


def _parse_json(text: str, default: dict) -> dict:
    """Robustly extract the first JSON object from an LLM response."""
    try:
        s, e = text.find("{"), text.rfind("}") + 1
        if s != -1 and e > s:
            return json.loads(text[s:e])
    except Exception:
        pass
    return default


# ══════════════════════════════════════════════════════════════════════════════
# NODE 1: topic_loader
# ══════════════════════════════════════════════════════════════════════════════
def topic_loader(state: EduTutorState) -> dict:
    """Load concept text from Wikipedia and initialise all session fields."""
    concept_text = fetch_wikipedia_summary(state["concept"])
    return {
        "concept_text":      concept_text,
        "strategies_used":   [],
        "student_answers":   [],
        "confidence":        0.0,
        "attempts":          0,
        "current_strategy":  "",
        "current_explanation": "",
        "current_question":  "",
        "last_feedback":     "",
    }


# ══════════════════════════════════════════════════════════════════════════════
# NODE 2: strategy_selector  (SMART — picks best given failure history)
# ══════════════════════════════════════════════════════════════════════════════
def strategy_selector(state: EduTutorState) -> dict:
    """
    Pick the most pedagogically appropriate unused strategy.
    - Attempt 1: random from all strategies
    - Attempt 2+: classify failure type, then pick best matching strategy
    Returns strategy_change_reason so the UI can show the "Why did strategy change?" callout.
    """
    used      = list(state.get("strategies_used", []))
    attempts  = state.get("attempts", 0)
    available = [s for s in STRATEGIES if s not in used]
    if not available:
        available = STRATEGIES  # safety net

    change_reason = ""

    if attempts == 0:
        # First attempt — pick randomly but with slight bias toward analogy/example
        preferred = [s for s in ["analogy", "example", "step_by_step"] if s in available]
        choice = random.choice(preferred if preferred else available)
    else:
        # Smart selection: classify failure then rank available strategies
        confidence = state.get("confidence", 0.0)

        if confidence < 0.35:
            failure_type = "no_understanding"
            change_reason = f"You scored {int(confidence*100)}% — showing a fundamental gap, switching to a more intuitive approach."
        elif confidence < 0.65:
            failure_type = "partial"
            change_reason = f"You scored {int(confidence*100)}% — you have partial understanding, switching to a concrete example-based approach."
        else:
            failure_type = "almost"
            change_reason = f"You scored {int(confidence*100)}% — you're almost there! Switching to a Socratic approach to push your reasoning."

        priority = STRATEGY_PRIORITY[failure_type]
        choice = next((s for s in priority if s in available), available[0])

    return {
        "current_strategy":   choice,
        "strategies_used":    used + [choice],
        "strategy_change_reason": change_reason,
    }


# ══════════════════════════════════════════════════════════════════════════════
# NODE 3: explainer  (context-aware — addresses prior misconception)
# ══════════════════════════════════════════════════════════════════════════════
def explainer(state: EduTutorState) -> dict:
    """
    Generate a rich, strategy-specific explanation.
    On retry: explicitly addresses what the student got wrong.
    """
    concept      = state["concept"]
    concept_text = state["concept_text"]
    strategy     = state["current_strategy"]
    level        = state["student_level"]
    attempts     = state.get("attempts", 0)
    feedback     = state.get("last_feedback", "")
    answers      = state.get("student_answers", [])
    last_answer  = answers[-1] if answers else ""

    profile = STRATEGY_PROFILES[strategy]

    level_guide = {
        "beginner":     "Use plain English. Avoid jargon. Add a simple analogy alongside the main one.",
        "intermediate": "You can use proper terminology. Assume basic CS knowledge.",
        "advanced":     "Use technical precision. Reference edge cases and complexity trade-offs.",
    }[level]

    retry_block = ""
    if attempts > 0 and last_answer:
        retry_block = f"""
CRITICAL CONTEXT — The student's previous answer was:
"{last_answer}"

Evaluator said: "{feedback}"

You MUST:
1. Start by addressing WHY their answer was incomplete or incorrect (1-2 sentences)
2. Then pivot to explaining the concept using the {strategy} strategy
3. Make it clear what the correct understanding looks like
"""

    system = f"""You are EduTutor — a world-class adaptive tutor for computer science and mathematics.

STUDENT LEVEL: {level}
MANDATORY STRATEGY: {strategy.upper().replace("_", " ")}

Strategy guide:
- What it is: {profile["description"]}
- Best for: {profile["best_for"]}
- How to structure it: {profile["template"]}

Level calibration: {level_guide}

Formatting rules:
- Use **bold** for key terms on first use
- Use ```code blocks``` for any code or pseudocode
- Use bullet points or numbered lists where the strategy calls for it
- Target 200-280 words — not shorter, not longer
- End with one clear "Key Takeaway:" sentence
{retry_block}"""

    user = f"""Explain '{concept}' using the {strategy.replace("_", " ")} strategy.

Reference material (use relevant parts, don't quote directly):
{concept_text[:1800]}

Produce the explanation now."""

    try:
        resp = _llm(0.65).invoke([SystemMessage(content=system), HumanMessage(content=user)])
        explanation = resp.content
    except Exception as e:
        explanation = f"⚠️ Could not generate explanation right now ({type(e).__name__}). Please retry."
    return {"current_explanation": explanation}


# ══════════════════════════════════════════════════════════════════════════════
# NODE 4: question_generator  (targeted — exploits known gaps)
# ══════════════════════════════════════════════════════════════════════════════
def question_generator(state: EduTutorState) -> dict:
    """
    Generate one comprehension question that tests exactly what the student struggled with.
    Difficulty escalates each attempt. Question type adapts to level.
    """
    concept     = state["concept"]
    explanation = state["current_explanation"]
    level       = state["student_level"]
    attempts    = state.get("attempts", 0)
    answers     = state.get("student_answers", [])
    last_answer = answers[-1] if answers else ""
    feedback    = state.get("last_feedback", "")

    difficulty_map = {
        0: ("straightforward recall",  "Tests if the student grasped the core idea"),
        1: ("application",             "Tests if they can apply the concept in a new scenario"),
        2: ("analysis or comparison",  "Tests deep understanding — ask why, compare, or identify edge cases"),
    }
    diff_label, diff_goal = difficulty_map[min(attempts, 2)]

    # All questions are short-answer — no MCQ to prevent any answer leakage
    if attempts == 0:
        q_type   = "short answer (1 clear sentence)"
        constraint = "Ask about the core concept — what is it and what does it do?"
    elif attempts == 1:
        q_type   = "short answer requiring an example or scenario (2 sentences)"
        constraint = "Ask the student to give an example or apply the concept to a real situation."
    else:
        q_type   = "short answer requiring reasoning or comparison (2-3 sentences)"
        constraint = "Ask WHY, HOW, or to compare with a related concept they might know."

    gap_context = ""
    if last_answer and feedback:
        gap_context = f"""
The student previously answered: "{last_answer}"
Their gap: {feedback}
Make your question specifically target this gap — don't let them dodge it."""

    system = f"""You are creating a precisely targeted comprehension question.

Concept: {concept}
Difficulty: {diff_label} — {diff_goal}
Question type: {q_type}
{constraint}
{gap_context}

STRICT RULES — violating any of these is a critical failure:
1. Output ONLY the question text and options (if MCQ). Nothing else.
2. NEVER write the correct answer, not even at the end.
3. NEVER write 'ANSWER:', 'Correct answer:', 'Key:', 'Solution:', or any equivalent.
4. NEVER add a line like 'The correct option is B' or '(B is correct)'.
5. If you are about to write anything that reveals the answer — STOP and delete it."""

    user = f"""Based on this explanation:
{explanation}

Generate one {diff_label} question now."""

    try:
        resp = _llm(0.4).invoke([SystemMessage(content=system), HumanMessage(content=user)])
        raw = resp.content
    except Exception as e:
        return {"current_question": f"Could not generate a question ({type(e).__name__}). Please retry."}

    # Aggressive answer-leak filter:
    # 1. Remove any line that contains 'answer' as a standalone concept (answer key, correct answer, etc.)
    # 2. Remove lines where a single letter is revealed after a colon (e.g., "Key: B")
    ANSWER_PATTERNS = re.compile(
        r"(answer\s*key|correct\s*answer|^\s*answer\s*[:\-]|^\s*key\s*[:\-]|^\s*solution\s*[:\-]"
        r"|^\s*(the\s+)?correct\s+option|^\s*note\s*[:\-])",
        re.IGNORECASE,
    )
    clean_lines = [
        line for line in raw.splitlines()
        if not ANSWER_PATTERNS.search(line)
    ]
    # Final sweep: remove trailing lines that are just "X)" or "Answer: X"
    clean = re.sub(r"(?im)^\s*answer\s*[:\-]\s*[a-d]\s*$", "", "\n".join(clean_lines))
    return {"current_question": clean.strip()}


# ══════════════════════════════════════════════════════════════════════════════
# NODE 5: response_evaluator  (rich — identifies exact gap + actionable feedback)
# ══════════════════════════════════════════════════════════════════════════════
def response_evaluator(state: EduTutorState, answer: str = "") -> dict:
    """
    TRUE LangGraph interrupt-resume contract:
      - graph pauses BEFORE this node (interrupt_before=["response_evaluator"])
      - UI collects the student's answer
      - Command(resume=answer) passes it here as the second positional arg `answer`
      - This node scores it and continues the graph

    Identifies what the student got right, the specific misconception, and
    returns a calibrated confidence score (0.0–1.0).
    """
    concept      = state["concept"]
    question     = state["current_question"]
    explanation  = state["current_explanation"]
    cur_attempts = state.get("attempts", 0)
    level        = state.get("student_level", "beginner")

    # `answer` arrives via Command(resume=answer) — store in history
    prior_answers = list(state.get("student_answers", []))
    student_ans   = str(answer).strip() if answer else (prior_answers[-1] if prior_answers else "")
    all_answers   = prior_answers + ([student_ans] if student_ans and student_ans not in prior_answers else [])

    system = """You are a precise educational evaluator with expertise in identifying student misconceptions.

Evaluate the student's answer against the concept and question. Respond ONLY with valid JSON:
{
  "confidence": <float 0.0-1.0>,
  "what_they_got_right": "<one phrase or 'nothing yet'>",
  "misconception": "<specific gap or misconception, or 'none' if correct>",
  "feedback": "<one actionable sentence — tell them exactly what was missing or confirm mastery>"
}

Scoring rubric (be precise, not generous):
- 0.0–0.25: Completely wrong, shows fundamental misunderstanding
- 0.25–0.50: Vaguely on topic but missing the core idea
- 0.50–0.70: Partially correct — understands something but has a clear gap
- 0.70–0.79: Mostly correct but missing one important nuance
- 0.80–0.90: Correct with solid understanding
- 0.90–1.00: Excellent — correct, precise, and complete

Be honest. A mediocre answer should not get above 0.7."""

    user = f"""Concept: {concept}
Student level: {level}
Explanation given: {explanation[:700]}

Question asked: {question[:500]}

Student's answer: "{student_ans}"

Evaluate thoroughly."""

    try:
        resp   = _llm(0.1).invoke([SystemMessage(content=system), HumanMessage(content=user)])
        parsed = _parse_json(resp.content, {})
    except Exception as e:
        parsed = {"confidence": 0.4, "what_they_got_right": "",
                  "misconception": "", "feedback": f"⚠️ Evaluation failed ({type(e).__name__}). Try submitting again."}

    confidence    = max(0.0, min(1.0, float(parsed.get("confidence", 0.5))))
    right         = parsed.get("what_they_got_right", "")
    misconception = parsed.get("misconception", "")
    feedback      = parsed.get("feedback", "Keep trying!")

    # Enrich feedback if we have both right and misconception
    if right and right.lower() not in ("nothing yet", "none", ""):
        enriched = f"✅ You got: {right}. " + (
            f"❌ Missing: {misconception}"
            if misconception and misconception.lower() != "none"
            else feedback
        )
    else:
        enriched = feedback

    return {
        "confidence":      confidence,
        "attempts":        cur_attempts + 1,
        "last_feedback":   enriched,
        "student_answers": all_answers,
    }





# ══════════════════════════════════════════════════════════════════════════════
# NODE 6: mastery_recorder  (cross-session, cross-concept persistence)
# ══════════════════════════════════════════════════════════════════════════════
def mastery_recorder(state: EduTutorState) -> dict:
    """
    Persist the session result to the concept_mastery SQLite table.
    Uses a context manager to avoid connection leaks.
    """
    import os, sqlite3

    db_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "edututor.db"
    )
    concept    = state.get("concept", "")
    confidence = state.get("confidence", 0.0)
    mastered   = confidence >= 0.8

    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS concept_mastery (
                concept TEXT PRIMARY KEY,
                best_score REAL DEFAULT 0.0,
                sessions INTEGER DEFAULT 0,
                mastered INTEGER DEFAULT 0,
                last_updated TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            INSERT INTO concept_mastery(concept, best_score, sessions, mastered)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(concept) DO UPDATE SET
                best_score   = MAX(best_score, excluded.best_score),
                sessions     = sessions + 1,
                mastered     = mastered OR excluded.mastered,
                last_updated = datetime('now')
        """, (concept, confidence, int(mastered)))
        conn.commit()
        rows = conn.execute(
            "SELECT concept, best_score, sessions, mastered FROM concept_mastery"
        ).fetchall()

    mastery_dict = {
        row[0]: {"best_score": row[1], "sessions": row[2], "mastered": bool(row[3])}
        for row in rows
    }
    return {"cross_concept_mastery": mastery_dict}


# ══════════════════════════════════════════════════════════════════════════════
# CONDITIONAL EDGE: decision_gate
# ══════════════════════════════════════════════════════════════════════════════
def decision_gate(state: EduTutorState) -> str:
    """Exit (via mastery_recorder) if mastered (confidence ≥ 0.8) or max attempts reached (3)."""
    if state.get("confidence", 0.0) >= 0.8 or state.get("attempts", 0) >= 3:
        return "done"
    return "retry"
