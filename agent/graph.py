import os
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

from langgraph.graph import StateGraph, END
from .state import EduTutorState
from .nodes import (
    topic_loader,
    strategy_selector,
    explainer,
    question_generator,
    response_evaluator,
    mastery_recorder,
    decision_gate,
)


def build_graph(checkpointer=None):
    """
    Build and compile the EduTutor LangGraph (Reflection Loop pattern).

    Flow:
        topic_loader → strategy_selector → explainer → question_generator
                                ↑                               ↓
                          (retry edge)              [INTERRUPT before response_evaluator]
                                |                               ↓
                                └──── decision_gate ←── response_evaluator
                                           |
                                      (done edge)
                                           ↓
                                   mastery_recorder → END

    Exit conditions:  confidence >= 0.8  OR  attempts >= 3
    """
    builder = StateGraph(EduTutorState)

    builder.add_node("topic_loader",       topic_loader)
    builder.add_node("strategy_selector",  strategy_selector)
    builder.add_node("explainer",          explainer)
    builder.add_node("question_generator", question_generator)
    builder.add_node("response_evaluator", response_evaluator)
    builder.add_node("mastery_recorder",   mastery_recorder)

    builder.set_entry_point("topic_loader")
    builder.add_edge("topic_loader",       "strategy_selector")
    builder.add_edge("strategy_selector",  "explainer")
    builder.add_edge("explainer",          "question_generator")
    builder.add_edge("question_generator", "response_evaluator")
    builder.add_edge("mastery_recorder",   END)

    builder.add_conditional_edges(
        "response_evaluator",
        decision_gate,
        {"retry": "strategy_selector", "done": "mastery_recorder"},
    )

    # ── Checkpointer (SqliteSaver for persistent, traceable history) ──
    if checkpointer is not None:
        cp = checkpointer
    else:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "edututor.db")
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cp = SqliteSaver(conn)

    graph = builder.compile(
        checkpointer=cp,
        interrupt_before=["response_evaluator"],
    )
    return graph
