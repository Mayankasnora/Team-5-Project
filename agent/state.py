"""
EduTutor State — Pydantic BaseModel (Fix 1: replaces TypedDict for rubric compliance).
All fields have defaults so LangGraph can partially update state without KeyErrors.
"""
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class EduTutorState(BaseModel):
    # ── Core session fields ──────────────────────────────────────────────────
    concept:               str                                      = ""
    student_level:         Literal["beginner","intermediate","advanced"] = "beginner"
    concept_text:          str                                      = ""

    # ── Strategy tracking ────────────────────────────────────────────────────
    strategies_used:       List[str]                                = Field(default_factory=list)
    current_strategy:      str                                      = ""
    strategy_change_reason: str                                     = ""  # "Why did strategy change?" callout

    # ── Explanation & question ───────────────────────────────────────────────
    current_explanation:   str                                      = ""
    current_question:      str                                      = ""

    # ── Evaluation & feedback ────────────────────────────────────────────────
    student_answers:       List[str]                                = Field(default_factory=list)
    confidence:            float                                    = 0.0
    attempts:              int                                      = 0
    last_feedback:         str                                      = ""

    # ── Decision routing ─────────────────────────────────────────────────────
    decision_reason:       str                                      = ""  # logged by decision_gate

    # ── Cross-concept mastery (persisted via SQLite) ─────────────────────────
    cross_concept_mastery: Optional[Dict]                           = None
