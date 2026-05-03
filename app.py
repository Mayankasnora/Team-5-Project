"""
EduTutor — Adaptive AI Tutor with Comprehension Retry
LangGraph Reflection Loop | Problem 5 | UGDSAI 29
"""
import uuid, os, sqlite3, streamlit as st
from dotenv import load_dotenv
from langgraph.types import Command
load_dotenv()

st.set_page_config(page_title="EduTutor — Adaptive AI Tutor", page_icon="🎓",
                   layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════
# PREMIUM CSS
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');

*{font-family:'Inter',sans-serif!important;box-sizing:border-box;}
code,pre{font-family:'JetBrains Mono',monospace!important;}

/* ── Base ── */
.stApp{background:radial-gradient(ellipse at 10% 0%,#1b0a3a 0%,#0a0a1f 45%,#001428 100%)!important;min-height:100vh;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:1.5rem 2.5rem 4rem!important;max-width:1280px!important;}

/* ── FORCE SIDEBAR ALWAYS VISIBLE ── */
section[data-testid="stSidebar"]{
  display:flex!important;
  visibility:visible!important;
  opacity:1!important;
  width:21rem!important;
  min-width:21rem!important;
  max-width:21rem!important;
  transform:none!important;
  position:relative!important;
  left:0!important;
}
section[data-testid="stSidebarCollapsedControl"]{display:none!important;}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,rgba(18,8,36,0.98) 0%,rgba(0,12,32,0.98) 100%)!important;
  border-right:1px solid rgba(139,92,246,0.15)!important;
}
section[data-testid="stSidebar"] .block-container{padding:1.5rem 1.2rem!important;}

/* ── Inputs ── */
div[data-testid="stSelectbox"]>div>div{
  background:rgba(255,255,255,0.05)!important;
  border:1px solid rgba(139,92,246,0.3)!important;border-radius:10px!important;color:white!important;
}
div[data-testid="stRadio"] label{color:rgba(255,255,255,0.75)!important;}
div[data-testid="stTextArea"] textarea{
  background:rgba(255,255,255,0.04)!important;
  border:1px solid rgba(139,92,246,0.3)!important;border-radius:12px!important;
  color:rgba(255,255,255,0.92)!important;font-size:0.95rem!important;padding:14px!important;
  transition:border-color .2s,box-shadow .2s;
}
div[data-testid="stTextArea"] textarea:focus{
  border-color:rgba(139,92,246,0.75)!important;
  box-shadow:0 0 0 3px rgba(139,92,246,0.12)!important;
}

/* ── Buttons ── */
.stButton>button{
  background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;color:white!important;
  border:none!important;border-radius:12px!important;font-weight:700!important;
  font-size:0.9rem!important;padding:0.65rem 1.4rem!important;
  transition:all .25s ease!important;box-shadow:0 4px 20px rgba(124,58,237,0.35)!important;
  letter-spacing:0.3px!important;
}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 32px rgba(124,58,237,0.55)!important;}
.stButton>button[kind="secondary"]{
  background:rgba(255,255,255,0.06)!important;box-shadow:none!important;
  border:1px solid rgba(255,255,255,0.12)!important;
}
.stButton>button[kind="secondary"]:hover{background:rgba(255,255,255,0.1)!important;box-shadow:none!important;transform:none!important;}
div[data-testid="stFormSubmitButton"]>button{
  background:linear-gradient(135deg,#059669,#0d9488)!important;
  box-shadow:0 4px 20px rgba(5,150,105,0.4)!important;
  width:100%!important;padding:0.8rem!important;font-size:1rem!important;
}
div[data-testid="stFormSubmitButton"]>button:hover{box-shadow:0 8px 30px rgba(5,150,105,0.6)!important;}

/* ── Progress ── */
div[data-testid="stProgress"]>div{border-radius:99px!important;}
div[data-testid="stProgress"]>div>div{
  background:linear-gradient(90deg,#7c3aed,#06b6d4)!important;border-radius:99px!important;
}

hr{border-color:rgba(255,255,255,0.07)!important;}

/* ── Fade-in animation ── */
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

/* ── Tabs ── */
div[data-testid="stTabs"] button[role="tab"]{
  color:rgba(255,255,255,.45)!important;font-weight:700!important;font-size:.82rem!important;
  letter-spacing:.3px!important;border-radius:8px 8px 0 0!important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{
  color:#a78bfa!important;border-bottom:2px solid #a78bfa!important;
}
div[data-testid="stTabs"]>div>div>div>div{
  background:rgba(255,255,255,.02)!important;
  border:1px solid rgba(255,255,255,.07)!important;border-radius:0 12px 12px 12px!important;
  padding:16px!important;
}

/* ── Code blocks ── */
div[data-testid="stCode"] pre{
  background:rgba(0,0,0,.4)!important;border:1px solid rgba(255,255,255,.07)!important;
  border-radius:12px!important;font-size:.82rem!important;
}



/* ── Sidebar toggle arrow (make it visible on dark bg) ── */
button[data-testid="collapsedControl"],
button[data-testid="baseButton-headerNoPadding"]{
  background:rgba(139,92,246,0.25)!important;
  border:1px solid rgba(139,92,246,0.5)!important;
  border-radius:8px!important;
  color:white!important;
}
section[data-testid="stSidebarCollapsedControl"]{
  background:rgba(18,8,36,0.9)!important;
  border-right:1px solid rgba(139,92,246,0.2)!important;
}
section[data-testid="stSidebarCollapsedControl"] button{
  background:rgba(139,92,246,0.3)!important;
  border:1px solid rgba(139,92,246,0.55)!important;
  border-radius:8px!important;color:#c4b5fd!important;
}
section[data-testid="stSidebarCollapsedControl"] button:hover{
  background:rgba(139,92,246,0.55)!important;
}


/* ── GRAD TEXT ── */
.grad-text{
  background:linear-gradient(135deg,#a78bfa 0%,#60a5fa 50%,#34d399 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.grad-text-2{
  background:linear-gradient(135deg,#f9a8d4,#c084fc,#818cf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}

/* ── CARDS ── */
.glass{
  background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
  border-radius:20px;padding:26px 30px;margin:14px 0;
  backdrop-filter:blur(14px);transition:border-color .3s,box-shadow .3s;
}
.glass:hover{border-color:rgba(139,92,246,0.22);box-shadow:0 8px 40px rgba(124,58,237,0.07);}

.glow-purple{
  background:linear-gradient(135deg,rgba(124,58,237,0.1),rgba(79,70,229,0.07));
  border:1px solid rgba(124,58,237,0.28);border-radius:20px;padding:26px 30px;margin:14px 0;
  box-shadow:0 0 50px rgba(124,58,237,0.06);
}
.glow-cyan{
  background:linear-gradient(135deg,rgba(6,182,212,0.08),rgba(59,130,246,0.06));
  border:1px solid rgba(6,182,212,0.22);border-radius:20px;padding:26px 30px;margin:14px 0;
}
.glow-green{
  background:linear-gradient(135deg,rgba(5,150,105,0.1),rgba(6,182,212,0.07));
  border:1px solid rgba(5,150,105,0.28);border-radius:20px;padding:26px 30px;margin:14px 0;
}

/* ── HERO ── */
.hero{
  background:linear-gradient(135deg,rgba(124,58,237,0.18),rgba(79,70,229,0.12),rgba(6,182,212,0.1));
  border:1px solid rgba(139,92,246,0.22);border-radius:28px;
  padding:52px 48px;text-align:center;margin-bottom:10px;
  position:relative;overflow:hidden;
}
.hero::before{
  content:'';position:absolute;top:-80px;right:-80px;
  width:280px;height:280px;
  background:radial-gradient(circle,rgba(139,92,246,0.18),transparent 70%);
  border-radius:50%;pointer-events:none;
}
.hero::after{
  content:'';position:absolute;bottom:-60px;left:-60px;
  width:220px;height:220px;
  background:radial-gradient(circle,rgba(6,182,212,0.12),transparent 70%);
  border-radius:50%;pointer-events:none;
}
.hero h1{font-size:3.2rem;font-weight:900;letter-spacing:-1.5px;margin:0 0 12px;line-height:1.1;}
.hero .tagline{font-size:1.05rem;color:rgba(255,255,255,0.55);margin:0 0 28px;max-width:560px;margin-left:auto;margin-right:auto;}

/* ── STATS BAR ── */
.stats-bar{
  display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
  background:rgba(255,255,255,0.06);border-radius:16px;overflow:hidden;margin:20px 0;
}
.stat-cell{
  background:rgba(255,255,255,0.025);padding:18px 20px;text-align:center;
}
.stat-num{font-size:1.6rem;font-weight:900;color:#a78bfa;line-height:1;}
.stat-lbl{font-size:.7rem;color:rgba(255,255,255,.35);font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-top:4px;}

/* ── CONCEPT CARDS ── */
.concept-card{
  background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
  border-radius:18px;padding:26px 20px;text-align:center;
  transition:all .3s ease;cursor:pointer;height:100%;position:relative;overflow:hidden;
}
.concept-card::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(124,58,237,0.06),transparent);
  opacity:0;transition:opacity .3s;
}
.concept-card:hover{border-color:rgba(139,92,246,0.4);transform:translateY(-5px);
  box-shadow:0 16px 50px rgba(124,58,237,0.18);}
.concept-card:hover::before{opacity:1;}
.c-icon{font-size:2.8rem;margin-bottom:12px;}
.c-title{font-size:1rem;font-weight:800;color:#a78bfa;margin-bottom:6px;}
.c-desc{font-size:.82rem;color:rgba(255,255,255,.5);line-height:1.65;}
.c-tag{
  display:inline-block;margin-top:12px;padding:3px 10px;border-radius:99px;
  font-size:.7rem;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
  background:rgba(124,58,237,.2);border:1px solid rgba(124,58,237,.35);color:#c4b5fd;
}

/* ── STRATEGY GALLERY ── */
.strat-gallery{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:16px 0;}
.strat-tile{
  border-radius:16px;padding:18px 12px;text-align:center;
  transition:transform .25s,box-shadow .25s;cursor:default;
}
.strat-tile:hover{transform:translateY(-4px);}
.s-analogy   {background:rgba(124,58,237,.15);border:1px solid rgba(124,58,237,.35);}
.s-example   {background:rgba(37,99,235,.15); border:1px solid rgba(37,99,235,.35);}
.s-step      {background:rgba(5,150,105,.15); border:1px solid rgba(5,150,105,.35);}
.s-visual    {background:rgba(217,119,6,.15); border:1px solid rgba(217,119,6,.35);}
.s-socratic  {background:rgba(220,38,38,.15); border:1px solid rgba(220,38,38,.35);}
.strat-tile .s-emoji{font-size:1.8rem;margin-bottom:8px;}
.strat-tile .s-name{font-size:.75rem;font-weight:800;letter-spacing:.5px;text-transform:uppercase;}
.s-analogy  .s-name{color:#c4b5fd;}
.s-example  .s-name{color:#93c5fd;}
.s-step     .s-name{color:#6ee7b7;}
.s-visual   .s-name{color:#fcd34d;}
.s-socratic .s-name{color:#fca5a5;}
.strat-tile .s-desc{font-size:.72rem;color:rgba(255,255,255,.45);line-height:1.5;margin-top:6px;}

/* ── PILLS ── */
.pill{display:inline-flex;align-items:center;gap:5px;padding:4px 12px;border-radius:99px;
  font-size:11px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;}
.p-analogy   {background:rgba(124,58,237,.25);border:1px solid rgba(124,58,237,.55);color:#c4b5fd;}
.p-example   {background:rgba(37,99,235,.25); border:1px solid rgba(37,99,235,.55); color:#93c5fd;}
.p-step_by_step{background:rgba(5,150,105,.25);border:1px solid rgba(5,150,105,.55);color:#6ee7b7;}
.p-visual    {background:rgba(217,119,6,.25); border:1px solid rgba(217,119,6,.55); color:#fcd34d;}
.p-socratic  {background:rgba(220,38,38,.25); border:1px solid rgba(220,38,38,.55); color:#fca5a5;}

/* ── ATTEMPT CHIP ── */
.attempt-chip{
  display:inline-flex;align-items:center;gap:10px;
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
  border-radius:99px;padding:7px 20px;font-size:13px;font-weight:600;
  color:rgba(255,255,255,.72);margin-bottom:18px;
}

/* ── STEPPER ── */
.stepper{display:flex;align-items:center;gap:0;margin-bottom:28px;}
.step-node{
  width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:.8rem;font-weight:800;flex-shrink:0;
}
.step-active{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:white;box-shadow:0 0 16px rgba(124,58,237,.5);}
.step-done  {background:rgba(5,150,105,.3);border:1px solid #059669;color:#6ee7b7;}
.step-todo  {background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:rgba(255,255,255,.3);}
.step-line  {flex:1;height:2px;background:rgba(255,255,255,.08);}
.step-line-done{background:linear-gradient(90deg,#7c3aed,#059669);}
.step-label{font-size:.65rem;color:rgba(255,255,255,.4);text-align:center;margin-top:5px;font-weight:600;letter-spacing:.3px;}

/* ── CONF BOX ── */
.conf-box{border-radius:16px;padding:18px 22px;display:flex;align-items:center;gap:18px;}
.conf-green{background:rgba(5,150,105,.12);border:1px solid rgba(5,150,105,.3);}
.conf-yellow{background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.3);}
.conf-red{background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.3);}
.conf-num{font-size:2.5rem;font-weight:900;line-height:1;}
.conf-green .conf-num{color:#34d399;}
.conf-yellow .conf-num{color:#fbbf24;}
.conf-red   .conf-num{color:#f87171;}

/* ── SECTION LABEL ── */
.sec-lbl{font-size:.68rem;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;
  color:rgba(255,255,255,.3);margin-bottom:10px;}

/* ── SIDEBAR rows ── */
.sb-row{background:rgba(255,255,255,.04);border-radius:10px;padding:10px 14px;margin:5px 0;
  display:flex;justify-content:space-between;align-items:center;}
.sb-k{font-size:.75rem;color:rgba(255,255,255,.38);font-weight:500;}
.sb-v{font-size:.83rem;color:rgba(255,255,255,.85);font-weight:700;}

/* ── MASTERY BADGE ── */
.mastery-badge{display:flex;align-items:center;gap:10px;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);
  border-radius:12px;padding:10px 14px;margin:5px 0;}

/* ── SUMMARY TABLE ── */
.sum-hdr,.sum-row-g{display:grid;grid-template-columns:36px 1fr 1.8fr 70px;
  gap:10px;align-items:center;padding:9px 14px;}
.sum-hdr{font-size:.68rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,.28);}
.sum-row-g{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);
  border-radius:12px;margin-bottom:7px;}

/* ── HOW STEPS ── */
.how-step{display:flex;align-items:flex-start;gap:14px;padding:10px 0;
  border-bottom:1px solid rgba(255,255,255,.05);}
.step-circle{width:28px;height:28px;border-radius:50%;flex-shrink:0;
  background:linear-gradient(135deg,#7c3aed,#4f46e5);
  display:flex;align-items:center;justify-content:center;
  font-size:.78rem;font-weight:800;color:white;}
.step-txt{font-size:.88rem;color:rgba(255,255,255,.6);line-height:1.65;padding-top:4px;}

/* ── FEATURE ICONS ── */
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:16px 0;}
.feat-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
  border-radius:16px;padding:22px 18px;transition:all .25s;}
.feat-card:hover{border-color:rgba(139,92,246,.3);transform:translateY(-3px);}
.feat-icon{font-size:1.6rem;margin-bottom:10px;}
.feat-title{font-size:.88rem;font-weight:700;color:rgba(255,255,255,.85);margin-bottom:5px;}
.feat-desc{font-size:.78rem;color:rgba(255,255,255,.42);line-height:1.6;}

/* ── STRAT POOL dots ── */
.pool-wrap{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;align-items:center;}

/* ── Sidebar hidden state ── */
.sidebar-hidden section[data-testid="stSidebar"]{display:none!important;}
.sidebar-hidden section[data-testid="stSidebarCollapsedControl"]{display:none!important;}
</style>
""", unsafe_allow_html=True)



# ═══════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════
CONCEPTS = [
    "Recursion","Bayes Theorem","Binary Search Tree",
    "Dynamic Programming","Neural Networks","Big O Notation",
]
LEVELS = ["beginner","intermediate","advanced"]

CONCEPT_META = {
    "Recursion":            ("🔁","CS Algorithm","Functions that call themselves to conquer sub-problems."),
    "Bayes Theorem":        ("📊","Probability","Update beliefs when new evidence arrives."),
    "Binary Search Tree":   ("🌳","Data Structure","Ordered tree enabling O(log n) search."),
    "Dynamic Programming":  ("🧩","Optimization","Solve complex problems by caching sub-solutions."),
    "Neural Networks":      ("🧠","AI/ML","Layered neurons inspired by the human brain."),
    "Big O Notation":       ("⏱️","Complexity","Measure algorithm efficiency as input scales."),
}

STRAT_TILES = [
    ("analogy",   "🔗","Analogy",   "s-analogy", "Relate to real life"),
    ("example",   "📝","Example",   "s-example", "Worked examples"),
    ("step_by_step","📋","Step-by-Step","s-step","Sequential guide"),
    ("visual",    "🎨","Visual",    "s-visual",  "Diagrams & maps"),
    ("socratic",  "💭","Socratic",  "s-socratic","Guided questions"),
]

EMOJI = {"analogy":"🔗","example":"📝","step_by_step":"📋","visual":"🎨","socratic":"💭"}

# ═══════════════════════════════════════════════════════
# SESSION INIT
# ═══════════════════════════════════════════════════════
def _init():
    for k,v in {"phase":"setup","thread_id":None,"config":None,
                "current_gs":None,"attempt_log":[],"session_mastery":[]}.items():
        if k not in st.session_state: st.session_state[k]=v
_init()

@st.cache_resource(show_spinner=False)
def get_graph():
    """Cached graph — SqliteSaver checkpoint for persistent, traceable sessions."""
    from agent.graph import build_graph
    return build_graph()


def load_cross_mastery() -> dict:
    """Read the concept_mastery table from SQLite — survives restarts."""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "edututor.db")
    if not os.path.exists(db_path):
        return {}
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        rows = conn.execute(
            "SELECT concept, best_score, sessions, mastered FROM concept_mastery"
        ).fetchall()
        conn.close()
        return {
            r[0]: {"best_score": r[1], "sessions": r[2], "mastered": bool(r[3])}
            for r in rows
        }
    except Exception:
        return {}


# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════
def pill(s):
    return f'<span class="pill p-{s}">{EMOJI.get(s,"⚡")} {s.replace("_"," ").title()}</span>'

def conf_cls(c): return "conf-green" if c>=0.8 else "conf-yellow" if c>=0.5 else "conf-red"
def conf_clr(c): return "#34d399" if c>=0.8 else "#fbbf24" if c>=0.5 else "#f87171"

def start_session(concept, level):
    g = get_graph()
    tid = str(uuid.uuid4())
    cfg = {"configurable": {"thread_id": tid}}
    init = {
        "concept": concept, "student_level": level, "concept_text": "",
        "strategies_used": [], "current_strategy": "", "current_explanation": "",
        "current_question": "", "student_answers": [], "confidence": 0.0,
        "attempts": 0, "last_feedback": "",
    }
    try:
        with st.spinner("🧠  Fetching concept · Selecting strategy · Crafting explanation…"):
            # TRUE INTERRUPT-RESUME FLOW (LangGraph pattern):
            # invoke() runs: topic_loader → strategy_selector → explainer → question_generator
            # then PAUSES before response_evaluator (interrupt_before=["response_evaluator"]).
            # The UI collects the student answer; submit_answer() injects it via
            # update_state() then resumes the graph with invoke(None, config=cfg).
            g.invoke(init, config=cfg)
        snap = g.get_state(cfg)
        st.session_state.update(
            thread_id=tid, config=cfg,
            current_gs=snap.values, attempt_log=[], phase="explaining"
        )
    except Exception as e:
        st.error(f"❌ Failed to start session: {e}. Check your GITHUB_TOKEN and try again.")

def submit_answer(answer):
    """
    TRUE LangGraph interrupt-resume cycle:
      1. graph was paused at interrupt_before=["response_evaluator"]
      2. Student types answer in the UI
      3. Command(resume=answer) injects the answer and resumes execution
         — response_evaluator runs → decision_gate → retry OR mastery_recorder → END
    """
    g = get_graph()
    cfg = st.session_state.config
    gs  = st.session_state.current_gs

    pre = {
        "attempt_num": gs.get("attempts", 0) + 1,
        "strategy":    gs.get("current_strategy", ""),
        "explanation": gs.get("current_explanation", ""),
        "question":    gs.get("current_question", ""),
        "answer":      answer,
    }

    # ── TRUE RESUME: inject answer as the resume value ──────────────────────
    # The graph paused before response_evaluator; Command(resume=answer)
    # passes the student's answer to that node and continues the graph.
    with st.spinner("⚙️  Scoring your answer…"):
        g.invoke(Command(resume=answer), config=cfg)

    snap = g.get_state(cfg)
    ngs  = snap.values
    pre["confidence"] = ngs.get("confidence", 0.0)
    pre["feedback"]   = ngs.get("last_feedback", "")
    st.session_state.attempt_log.append(pre)

    if not snap.next:  # graph reached END
        st.session_state.update(current_gs=ngs, phase="finished")
        st.session_state.session_mastery.append({
            "concept":    ngs.get("concept", ""),
            "confidence": ngs.get("confidence", 0.0),
            "attempts":   ngs.get("attempts", 0),
        })
    else:  # still looping (retry branch)
        st.session_state.current_gs = ngs
    st.rerun()

def reset():
    st.session_state.update(phase="setup",thread_id=None,config=None,current_gs=None,attempt_log=[])
    st.rerun()

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:14px 0 22px">
  <div style="font-size:2.4rem;filter:drop-shadow(0 0 14px rgba(167,139,250,.6))">🎓</div>
  <div style="font-size:1.3rem;font-weight:900;background:linear-gradient(135deg,#a78bfa,#60a5fa);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-top:4px">EduTutor</div>
  <div style="font-size:.7rem;color:rgba(255,255,255,.28);letter-spacing:1px;text-transform:uppercase;margin-top:2px">Adaptive AI Tutor</div>
</div>""", unsafe_allow_html=True)


    st.markdown('<div class="sec-lbl">Session</div>', unsafe_allow_html=True)

    if st.session_state.phase == "setup":
        concept = st.selectbox("📚 Concept", CONCEPTS, key="sel_concept")
        custom  = st.text_input("✏️ Or type any concept",
                                placeholder="e.g. Gradient Descent, Hash Tables…",
                                key="custom_concept")
        level   = st.radio("🎯 Level", LEVELS, key="sel_level")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀  Start Learning", use_container_width=True, type="primary"):
            final_concept = custom.strip() if custom.strip() else concept
            start_session(final_concept, level); st.rerun()
    else:
        gs = st.session_state.current_gs or {}
        icon = CONCEPT_META.get(gs.get("concept",""), ("📚","",""))[0]
        st.markdown(f"""
<div class="sb-row"><span class="sb-k">Concept</span><span class="sb-v">{icon} {gs.get("concept","")}</span></div>
<div class="sb-row"><span class="sb-k">Level</span><span class="sb-v">{gs.get("student_level","").title()}</span></div>
<div class="sb-row"><span class="sb-k">Attempts</span><span class="sb-v">{gs.get("attempts",0)} / 3</span></div>
""", unsafe_allow_html=True)
        used=gs.get("strategies_used",[])
        if used:
            st.markdown('<div class="sec-lbl" style="margin-top:14px">Strategies tried</div>', unsafe_allow_html=True)
            st.markdown('<div style="display:flex;flex-wrap:wrap;gap:6px">'+"".join(pill(s) for s in used)+"</div>", unsafe_allow_html=True)
        if st.session_state.phase!="finished" and gs.get("attempts",0)>0:
            c=gs.get("confidence",0.0)
            st.markdown('<div class="sec-lbl" style="margin-top:14px">Confidence</div>', unsafe_allow_html=True)
            st.progress(c)
            st.markdown(f'<div style="text-align:center;font-size:.82rem;color:{conf_clr(c)};font-weight:800">{int(c*100)}%</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            if st.button("🔄 New",use_container_width=True,type="secondary"): reset()
        with c2:
            if st.button("🔁 Retry", use_container_width=True, type="secondary"):
                cname = gs.get("concept", "Recursion"); lv = gs.get("student_level", "beginner")
                st.session_state.update(phase="setup", thread_id=None, config=None, current_gs=None, attempt_log=[])
                start_session(cname, lv)
                st.rerun()

    if st.session_state.session_mastery:
        st.markdown("---")
        st.markdown('<div class="sec-lbl">🏆 Mastery Board</div>', unsafe_allow_html=True)
        for m in st.session_state.session_mastery:
            pct=int(m["confidence"]*100); icon="✅" if m["confidence"]>=0.8 else "⚠️"
            st.markdown(f"""
<div class="mastery-badge">
  <span style="font-size:1.1rem">{icon}</span>
  <div>
    <div style="font-size:.82rem;font-weight:700;color:rgba(255,255,255,.85)">{m["concept"]}</div>
    <div style="font-size:.73rem;color:{conf_clr(m["confidence"])};font-weight:700">{pct}% · {m["attempts"]} attempt(s)</div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:.68rem;color:rgba(255,255,255,.18);text-align:center;line-height:1.8">UGDSAI 29 · Problem 5<br>LangGraph Reflection Loop</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div style="display:inline-block;background:rgba(124,58,237,.2);border:1px solid rgba(139,92,246,.35);
    border-radius:99px;padding:5px 16px;font-size:.72rem;font-weight:800;letter-spacing:1px;
    text-transform:uppercase;color:#c4b5fd;margin-bottom:18px">
    🧠 LangGraph Reflection Loop · Ed-tech · Problem 5
  </div>
  <h1><span class="grad-text">EduTutor</span></h1>
  <p class="tagline">An adaptive AI tutor that teaches, checks your understanding, and re-teaches using a completely different strategy until you truly get it.</p>
  <div style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap">
    <span style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
      border-radius:99px;padding:6px 18px;font-size:.82rem;color:rgba(255,255,255,.65)">
      🔁 Reflection Loop
    </span>
    <span style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
      border-radius:99px;padding:6px 18px;font-size:.82rem;color:rgba(255,255,255,.65)">
      🌐 Wikipedia Data
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# STATS BAR — live counts from SQLite
# ═══════════════════════════════════════════════════════
_cm = load_cross_mastery()
_total_sessions = sum(v["sessions"] for v in _cm.values()) if _cm else 0
_mastered_count = sum(1 for v in _cm.values() if v["mastered"]) if _cm else 0
st.markdown(f"""
<div class="stats-bar">
  <div class="stat-cell"><div class="stat-num">6</div><div class="stat-lbl">Concepts</div></div>
  <div class="stat-cell"><div class="stat-num">5</div><div class="stat-lbl">Strategies</div></div>
  <div class="stat-cell"><div class="stat-num">{_mastered_count}</div><div class="stat-lbl">Mastered</div></div>
  <div class="stat-cell"><div class="stat-num">{_total_sessions}</div><div class="stat-lbl">Sessions</div></div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PHASE: SETUP
# ═══════════════════════════════════════════════════════
if st.session_state.phase == "setup":

    # Concept cards
    st.markdown('<div class="sec-lbl" style="margin-top:24px">📚 Choose a Concept — click to start</div>', unsafe_allow_html=True)
    rows = [CONCEPTS[:3], CONCEPTS[3:]]
    for row in rows:
        cols = st.columns(3)
        for col, c in zip(cols, row):
            icon, tag, desc = CONCEPT_META[c]
            with col:
                st.markdown(f"""
<div class="concept-card">
  <div class="c-icon">{icon}</div>
  <div class="c-title">{c}</div>
  <div class="c-desc">{desc}</div>
  <div class="c-tag">{tag}</div>
</div>""", unsafe_allow_html=True)
                level_sel = st.session_state.get("sel_level", "beginner")
                if st.button(f"🚀 Start Learning", key=f"card_btn_{c}", use_container_width=True, type="primary"):
                    start_session(c, level_sel)
                    st.rerun()
        st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        # Strategy gallery
        st.markdown('<div class="sec-lbl">🎭 Explanation Strategies</div>', unsafe_allow_html=True)
        st.markdown('<div class="strat-gallery">', unsafe_allow_html=True)
        for _,emoji,name,cls,desc in STRAT_TILES:
            st.markdown(f"""
<div class="strat-tile {cls}">
  <div class="s-emoji">{emoji}</div>
  <div class="s-name">{name}</div>
  <div class="s-desc">{desc}</div>
</div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        # Features + How it works
        st.markdown('<div class="sec-lbl">✨ Key Features</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="feat-grid">
  <div class="feat-card">
    <div class="feat-icon">🔄</div>
    <div class="feat-title">Reflection Loop</div>
    <div class="feat-desc">Loops back with a fresh strategy if you struggle</div>
  </div>
  <div class="feat-card">
    <div class="feat-icon">📐</div>
    <div class="feat-title">Confidence Score</div>
    <div class="feat-desc">LLM scores 0–1. Need ≥ 0.8 to master</div>
  </div>
  <div class="feat-card">
    <div class="feat-icon">🚫</div>
    <div class="feat-title">No Repeats</div>
    <div class="feat-desc">Strategies never repeat in one session</div>
  </div>
  <div class="feat-card">
    <div class="feat-icon">🌐</div>
    <div class="feat-title">Live Data</div>
    <div class="feat-desc">Real definitions from Wikipedia API</div>
  </div>
  <div class="feat-card">
    <div class="feat-icon">🎯</div>
    <div class="feat-title">Adaptive MCQ</div>
    <div class="feat-desc">Questions get harder with each attempt</div>
  </div>
  <div class="feat-card">
    <div class="feat-icon">🏆</div>
    <div class="feat-title">Mastery Board</div>
    <div class="feat-desc">Track which concepts you've mastered</div>
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-lbl" style="margin-top:18px">⚙️ How it works</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="glass" style="padding:18px 22px">
  <div class="how-step">
    <div class="step-circle">1</div>
    <div class="step-txt">Pick a concept + level from the sidebar</div>
  </div>
  <div class="how-step">
    <div class="step-circle">2</div>
    <div class="step-txt">AI fetches real content from <b style="color:#60a5fa">Wikipedia</b> and explains using one of <b style="color:#a78bfa">5 unique strategies</b></div>
  </div>
  <div class="how-step">
    <div class="step-circle">3</div>
    <div class="step-txt">Answer a comprehension question — difficulty escalates each attempt</div>
  </div>
  <div class="how-step">
    <div class="step-circle">4</div>
    <div class="step-txt">LLM scores your answer <b style="color:#f87171">0 → 1</b>. Below 0.8? Agent <b style="color:#a78bfa">loops with a new strategy</b></div>
  </div>
  <div class="how-step" style="border:none">
    <div class="step-circle">5</div>
    <div class="step-txt">Session ends at <b style="color:#34d399">confidence ≥ 80%</b> or after 3 attempts</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Cross-Concept Mastery Leaderboard (reads from SQLite — survives restarts) ──
    st.markdown("<br>", unsafe_allow_html=True)
    cross_mastery = load_cross_mastery()
    if cross_mastery:
        st.markdown('<div class="sec-lbl">🏆 Cross-Concept Mastery — Persistent Progress</div>', unsafe_allow_html=True)
        sorted_concepts = sorted(cross_mastery.items(), key=lambda x: x[1]["best_score"], reverse=True)
        header_html = """
<div style="display:grid;grid-template-columns:28px 1fr 90px 70px 60px;gap:10px;align-items:center;
  padding:7px 14px;font-size:.66rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;
  color:rgba(255,255,255,.28);">
  <div>#</div><div>Concept</div><div>Best Score</div><div>Sessions</div><div>Status</div>
</div>"""
        st.markdown(header_html, unsafe_allow_html=True)
        for rank, (concept, data) in enumerate(sorted_concepts, 1):
            score   = data["best_score"]
            sessions= data["sessions"]
            mastered= data["mastered"]
            score_color = "#34d399" if score >= 0.8 else "#fbbf24" if score >= 0.5 else "#f87171"
            badge   = "🎓 Mastered" if mastered else ("📈 In Progress" if score >= 0.5 else "🔁 Needs Work")
            badge_bg= "rgba(5,150,105,.15)" if mastered else ("rgba(245,158,11,.1)" if score >= 0.5 else "rgba(239,68,68,.1)")
            badge_border = "rgba(5,150,105,.35)" if mastered else ("rgba(245,158,11,.3)" if score >= 0.5 else "rgba(239,68,68,.25)")
            icon    = CONCEPT_META.get(concept, ("📚","",""))[0]
            st.markdown(f"""
<div style="display:grid;grid-template-columns:28px 1fr 90px 70px 60px;gap:10px;align-items:center;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);
  border-radius:12px;padding:10px 14px;margin-bottom:6px;font-size:.84rem;">
  <div style="color:rgba(255,255,255,.25);font-weight:800;font-size:.75rem">{rank}</div>
  <div style="font-weight:700;color:rgba(255,255,255,.85)">{icon} {concept}</div>
  <div style="font-weight:900;color:{score_color}">{int(score*100)}%</div>
  <div style="color:rgba(255,255,255,.45)">{sessions} session{'s' if sessions!=1 else ''}</div>
  <div style="padding:2px 8px;border-radius:99px;font-size:.68rem;font-weight:700;
    background:{badge_bg};border:1px solid {badge_border};color:rgba(255,255,255,.85);white-space:nowrap">{badge}</div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PHASE: EXPLAINING
# ═══════════════════════════════════════════════════════
elif st.session_state.phase == "explaining":
    gs = st.session_state.current_gs or {}
    done     = gs.get("attempts", 0)
    cur_att  = done + 1
    strategy = gs.get("current_strategy","")
    expl     = gs.get("current_explanation","")
    question = gs.get("current_question","")
    concept  = gs.get("concept","")

    # ── Flow stepper ──
    steps = ["Load","Strategy","Explain","Question","Evaluate"]
    active = 3  # currently showing question
    stpr = '<div class="stepper">'
    for i,s in enumerate(steps):
        nd_cls = "step-active" if i==active else "step-done" if i<active else "step-todo"
        lbl = "✓" if i<active else str(i+1)
        line_cls = "step-line-done" if i<active else "step-line"
        stpr += f'<div style="display:flex;flex-direction:column;align-items:center;gap:0">'
        stpr += f'  <div class="step-node {nd_cls}">{lbl}</div>'
        stpr += f'  <div class="step-label">{s}</div>'
        stpr += f'</div>'
        if i<len(steps)-1:
            stpr += f'<div class="step-line {line_cls}" style="margin-bottom:16px"></div>'
    stpr += "</div>"
    st.markdown(stpr, unsafe_allow_html=True)

    # ── Attempt + strategy badge ──
    st.markdown(
        f'<div class="attempt-chip">📍 Attempt {cur_att} of 3 &nbsp;·&nbsp; {pill(strategy)}</div>',
        unsafe_allow_html=True)

    # ── Strategy-change callout + confidence row (after first eval) ──
    if done > 0:
        c = gs.get("confidence", 0.0); fb = gs.get("last_feedback", "")
        change_reason = gs.get("strategy_change_reason", "")
        cls = conf_cls(c)
        used = gs.get("strategies_used", [])
        prev_pill = pill(used[-2]) if len(used) > 1 else ""

        # "Why did strategy change?" — explicit bonus criterion
        if change_reason:
            st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(245,158,11,.1),rgba(124,58,237,.08));
  border:1px solid rgba(245,158,11,.3);border-radius:16px;padding:14px 20px;margin-bottom:16px;
  display:flex;align-items:flex-start;gap:14px">
  <span style="font-size:1.4rem">🔄</span>
  <div>
    <div style="font-size:.68rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;
      color:rgba(245,158,11,.7);margin-bottom:4px">Why did strategy change?</div>
    <div style="font-size:.88rem;color:rgba(255,255,255,.78);line-height:1.6">{change_reason}</div>
    <div style="margin-top:6px;display:flex;align-items:center;gap:6px;font-size:.8rem;color:rgba(255,255,255,.35)">
      {prev_pill} → {pill(strategy)}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown(f"""
<div style="display:grid;grid-template-columns:220px 1fr;gap:14px;margin-bottom:20px">
  <div class="conf-box {cls}">
    <div style="min-width:64px;text-align:center">
      <div style="font-size:.65rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,.35)">Score</div>
      <div class="conf-num">{int(c*100)}%</div>
    </div>
    <div style="font-size:.82rem;color:rgba(255,255,255,.7)">{'Almost there!' if c<0.8 else 'Great!'}</div>
  </div>
  <div class="glass" style="padding:18px 22px;margin:0">
    <div style="font-size:.65rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,.3);margin-bottom:8px">Evaluator Feedback</div>
    <div style="font-size:.92rem;color:rgba(255,255,255,.82);line-height:1.65">{fb}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Explanation ──
    concept_icon = CONCEPT_META.get(concept, ("📖","",""))[0]
    st.markdown(f"""
<div class="glow-purple">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px">
    <div style="display:flex;align-items:center;gap:10px">
      <span style="font-size:1.4rem">{concept_icon}</span>
      <div>
        <div class="sec-lbl" style="margin:0">Explanation</div>
        <div style="font-size:1rem;font-weight:700;color:rgba(255,255,255,.85)">{concept}</div>
      </div>
    </div>
    <div>{pill(strategy)}</div>
  </div>
  <div style="color:rgba(255,255,255,.88);line-height:1.85;font-size:.96rem">
""", unsafe_allow_html=True)
    st.markdown(expl)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Rich Extras Panel ──
    from agent.concept_extras import get_extras
    extra_fig, extra_code, extra_facts, extra_examples = get_extras(concept)

    tab_chart, tab_examples, tab_code, tab_facts = st.tabs([
        "📊 Interactive Chart", "🔢 Worked Examples", "💻 Code Example", "💡 Fun Facts"
    ])

    with tab_chart:
        if extra_fig:
            st.plotly_chart(extra_fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No chart available for this concept yet.")

    with tab_examples:
        if extra_examples:
            st.markdown(extra_examples)
        else:
            st.info("No worked example available.")

    with tab_code:
        if extra_code:
            st.code(extra_code, language="python")
        else:
            st.info("No code example available.")

    with tab_facts:
        if extra_facts:
            cols_f = st.columns(2)
            for i, fact in enumerate(extra_facts):
                with cols_f[i % 2]:
                    st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(124,58,237,.1),rgba(6,182,212,.06));
  border:1px solid rgba(139,92,246,.25);border-radius:16px;padding:18px 20px;margin:6px 0;
  animation:fadeIn .4s ease {i*0.1:.1f}s both">
  <div style="font-size:.92rem;color:rgba(255,255,255,.82);line-height:1.68">{fact}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Question ──
    diff_map = {0: ("Recall", "#a78bfa"), 1: ("Application", "#60a5fa"), 2: ("Analysis", "#34d399")}
    diff_label, diff_color = diff_map[min(done, 2)]
    st.markdown(f"""
<div class="glow-cyan">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
    <span style="font-size:1.3rem">❓</span>
    <div class="sec-lbl" style="margin:0">Comprehension Check</div>
    <div style="margin-left:auto;display:flex;align-items:center;gap:8px">
      <span style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
        border-radius:99px;padding:3px 12px;font-size:.72rem;font-weight:700;color:{diff_color}">
        {diff_label}
      </span>
      <span style="font-size:.75rem;color:rgba(255,255,255,.3)">Attempt {cur_att} · {gs.get('student_level','').title()}</span>
    </div>
  </div>
  <div style="font-size:.98rem;color:rgba(255,255,255,.92);line-height:1.78">{question}</div>
</div>
""", unsafe_allow_html=True)

    with st.form("answer_form", clear_on_submit=True):
        answer = st.text_area("Answer", placeholder="Type your answer here… (1–3 sentences is fine)",
                              height=100, label_visibility="collapsed")
        submitted = st.form_submit_button("✅  Submit Answer", use_container_width=True)

    if submitted:
        if answer and answer.strip():
            submit_answer(answer.strip())
        else:
            st.warning("Please write something before submitting!")

# ═══════════════════════════════════════════════════════
# PHASE: FINISHED
# ═══════════════════════════════════════════════════════
elif st.session_state.phase == "finished":
    gs   = st.session_state.current_gs or {}
    fc   = gs.get("confidence", 0.0)
    ta   = gs.get("attempts",   0)
    conc = gs.get("concept",    "")
    won  = fc >= 0.8
    icon = CONCEPT_META.get(conc, ("📚","",""))[0]

    # ── Banner ──
    if won:
        st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(5,150,105,.15),rgba(6,182,212,.1));
  border:1px solid rgba(5,150,105,.4);border-radius:28px;padding:48px;text-align:center;margin-bottom:28px;
  position:relative;overflow:hidden">
  <div style="position:absolute;top:-50px;right:-50px;width:200px;height:200px;
    background:radial-gradient(circle,rgba(5,150,105,.2),transparent 70%);border-radius:50%"></div>
  <div style="font-size:4rem;margin-bottom:14px">🎉</div>
  <h2 class="grad-text" style="font-size:2.2rem;font-weight:900;margin:0 0 10px;letter-spacing:-.5px">Concept Mastered!</h2>
  <p style="color:rgba(255,255,255,.6);font-size:1rem;margin:0">
    {icon} <strong style="color:#6ee7b7">{conc}</strong> — mastered with
    <strong style="color:#34d399">{int(fc*100)}%</strong> confidence in <strong style="color:#34d399">{ta}</strong> attempt(s)
  </p>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(245,158,11,.12),rgba(239,68,68,.08));
  border:1px solid rgba(245,158,11,.35);border-radius:28px;padding:48px;text-align:center;margin-bottom:28px">
  <div style="font-size:4rem;margin-bottom:14px">📚</div>
  <h2 style="font-size:2rem;font-weight:900;margin:0 0 10px;color:#fbbf24">Keep Practising!</h2>
  <p style="color:rgba(255,255,255,.6);font-size:1rem;margin:0">
    You reached <strong style="color:#fbbf24">{int(fc*100)}%</strong> on {icon} <strong style="color:#fcd34d">{conc}</strong>. Review the explanations and try again!
  </p>
</div>
""", unsafe_allow_html=True)

    # ── Two-column summary ──
    left_col, right_col = st.columns([1.4, 1])

    with left_col:
        st.markdown('<div class="sec-lbl">📋 Attempt Summary</div>', unsafe_allow_html=True)
        st.markdown('<div class="sum-hdr"><div>#</div><div>Strategy</div><div>Feedback</div><div>Score</div></div>', unsafe_allow_html=True)
        for log in st.session_state.attempt_log:
            c  = log.get("confidence",0.0); pct=int(c*100)
            ic = "✅" if c>=0.8 else "⚠️" if c>=0.5 else "❌"
            st.markdown(f"""
<div class="sum-row-g">
  <div style="color:rgba(255,255,255,.38);font-weight:800">{log["attempt_num"]}</div>
  <div>{pill(log["strategy"])}</div>
  <div style="color:rgba(255,255,255,.6);font-size:.82rem">{log.get("feedback","—")}</div>
  <div style="color:{conf_clr(c)};font-weight:900">{ic} {pct}%</div>
</div>""", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="sec-lbl">🔍 Strategy Analysis</div>', unsafe_allow_html=True)
        for s in gs.get("strategies_used",[]):
            entry = next((l for l in st.session_state.attempt_log if l["strategy"]==s), None)
            c     = entry.get("confidence",0.0) if entry else 0.0
            worked= c>=0.8
            st.markdown(f"""
<div class="glass" style="padding:16px 20px;display:flex;align-items:center;gap:14px">
  <div style="font-size:1.6rem">{"✅" if worked else "❌"}</div>
  <div style="flex:1">
    <div>{pill(s)}</div>
    <div style="font-size:.78rem;color:rgba(255,255,255,.4);margin-top:6px">Confidence: <span style="color:{conf_clr(c)};font-weight:700">{int(c*100)}%</span></div>
  </div>
  <div style="font-size:.75rem;color:{"#34d399" if worked else "rgba(255,255,255,.3)"};font-weight:700">{"Mastered" if worked else "Not yet"}</div>
</div>""", unsafe_allow_html=True)

        # Overall verdict card
        st.markdown(f"""
<div class="{'glow-green' if won else 'glass'}" style="text-align:center;margin-top:12px;padding:22px">
  <div style="font-size:.68rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;
    color:rgba(255,255,255,.3);margin-bottom:8px">Final Score</div>
  <div style="font-size:3rem;font-weight:900;color:{conf_clr(fc)}">{int(fc*100)}%</div>
  <div style="font-size:.82rem;color:rgba(255,255,255,.45);margin-top:4px">
    {ta} attempt(s) · {"Mastered 🎓" if won else "Try again 🔁"}
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    b1,b2 = st.columns(2)
    with b1:
        if st.button("🌐  Try Another Concept", use_container_width=True, type="primary"): reset()
    with b2:
        if st.button("🔁  Retry Same Concept", use_container_width=True, type="secondary"):
            start_session(conc, gs.get("student_level","beginner")); st.rerun()
