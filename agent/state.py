from typing import TypedDict, Literal, Optional


class EduTutorState(TypedDict):
    concept: str
    student_level: Literal['beginner', 'intermediate', 'advanced']
    concept_text: str
    strategies_used: list
    current_strategy: str
    current_explanation: str
    current_question: str
    student_answers: list
    confidence: float
    attempts: int
    last_feedback: str
    strategy_change_reason: str  # "Why did strategy change?" callout text
    # Cross-concept mastery tracking (persisted to SQLite across sessions)
    cross_concept_mastery: Optional[dict]  # {concept: {"best_score": float, "sessions": int, "mastered": bool}}
