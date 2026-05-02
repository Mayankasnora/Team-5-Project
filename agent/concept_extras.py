"""
concept_extras.py — Rich supplementary content for each concept:
  - Interactive Plotly charts
  - Fun facts
  - Code examples with syntax highlighting
"""
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# CHART COLOURS (match the UI palette)
# ─────────────────────────────────────────────────────────────────────────────
BG    = "rgba(0,0,0,0)"
GRID  = "rgba(255,255,255,0.06)"
TXT   = "rgba(255,255,255,0.75)"
ACC1  = "#a78bfa"   # purple
ACC2  = "#60a5fa"   # blue
ACC3  = "#34d399"   # green
ACC4  = "#fbbf24"   # yellow
ACC5  = "#f87171"   # red

LAYOUT_BASE = dict(
    paper_bgcolor=BG, plot_bgcolor=BG,
    font=dict(color=TXT, family="Inter, sans-serif", size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(bgcolor="rgba(255,255,255,0.04)", bordercolor=GRID),
    xaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
    yaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
)


def _layout(**kwargs):
    d = dict(LAYOUT_BASE)
    d.update(kwargs)
    return d


# ─────────────────────────────────────────────────────────────────────────────
# RECURSION
# ─────────────────────────────────────────────────────────────────────────────
def chart_recursion():
    """Fibonacci call-count: recursive vs DP."""
    ns = list(range(1, 16))
    memo = {}
    def fib_dp(n):
        if n <= 1: return n
        if n in memo: return memo[n]
        memo[n] = fib_dp(n-1) + fib_dp(n-2)
        return memo[n]

    call_counts = []
    def fib_naive(n):
        call_counts.append(1)
        if n <= 1: return n
        return fib_naive(n-1) + fib_naive(n-2)

    naive_calls = []
    for n in ns:
        call_counts.clear()
        fib_naive(n)
        naive_calls.append(len(call_counts))

    dp_calls = ns  # DP = exactly n calls

    fig = go.Figure()
    fig.add_trace(go.Bar(x=ns, y=naive_calls, name="Naive Recursion", marker_color=ACC5,
                         text=naive_calls, textposition="outside"))
    fig.add_trace(go.Bar(x=ns, y=dp_calls,    name="Memoized DP",     marker_color=ACC3,
                         text=dp_calls, textposition="outside"))
    fig.update_layout(**_layout(
        title="Fibonacci: Function calls — Naive vs Memoized",
        barmode="group", xaxis_title="n", yaxis_title="# calls",
        height=340,
    ))
    return fig


CODE_RECURSION = '''
# Classic recursion — fib(n)
def fibonacci(n):
    if n <= 1:          # ← base case (essential!)
        return n
    return fibonacci(n-1) + fibonacci(n-2)   # ← recursive calls

# Memoized version (far more efficient)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_fast(n):
    if n <= 1: return n
    return fib_fast(n-1) + fib_fast(n-2)

print(fib_fast(50))   # instant!
'''.strip()

FACTS_RECURSION = [
    "🐍 Python's default recursion limit is **1,000 calls** to prevent stack overflows.",
    "🌍 The **Tower of Hanoi** puzzle — optimal solution is purely recursive.",
    "📂 Your file system is a recursive structure — folders inside folders inside folders.",
    "🎮 Many classic games (chess, Go) use recursive **minimax** search to find best moves.",
]


# ─────────────────────────────────────────────────────────────────────────────
# BAYES THEOREM
# ─────────────────────────────────────────────────────────────────────────────
def chart_bayes():
    """Interactive belief update: prior → posterior."""
    labels = ["P(H) prior", "P(H|E) posterior"]
    prior = 0.1
    likelihood = 0.9
    p_evidence = prior * likelihood + (1 - prior) * 0.05
    posterior = (likelihood * prior) / p_evidence

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels,
        y=[prior, posterior],
        marker_color=[ACC2, ACC3],
        text=[f"{prior:.1%}", f"{posterior:.1%}"],
        textposition="outside",
        width=0.35,
    ))
    fig.add_annotation(
        x=0.5, y=(prior+posterior)/2 + 0.05,
        text=f"⬆ Updated by {posterior-prior:.1%} after evidence",
        showarrow=False, font=dict(color=ACC4, size=13), xref="paper", yref="y"
    )
    fig.update_layout(**_layout(
        title="Bayes: Belief Update After Seeing Evidence",
        yaxis=dict(range=[0, 1.1], gridcolor=GRID, tickformat=".0%"),
        height=320,
    ))
    return fig


CODE_BAYES = '''
# Bayes' Theorem: P(H|E) = P(E|H) * P(H) / P(E)

def bayes_update(prior, likelihood, false_positive=0.05):
    """
    prior       = P(H)   — belief before evidence
    likelihood  = P(E|H) — how likely evidence if H is true
    false_positive = P(E|¬H) — evidence chance if H is false
    """
    p_evidence = likelihood * prior + false_positive * (1 - prior)
    posterior  = (likelihood * prior) / p_evidence
    return posterior

# Worked example: medical test
prior_sick   = 0.01        # 1% of population has illness
test_accuracy = 0.95       # test detects illness 95% of time
false_pos     = 0.05       # 5% false-positive rate

result = bayes_update(prior_sick, test_accuracy, false_pos)
print(f"P(sick | positive test) = {result:.1%}")   # ≈ 16.1%
'''.strip()

FACTS_BAYES = [
    "📧 **Email spam filters** were the first large-scale use of Bayesian inference.",
    "🩺 A positive medical test often means **less than 20%** chance of disease — Bayes explains why!",
    "🔍 Thomas Bayes wrote the theorem in the 1740s; it was published **after his death**.",
    "🤖 Modern large language models use Bayesian-style reasoning under the hood.",
]


# ─────────────────────────────────────────────────────────────────────────────
# BINARY SEARCH TREE
# ─────────────────────────────────────────────────────────────────────────────
def chart_bst():
    """Scatter-plot tree structure for BST [8, 4, 12, 2, 6, 10, 14]."""
    nodes = [
        (8,  0.50, 1.0, "8 (root)"),
        (4,  0.25, 0.6, "4"),
        (12, 0.75, 0.6, "12"),
        (2,  0.12, 0.2, "2"),
        (6,  0.38, 0.2, "6"),
        (10, 0.62, 0.2, "10"),
        (14, 0.88, 0.2, "14"),
    ]
    edges = [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]

    fig = go.Figure()
    # edges
    for p, c in edges:
        fig.add_trace(go.Scatter(
            x=[nodes[p][1], nodes[c][1]], y=[nodes[p][2], nodes[c][2]],
            mode="lines", line=dict(color=GRID, width=2), showlegend=False,
            hoverinfo="none",
        ))
    # nodes
    colors = [ACC1, ACC2, ACC2, ACC3, ACC3, ACC3, ACC3]
    fig.add_trace(go.Scatter(
        x=[n[1] for n in nodes], y=[n[2] for n in nodes],
        mode="markers+text",
        marker=dict(size=38, color=colors, line=dict(color="white", width=1.5)),
        text=[n[0] for n in nodes],
        textfont=dict(size=14, color="white"),
        textposition="middle center",
        hovertext=[n[3] for n in nodes],
        hoverinfo="text",
        showlegend=False,
    ))
    fig.update_layout(**_layout(
        title="BST: [8, 4, 12, 2, 6, 10, 14] — left < root < right",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        height=330,
    ))
    return fig


CODE_BST = '''
class Node:
    def __init__(self, val):
        self.val   = val
        self.left  = None
        self.right = None

class BST:
    def insert(self, root, val):
        if not root: return Node(val)
        if val < root.val:
            root.left  = self.insert(root.left,  val)  # go left
        else:
            root.right = self.insert(root.right, val)  # go right
        return root

    def search(self, root, val):
        if not root or root.val == val: return root
        if val < root.val: return self.search(root.left,  val)
        return             self.search(root.right, val)

# Build the tree
bst  = BST()
root = None
for v in [8, 4, 12, 2, 6, 10, 14]:
    root = bst.insert(root, v)
'''.strip()

FACTS_BST = [
    "⚡ Search in a balanced BST is **O(log n)** — halves the search space every step.",
    "🔴 **Red-Black Trees** and **AVL Trees** are self-balancing BSTs used in databases.",
    "🗂️ Python's `bisect` module and C++'s `std::set` use BST-like structures internally.",
    "😱 A degenerate BST (sorted input) becomes a **linked list** — O(n) search!",
]


# ─────────────────────────────────────────────────────────────────────────────
# DYNAMIC PROGRAMMING
# ─────────────────────────────────────────────────────────────────────────────
def chart_dp():
    """DP memoization table for Fibonacci."""
    n = 10
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    fig = go.Figure(go.Bar(
        x=[f"F({i})" for i in range(n+1)],
        y=dp,
        marker=dict(
            color=dp,
            colorscale=[[0,"#7c3aed"],[1,"#34d399"]],
            showscale=False,
        ),
        text=dp, textposition="outside",
    ))
    fig.update_layout(**_layout(
        title="DP Memoization Table: Fibonacci F(0)…F(10)",
        xaxis_title="Sub-problem", yaxis_title="Value stored",
        height=320,
    ))
    return fig


CODE_DP = '''
# ─── Top-down (memoization) ───────────────────────────────
memo = {}
def fib_top_down(n):
    if n in memo: return memo[n]   # ← cache hit, skip work
    if n <= 1: return n
    memo[n] = fib_top_down(n-1) + fib_top_down(n-2)
    return memo[n]

# ─── Bottom-up (tabulation) ──────────────────────────────
def fib_bottom_up(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]   # ← fill table left→right
    return dp[n]

print(fib_top_down(40))    # 102334155 — instant!
print(fib_bottom_up(40))   # 102334155 — instant!
'''.strip()

FACTS_DP = [
    "🎒 The **0/1 Knapsack** problem (which items to pack for max value) is a classic DP problem.",
    "🧬 **DNA sequence alignment** in bioinformatics uses the DP algorithm LCS.",
    "💸 Richard Bellman coined 'dynamic programming' — the word 'dynamic' was just chosen to sound cool!",
    "🎮 Video game pathfinding (NPC movement) often uses DP-based shortest path algorithms.",
]


# ─────────────────────────────────────────────────────────────────────────────
# NEURAL NETWORKS
# ─────────────────────────────────────────────────────────────────────────────
def chart_nn():
    """Layer diagram: [3 inputs → 4 hidden → 2 output]."""
    layers = [[3, 0.15, ACC2], [4, 0.5, ACC1], [2, 0.85, ACC3]]
    labels = ["Input Layer", "Hidden Layer", "Output Layer"]
    fig    = go.Figure()

    positions = []
    for (count, x, color) in layers:
        ys = [(i - (count-1)/2) * 0.25 for i in range(count)]
        positions.append((x, ys, color))

    # Draw edges
    for li in range(len(positions)-1):
        x1, ys1, _ = positions[li]
        x2, ys2, _ = positions[li+1]
        for y1 in ys1:
            for y2 in ys2:
                fig.add_trace(go.Scatter(
                    x=[x1, x2], y=[y1, y2],
                    mode="lines", line=dict(color="rgba(167,139,250,0.12)", width=1),
                    showlegend=False, hoverinfo="none",
                ))

    # Draw nodes
    for i, (x, ys, color) in enumerate(positions):
        fig.add_trace(go.Scatter(
            x=[x]*len(ys), y=ys,
            mode="markers+text",
            marker=dict(size=30, color=color,
                        line=dict(color="white", width=1.5)),
            text=["●"]*len(ys), textfont=dict(size=10, color="white"),
            textposition="middle center",
            name=labels[i], hoverinfo="name",
        ))
        fig.add_annotation(x=x, y=max(ys)+0.22,
            text=f"<b>{labels[i]}</b><br>({len(ys)} neurons)",
            showarrow=False, font=dict(color=color, size=11))

    fig.update_layout(**_layout(
        title="Neural Network Architecture: 3 → 4 → 2",
        xaxis=dict(visible=False, range=[0,1]),
        yaxis=dict(visible=False, range=[-0.9,0.9]),
        height=360, showlegend=True,
    ))
    return fig


CODE_NN = '''
# Minimal 2-layer neural network (NumPy only)
import numpy as np

def sigmoid(x): return 1 / (1 + np.exp(-x))

class NeuralNet:
    def __init__(self, n_in, n_hidden, n_out):
        self.W1 = np.random.randn(n_in, n_hidden) * 0.1
        self.W2 = np.random.randn(n_hidden, n_out) * 0.1

    def forward(self, X):
        self.h = sigmoid(X @ self.W1)       # hidden layer
        return sigmoid(self.h @ self.W2)    # output layer

net = NeuralNet(n_in=3, n_hidden=4, n_out=2)
X   = np.array([[0.5, 0.2, 0.8]])
print(net.forward(X))   # predictions before training
'''.strip()

FACTS_NN = [
    "🧠 The human brain has **~86 billion** neurons; GPT-4 has ~1.8 trillion **parameters**.",
    "📸 ImageNet competition (2012): neural nets cut error rate by 10% overnight — the 'deep learning moment'.",
    "🎵 Neural networks can compose music, generate speech, and write code.",
    "⚡ Training GPT-3 consumed roughly the same energy as **driving a car 1 million km**.",
]


# ─────────────────────────────────────────────────────────────────────────────
# BIG O NOTATION
# ─────────────────────────────────────────────────────────────────────────────
def chart_bigo():
    """Complexity growth rate comparison."""
    n  = np.linspace(1, 20, 200)
    curves = [
        ("O(1)",        np.ones_like(n),       ACC3),
        ("O(log n)",    np.log2(n),             ACC2),
        ("O(n)",        n,                      ACC1),
        ("O(n log n)",  n * np.log2(n),         ACC4),
        ("O(n²)",       n**2,                   ACC5),
    ]
    fig = go.Figure()
    for name, y, color in curves:
        fig.add_trace(go.Scatter(
            x=n, y=y, name=name,
            mode="lines", line=dict(color=color, width=2.5),
        ))
    fig.update_layout(**_layout(
        title="Big O: How algorithms scale as input grows",
        xaxis_title="Input size (n)", yaxis_title="Operations",
        yaxis=dict(range=[0, 120], gridcolor=GRID),
        height=360,
    ))
    return fig


CODE_BIGO = '''
import time

def linear_search(arr, target):      # O(n)
    for x in arr:
        if x == target: return True
    return False

def binary_search(arr, target):      # O(log n) — requires sorted array
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return True
        elif arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return False

import random
data = sorted(random.sample(range(10**6), 10**5))

# Both find the same element — but binary search is ~17x fewer steps
print(linear_search(data, data[50000]))   # O(n)
print(binary_search(data, data[50000]))   # O(log n) ← much faster
'''.strip()

FACTS_BIGO = [
    "🔍 Google Search indexes **~130 trillion** pages — only possible with sub-linear algorithms.",
    "⚡ A 1-second O(n²) algorithm becomes a **11.5 DAY** wait for n = 1 million!",
    "🗂️ The best possible **comparison-based sort** is O(n log n) — mathematically proven.",
    "💾 O(1) space means 'constant memory' — your algorithm uses the same RAM for n=10 and n=10 billion.",
]


# ─────────────────────────────────────────────────────────────────────────────
# WORKED EXAMPLES (mathematical / logical / coding trace)
# ─────────────────────────────────────────────────────────────────────────────

EXAMPLES = {}

EXAMPLES["Recursion"] = """
### 🔢 Tracing `factorial(4)` step by step

```
factorial(4)
  └─ 4 × factorial(3)
          └─ 3 × factorial(2)
                  └─ 2 × factorial(1)
                          └─ 1 × factorial(0)
                                  └─ returns 1   ← BASE CASE hit!
                          returns 1×1 = 1
                  returns 2×1 = 2
          returns 3×2 = 6
  returns 4×6 = 24  ✅
```

**Key observations**
| Step | Call | Return value |
|------|------|-------------|
| 1 | `factorial(4)` | waits… |
| 2 | `factorial(3)` | waits… |
| 3 | `factorial(2)` | waits… |
| 4 | `factorial(1)` | waits… |
| 5 | `factorial(0)` | **1** (base case) |
| 6 | `factorial(1)` | 1×1 = **1** |
| 7 | `factorial(2)` | 2×1 = **2** |
| 8 | `factorial(3)` | 3×2 = **6** |
| 9 | `factorial(4)` | 4×6 = **24** |

> 📌 **Without a base case**, the stack keeps growing → `RecursionError` crash!
"""

EXAMPLES["Bayes Theorem"] = """
### 🏥 Medical Test Example (step by step)

**Setup:**
- Disease affects **1%** of population → P(Disease) = 0.01
- Test is **95% accurate** (sensitivity) → P(+ve | Disease) = 0.95
- Test has **5% false positive** rate → P(+ve | No Disease) = 0.05

**Question:** If you test positive, what is the actual probability you have the disease?

**Step 1 — Apply Bayes' Theorem:**
$$P(Disease | +ve) = \\frac{P(+ve | Disease) \\times P(Disease)}{P(+ve)}$$

**Step 2 — Compute P(+ve) using total probability rule:**
```
P(+ve) = P(+ve|Disease)×P(Disease) + P(+ve|No Disease)×P(No Disease)
       = 0.95 × 0.01 + 0.05 × 0.99
       = 0.0095 + 0.0495
       = 0.059
```

**Step 3 — Compute posterior:**
```
P(Disease | +ve) = (0.95 × 0.01) / 0.059
                 = 0.0095 / 0.059
                 ≈ 0.161  →  16.1% !!
```

> 😲 Despite a 95% accurate test, a positive result means only a **16% chance** of actually being sick. This is why doctors retest before diagnosing!
"""

EXAMPLES["Binary Search Tree"] = """
### 🌳 Insert `[8, 3, 10, 1, 6]` into a BST — trace

```
Insert 8:          8 (root)

Insert 3:          8
                  /
                 3          (3 < 8 → go LEFT)

Insert 10:         8
                  / \\
                 3   10     (10 > 8 → go RIGHT)

Insert 1:          8
                  / \\
                 3   10
                /
               1            (1 < 8 → LEFT, 1 < 3 → LEFT)

Insert 6:          8
                  / \\
                 3   10
                / \\
               1   6        (6 < 8 → LEFT, 6 > 3 → RIGHT)
```

### 🔍 Search for `6` — trace
```
Start at 8  →  6 < 8  →  go LEFT
At 3        →  6 > 3  →  go RIGHT
At 6        →  FOUND! ✅  (only 3 comparisons for 5 nodes)
```

**Why this is O(log n):** Each step eliminates half the remaining tree.
"""

EXAMPLES["Dynamic Programming"] = """
### 🧩 Longest Common Subsequence (LCS) — classic DP

Find the **LCS** of `"ABCB"` and `"BDCAB"`

**DP Table** (cell = length of LCS up to that prefix):

|   |   | B | D | C | A | B |
|---|---|---|---|---|---|---|
|   | 0 | 0 | 0 | 0 | 0 | 0 |
| **A** | 0 | 0 | 0 | 0 | **1** | 1 |
| **B** | 0 | **1** | 1 | 1 | 1 | **2** |
| **C** | 0 | 1 | 1 | **2** | 2 | 2 |
| **B** | 0 | 1 | 1 | 2 | 2 | **3** |

**Rule:** If `s1[i]==s2[j]` → `dp[i][j] = dp[i-1][j-1] + 1`  
Else → `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

**Result:** LCS = **"BCB"** (length 3)

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

print(lcs("ABCB", "BDCAB"))   # 3
```
"""

EXAMPLES["Neural Networks"] = """
### ⚡ Forward Pass — step by step (tiny network)

**Network:** 2 inputs → 2 hidden → 1 output  
**Activation:** Sigmoid σ(x) = 1/(1+e⁻ˣ)

**Inputs:** x₁ = 0.5, x₂ = 0.8

**Step 1 — Compute hidden layer (h₁, h₂):**
```
Weights W1 = [[0.4, 0.6], [0.3, 0.8]]

z₁ = 0.4×0.5 + 0.3×0.8 = 0.20 + 0.24 = 0.44
z₂ = 0.6×0.5 + 0.8×0.8 = 0.30 + 0.64 = 0.94

h₁ = σ(0.44) ≈ 0.608
h₂ = σ(0.94) ≈ 0.719
```

**Step 2 — Compute output:**
```
Weights W2 = [0.5, 0.7]

z_out = 0.5×0.608 + 0.7×0.719 = 0.304 + 0.503 = 0.807
output = σ(0.807) ≈ 0.692
```

**Step 3 — Loss (if true label = 1.0):**
```
MSE Loss = (1.0 - 0.692)² = 0.308² ≈ 0.095
```

Backprop would now compute gradients and nudge W1, W2 to reduce this loss.

> 🔁 Repeat for thousands of examples → network **learns**!
"""

EXAMPLES["Big O Notation"] = """
### ⏱️ Counting Operations — concrete examples

**Array of size n = 8: `[3, 1, 4, 1, 5, 9, 2, 6]`**

---
**O(1) — Array lookup:**
```
arr[3]  →  1 operation, always.  ✅
```

---
**O(log n) — Binary search for 5:**
```
Step 1: mid = 4 → arr[4]=5?  No, 5 > 4 → RIGHT half
Step 2: mid = 6 → arr[6]=2?  No, 5 > 2 → RIGHT half
Step 3: mid = 7 → arr[7]=6?  No, 5 < 6 → LEFT half
Step 4: Found 5 ✅   →  4 steps for n=8  (log₂8 = 3~4)
```

---
**O(n) — Linear search for 9:**
```
Check 3→1→4→1→5→9  →  6 comparisons
```

---
**O(n²) — Bubble sort passes:**
```
Pass 1: n-1 = 7 comparisons
Pass 2: n-2 = 6 comparisons
...
Total: 7+6+5+4+3+2+1 = 28 = n(n-1)/2 ≈ n²
```

**Growth comparison for n = 1,000:**
| Complexity | Operations |
|---|---|
| O(1) | 1 |
| O(log n) | ~10 |
| O(n) | 1,000 |
| O(n log n) | ~10,000 |
| O(n²) | 1,000,000 😱 |
"""


# ─────────────────────────────────────────────────────────────────────────────
# MASTER LOOKUP
# ─────────────────────────────────────────────────────────────────────────────
EXTRAS = {
    "Recursion":           (chart_recursion, CODE_RECURSION, FACTS_RECURSION, EXAMPLES["Recursion"]),
    "Bayes Theorem":       (chart_bayes,     CODE_BAYES,     FACTS_BAYES,     EXAMPLES["Bayes Theorem"]),
    "Binary Search Tree":  (chart_bst,       CODE_BST,       FACTS_BST,       EXAMPLES["Binary Search Tree"]),
    "Dynamic Programming": (chart_dp,        CODE_DP,        FACTS_DP,        EXAMPLES["Dynamic Programming"]),
    "Neural Networks":     (chart_nn,        CODE_NN,        FACTS_NN,        EXAMPLES["Neural Networks"]),
    "Big O Notation":      (chart_bigo,      CODE_BIGO,      FACTS_BIGO,      EXAMPLES["Big O Notation"]),
}


def get_extras(concept: str):
    """Returns (fig, code_str, facts_list, examples_md) or (None, None, [], '') if not found."""
    if concept not in EXTRAS:
        return None, None, [], ""
    chart_fn, code, facts, examples = EXTRAS[concept]
    try:
        fig = chart_fn()
    except Exception:
        fig = None
    return fig, code, facts, examples
