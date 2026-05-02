import requests

FALLBACK_CONTENT = {
    "dynamic programming": (
        "Dynamic programming (DP) is an algorithmic technique for solving an optimization problem "
        "by breaking it down into simpler overlapping subproblems and storing the results of each "
        "subproblem so that the result is only computed once. Unlike divide-and-conquer where "
        "subproblems are independent, DP is used when subproblems share sub-subproblems. "
        "Two key properties: optimal substructure (optimal solution built from optimal sub-solutions) "
        "and overlapping subproblems (same subproblems solved repeatedly). "
        "Classic examples include: Fibonacci (top-down with memoization), Knapsack problem, "
        "Longest Common Subsequence, and shortest path (Bellman-Ford). "
        "Approaches: top-down (recursion + memoization) or bottom-up (tabulation)."
    ),
    "neural networks": (
        "A neural network is a computational model inspired by the structure of biological neurons "
        "in the brain. It consists of layers of interconnected nodes (neurons): an input layer, "
        "one or more hidden layers, and an output layer. Each connection has a weight that is adjusted "
        "during training. Forward propagation passes data through the network to produce a prediction. "
        "The error is measured using a loss function. Backpropagation computes gradients and gradient "
        "descent adjusts weights to minimize the loss. Activation functions (ReLU, sigmoid, softmax) "
        "introduce non-linearity. Deep neural networks with many hidden layers are called deep learning "
        "models and power image recognition, NLP, and generative AI."
    ),
    "big o notation": (
        "Big O notation is a mathematical notation that describes the limiting behavior of a function "
        "when the argument tends towards infinity. In computer science it describes the worst-case "
        "time or space complexity of an algorithm as the input size n grows. Common complexities: "
        "O(1) constant (array access), O(log n) logarithmic (binary search), O(n) linear (linear search), "
        "O(n log n) linearithmic (merge sort), O(n²) quadratic (bubble sort), O(2^n) exponential (brute-force). "
        "We drop constants and lower-order terms: 3n² + 5n + 2 becomes O(n²). "
        "Big O lets us compare algorithms independently of hardware or implementation details."
    ),

    "recursion": (
        "Recursion is a method of solving computational problems where the solution depends on solutions "
        "to smaller instances of the same problem. A recursive function has two key parts: a base case "
        "(the simplest case solved directly without recursion) and a recursive case (where the function "
        "calls itself with a simpler or smaller input). Classic examples include computing factorials, "
        "Fibonacci numbers, and tree traversals. Without a proper base case, recursion leads to infinite "
        "loops (stack overflow). The call stack grows with each recursive call and unwinds as each returns."
    ),
    "bayes theorem": (
        "Bayes' theorem describes the probability of an event based on prior knowledge of conditions "
        "related to the event. The formula is: P(A|B) = P(B|A) × P(A) / P(B). Here P(A|B) is the "
        "posterior probability of A given B has occurred; P(B|A) is the likelihood; P(A) is the prior "
        "probability of A; P(B) is the marginal probability of B. It is the foundation of Bayesian "
        "inference, spam filtering, medical diagnosis, and many machine learning algorithms. For example: "
        "given a positive medical test, Bayes theorem helps compute the actual probability of having "
        "the disease, accounting for false positive rates."
    ),
    "binary search tree": (
        "A binary search tree (BST) is a node-based binary tree data structure where each node has at "
        "most two children (left and right). The BST property: for any node, all values in its left "
        "subtree are less than the node's value, and all values in its right subtree are greater. "
        "This ordering enables efficient search, insertion, and deletion — O(log n) on average for a "
        "balanced BST. Operations: to search, compare and go left if smaller, right if larger. "
        "To insert, follow the same path and add at the appropriate leaf. Deletion is more complex "
        "when removing a node with two children (replace with in-order successor)."
    ),
}


def fetch_wikipedia_summary(concept: str) -> str:
    """Fetch Wikipedia plain-text summary for a concept, with curated fallback."""
    clean = concept.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean}"
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "EduTutor/1.0"})
        if resp.status_code == 200:
            extract = resp.json().get("extract", "")
            if len(extract) > 80:
                return extract[:2000]
    except Exception:
        pass

    key = concept.lower().strip()
    return FALLBACK_CONTENT.get(
        key,
        f"{concept} is a fundamental concept in computer science and mathematics."
    )
