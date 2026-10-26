"""
Database module for Learnify AI
Uses Python's built-in sqlite3 for lightweight persistence.
"""

import sqlite3
import os
import json
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "learnify.db")


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create all tables if they don't exist and run non-destructive migrations."""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sources (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                url TEXT
            );

            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                unit INTEGER NOT NULL,
                description TEXT,
                estimated_hours INTEGER DEFAULT 3,
                category TEXT DEFAULT 'AI Foundations'
            );

            CREATE TABLE IF NOT EXISTS knowledge (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                topic_id TEXT,
                source_id TEXT,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics(id),
                FOREIGN KEY (source_id) REFERENCES sources(id)
            );

            CREATE TABLE IF NOT EXISTS faq (
                id TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT,
                source_id TEXT,
                FOREIGN KEY (source_id) REFERENCES sources(id)
            );

            CREATE TABLE IF NOT EXISTS topic_relationships (
                parent_id TEXT NOT NULL,
                child_id TEXT NOT NULL,
                relationship TEXT DEFAULT 'prerequisite',
                PRIMARY KEY (parent_id, child_id),
                FOREIGN KEY (parent_id) REFERENCES topics(id),
                FOREIGN KEY (child_id) REFERENCES topics(id)
            );

            -- Phase 3 (Hiran Antony): Declarative Policies, Decision Rules & Knowledge Facts
            CREATE TABLE IF NOT EXISTS policies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                version TEXT DEFAULT '1.0.0',
                is_illustrative INTEGER DEFAULT 1,
                disclaimer TEXT,
                default_decision TEXT DEFAULT 'INELIGIBLE'
            );

            CREATE TABLE IF NOT EXISTS rules (
                id TEXT PRIMARY KEY,
                policy_id TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                conditions_json TEXT NOT NULL,
                conclusion_json TEXT NOT NULL,
                priority INTEGER DEFAULT 10,
                is_exception INTEGER DEFAULT 0,
                overrides_rule_id TEXT,
                source_id TEXT DEFAULT 'src-demo',
                FOREIGN KEY (policy_id) REFERENCES policies(id),
                FOREIGN KEY (source_id) REFERENCES sources(id)
            );

            CREATE TABLE IF NOT EXISTS verified_facts (
                id TEXT PRIMARY KEY,
                entity_id TEXT NOT NULL,
                predicate TEXT NOT NULL,
                arguments_json TEXT,
                value_json TEXT,
                source_id TEXT DEFAULT 'src-demo',
                verification_status TEXT DEFAULT 'VERIFIED',
                policy_id TEXT,
                context TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES sources(id)
            );
        """)

        # Non-destructive column migrations for existing databases
        cursor = conn.execute("PRAGMA table_info(topics)")
        columns = [row["name"] for row in cursor.fetchall()]
        if "estimated_hours" not in columns:
            conn.execute("ALTER TABLE topics ADD COLUMN estimated_hours INTEGER DEFAULT 3")
        if "category" not in columns:
            conn.execute("ALTER TABLE topics ADD COLUMN category TEXT DEFAULT 'AI Foundations'")


def seed_db():
    """
    Populate the database with sample educational data.
    Uses INSERT OR IGNORE so it's safe to re-run without duplicates.
    """
    with get_db() as conn:
        # --- Sources ---
        sources = [
            ("src-textbook", "AI: A Modern Approach (Russell & Norvig)", "Standard AI textbook reference", None),
            ("src-coursework", "Learnify AI Course Materials", "Curated course content for Unit I–V", None),
            ("src-demo", "Illustrative Demo Data", "Illustrative demo data — not official institutional policy", None),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO sources (id, name, description, url) VALUES (?, ?, ?, ?)",
            sources,
        )

        # --- Topics (Unit I-V Curated Educational Graph) ---
        topics = [
            ("topic-prog-fund", "Programming Fundamentals", 1, "Variables, control structures, functions, and algorithm basics", 3, "Core Programming"),
            ("topic-python-basics", "Python Basics", 1, "Python syntax, lists, dicts, tuples, and scripting for AI", 4, "Core Programming"),
            ("topic-discrete-math", "Discrete Mathematics", 1, "Sets, relations, graphs, trees, and Boolean algebra", 5, "Foundational Math"),
            ("topic-probability", "Probability", 1, "Random variables, distributions, conditional probability, and expectation", 4, "Foundational Math"),
            ("topic-statistics", "Statistics", 1, "Descriptive statistics, inferential tests, estimation, and hypothesis testing", 4, "Foundational Math"),
            ("topic-linear-algebra", "Linear Algebra", 1, "Vectors, matrices, eigenvalues, dot products, and transformations", 5, "Foundational Math"),
            ("topic-ai-foundations", "Artificial Intelligence Foundations", 1, "Core AI concepts, history, definitions, and philosophy", 3, "AI Foundations"),
            ("topic-intelligent-agents", "Intelligent Agents", 1, "Agent types (reflex, model, goal, utility), environments, and rationality", 3, "AI Foundations"),
            ("topic-problem-solving", "Problem Solving", 1, "Problem formulation, states, transitions, actions, and goal tests", 3, "Search & Planning"),
            ("topic-state-spaces", "State Spaces & Problem Formulation", 2, "State spaces, branching factors, graph representation, and frontiers", 3, "Search & Planning"),
            ("topic-search-bfs-dfs", "Search Algorithms: BFS & DFS", 2, "Uninformed search strategies: FIFO queue BFS and LIFO stack DFS", 4, "Search & Planning"),
            ("topic-bidirectional-search", "Bidirectional Search", 2, "Simultaneous forward and backward exploration meeting at an intersection", 3, "Search & Planning"),
            ("topic-heuristic-search", "Heuristic Search", 2, "Informed search with heuristics: Greedy Best-First and A* algorithms", 4, "Search & Planning"),
            ("topic-csp-search", "Constraint Satisfaction & Backtracking", 2, "Variables, domains, constraints, and backtracking search with heuristics", 4, "Search & Planning"),
            ("topic-knowledge-rep", "Knowledge Representation", 3, "Semantic networks, conceptual frames, ontologies, and taxonomy", 4, "Logic & Knowledge"),
            ("topic-prop-logic", "Propositional Logic", 3, "Boolean propositions, connectives, truth tables, and inference rules", 3, "Logic & Knowledge"),
            ("topic-predicate-logic", "Predicate Logic", 3, "First-order logic (FOL), variables, predicates, and quantifiers", 4, "Logic & Knowledge"),
            ("topic-forward-backward", "Forward and Backward Chaining", 4, "Rule-based deduction: data-driven forward and goal-driven backward chaining", 4, "Inference & Rules"),
            ("topic-bayesian", "Bayesian Reasoning", 4, "Probabilistic inference, Bayes' rule, conditional independence, and belief networks", 4, "Probabilistic Reasoning"),
            ("topic-expert-systems", "Expert Systems", 5, "Architecture of expert systems: knowledge base, inference engine, and explanation", 3, "Applied AI Systems"),
            ("topic-machine-learning", "Machine Learning", 5, "Supervised, unsupervised, and reinforcement learning principles", 6, "Machine Learning"),
            ("topic-neural-networks", "Neural Networks & Deep Learning", 5, "Perceptrons, multi-layer networks, backpropagation, and activations", 5, "Machine Learning"),
            ("topic-study-prep", "Study Preparation", 1, "General study, revision strategies, and AI exam preparation guidance", 2, "Academic Skills"),
        ]
        conn.executemany(
            "INSERT OR REPLACE INTO topics (id, name, unit, description, estimated_hours, category) VALUES (?, ?, ?, ?, ?, ?)",
            topics,
        )

        # --- Topic relationships (Directed prerequisite graph: parent_id -> child_id means parent is prerequisite for child) ---
        relationships = [
            # Core Programming -> Problem Solving & ML
            ("topic-prog-fund", "topic-python-basics", "prerequisite"),
            ("topic-python-basics", "topic-problem-solving", "prerequisite"),
            ("topic-python-basics", "topic-machine-learning", "prerequisite"),

            # Foundational Math -> Logic, State Spaces, Stats, ML
            ("topic-discrete-math", "topic-prop-logic", "prerequisite"),
            ("topic-discrete-math", "topic-state-spaces", "prerequisite"),
            ("topic-linear-algebra", "topic-machine-learning", "prerequisite"),
            ("topic-linear-algebra", "topic-neural-networks", "prerequisite"),
            ("topic-probability", "topic-statistics", "prerequisite"),
            ("topic-probability", "topic-bayesian", "prerequisite"),
            ("topic-statistics", "topic-machine-learning", "prerequisite"),

            # AI Foundations -> Agents, Problem Solving, Knowledge Rep
            ("topic-ai-foundations", "topic-intelligent-agents", "prerequisite"),
            ("topic-ai-foundations", "topic-problem-solving", "prerequisite"),
            ("topic-ai-foundations", "topic-knowledge-rep", "prerequisite"),

            # Problem Solving -> State Spaces -> Search
            ("topic-problem-solving", "topic-state-spaces", "prerequisite"),
            ("topic-state-spaces", "topic-search-bfs-dfs", "prerequisite"),
            ("topic-search-bfs-dfs", "topic-bidirectional-search", "prerequisite"),
            ("topic-search-bfs-dfs", "topic-heuristic-search", "prerequisite"),
            ("topic-search-bfs-dfs", "topic-csp-search", "prerequisite"),

            # Logic & Knowledge
            ("topic-knowledge-rep", "topic-prop-logic", "prerequisite"),
            ("topic-prop-logic", "topic-predicate-logic", "prerequisite"),
            ("topic-predicate-logic", "topic-forward-backward", "prerequisite"),
            ("topic-forward-backward", "topic-expert-systems", "prerequisite"),

            # Search & ML -> Neural Networks
            ("topic-heuristic-search", "topic-machine-learning", "prerequisite"),
            ("topic-machine-learning", "topic-neural-networks", "prerequisite"),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO topic_relationships (parent_id, child_id, relationship) VALUES (?, ?, ?)",
            relationships,
        )

        # --- Knowledge records ---
        knowledge = [
            # AI Foundations
            ("k-ai-definition", "What is Artificial Intelligence?",
             "Artificial Intelligence (AI) is the branch of computer science that aims to create systems capable of performing tasks that typically require human intelligence. These tasks include learning from experience, understanding natural language, recognizing patterns, making decisions, and solving problems. AI can be categorized into Narrow AI (designed for specific tasks like image recognition or language translation) and General AI (hypothetical systems with human-level cognitive abilities across all domains). Modern AI primarily relies on machine learning, where systems improve their performance through exposure to data rather than explicit programming.",
             "topic-ai-foundations", "src-textbook", "artificial intelligence,AI,definition,what is ai,intelligence"),

            ("k-ai-history", "History of Artificial Intelligence",
             "The field of Artificial Intelligence was formally founded at the Dartmouth Conference in 1956, organized by John McCarthy, Marvin Minsky, Nathaniel Rochester, and Claude Shannon. Key milestones include: the creation of the Logic Theorist (1956) by Newell and Simon, ELIZA (1966) by Weizenbaum demonstrating natural language processing, expert systems like MYCIN (1970s) for medical diagnosis, the Deep Blue chess victory (1997), IBM Watson's Jeopardy win (2011), and the rise of deep learning with AlphaGo (2016). The field experienced periods of reduced funding known as 'AI Winters' in the 1970s and late 1980s, before the current resurgence driven by big data, increased computing power, and advances in neural network architectures.",
             "topic-ai-foundations", "src-textbook", "history,AI history,dartmouth,milestones,timeline"),

            ("k-ai-applications", "Applications of Artificial Intelligence",
             "AI is applied across numerous domains: (1) Healthcare — disease diagnosis, drug discovery, medical imaging analysis; (2) Finance — fraud detection, algorithmic trading, credit scoring; (3) Transportation — self-driving vehicles, route optimization, traffic management; (4) Education — intelligent tutoring systems, automated grading, personalized learning paths; (5) Natural Language Processing — machine translation, chatbots, sentiment analysis; (6) Computer Vision — facial recognition, object detection, autonomous navigation; (7) Robotics — manufacturing automation, surgical robots, exploration; (8) Gaming — game-playing AI, procedural content generation. Each application area uses different AI techniques suited to the specific problem domain.",
             "topic-ai-foundations", "src-coursework", "applications,uses,domains,healthcare,finance,education"),

            # Intelligent Agents
            ("k-agent-definition", "What is an Intelligent Agent?",
             "An intelligent agent is a system that perceives its environment through sensors and acts upon that environment through actuators to achieve its goals. Key properties include: (1) Autonomy — operates without direct human intervention; (2) Reactivity — responds to changes in the environment in a timely fashion; (3) Proactiveness — takes initiative to achieve goals; (4) Social ability — interacts with other agents or humans. The agent's behavior is described by its agent function, which maps percept sequences to actions. A rational agent selects actions that maximize its expected performance measure given the percept sequence and built-in knowledge.",
             "topic-intelligent-agents", "src-textbook", "agent,intelligent agent,rational agent,autonomy,reactivity"),

            ("k-agent-types", "Types of Intelligent Agents",
             "There are several types of agents with increasing sophistication: (1) Simple Reflex Agents — act only on the current percept, using condition-action rules (if-then). They work in fully observable environments but fail with partial observability. (2) Model-Based Reflex Agents — maintain an internal model of the world to handle partial observability. They track aspects of the world they cannot currently see. (3) Goal-Based Agents — act to achieve specific goals, using search and planning algorithms to determine actions. (4) Utility-Based Agents — use a utility function to evaluate how desirable different states are, handling trade-offs between conflicting goals. (5) Learning Agents — improve their performance over time through a learning element, performance element, critic, and problem generator.",
             "topic-intelligent-agents", "src-textbook", "agent types,simple reflex,model-based,goal-based,utility-based,learning agent"),

            ("k-agent-environment", "Agent Environment Properties",
             "Agent environments are characterized by several properties: (1) Fully Observable vs. Partially Observable — whether the agent can see the complete state of the environment; (2) Deterministic vs. Stochastic — whether the next state is completely determined by the current state and action; (3) Episodic vs. Sequential — whether the agent's experience is divided into independent episodes; (4) Static vs. Dynamic — whether the environment changes while the agent is deliberating; (5) Discrete vs. Continuous — whether state, time, and actions are discrete or continuous; (6) Single-Agent vs. Multi-Agent — whether other agents are operating in the environment. These properties affect which agent architecture is most appropriate.",
             "topic-intelligent-agents", "src-coursework", "environment,observable,deterministic,static,dynamic,discrete"),

            # BFS and DFS
            ("k-bfs", "Breadth-First Search (BFS)",
             "Breadth-First Search is an uninformed search algorithm that explores all nodes at the present depth level before moving to nodes at the next depth level. It uses a FIFO queue (First-In, First-Out) as its frontier data structure. Properties: (1) Complete — guaranteed to find a solution if one exists (for finite graphs); (2) Optimal — finds the shallowest solution (optimal when all step costs are equal); (3) Time Complexity — O(b^d) where b is the branching factor and d is the depth of the shallowest solution; (4) Space Complexity — O(b^d), which is its main limitation as it stores all generated nodes. BFS is used in shortest path problems, social network analysis, web crawling, and puzzle solving like the 15-puzzle.",
             "topic-search-bfs-dfs", "src-textbook", "BFS,breadth-first search,uninformed search,queue,FIFO,shortest path"),

            ("k-dfs", "Depth-First Search (DFS)",
             "Depth-First Search is an uninformed search algorithm that explores as far as possible along each branch before backtracking. It uses a LIFO stack (Last-In, First-Out) as its frontier or can be implemented recursively. Properties: (1) Not complete in infinite state spaces (can get stuck in infinite loops without cycle detection); (2) Not optimal — may find a deeper solution before a shallower one; (3) Time Complexity — O(b^m) where m is the maximum depth; (4) Space Complexity — O(b*m), which is its main advantage over BFS as it only stores nodes along the current path. DFS is useful for topological sorting, cycle detection in graphs, solving mazes, and generating game trees. Depth-Limited Search and Iterative Deepening address its completeness issues.",
             "topic-search-bfs-dfs", "src-textbook", "DFS,depth-first search,uninformed search,stack,LIFO,backtracking"),

            ("k-bfs-vs-dfs", "Comparing BFS and DFS",
             "BFS and DFS are complementary uninformed search strategies with different strengths: BFS guarantees finding the optimal (shallowest) solution and is complete for finite graphs, but requires O(b^d) memory. DFS uses only O(b*m) memory but may not find the optimal solution and can be incomplete in infinite spaces. For finding the shortest path, BFS is preferred. For memory-constrained problems, DFS is preferred. Iterative Deepening Depth-First Search (IDDFS) combines the best of both: it is complete, optimal for unit-cost actions, uses O(b*d) space like DFS, but explores nodes in BFS order. In practice, the overhead of re-expanding nodes in IDDFS is usually small compared to the exponential growth at each level.",
             "topic-search-bfs-dfs", "src-coursework", "BFS vs DFS,comparison,iterative deepening,IDDFS,search comparison"),

            # Heuristic Search
            ("k-heuristic-search", "Heuristic Search and A* Algorithm",
             "Heuristic search uses problem-specific knowledge (heuristics) to guide the search toward the goal more efficiently than uninformed methods. A* is the most well-known heuristic search algorithm that uses an evaluation function f(n) = g(n) + h(n), where g(n) is the cost to reach node n from the start and h(n) is the estimated cost from n to the goal (the heuristic). A* is both complete and optimal when the heuristic h(n) is admissible (never overestimates the true cost) and consistent (satisfies the triangle inequality). Examples of heuristics include Manhattan distance for grid navigation and misplaced tiles for the 8-puzzle. Greedy Best-First Search uses only h(n) and is faster but not optimal.",
             "topic-heuristic-search", "src-textbook", "heuristic,A*,A-star,informed search,admissible,best-first"),

            ("k-hill-climbing", "Hill Climbing Search",
             "Hill Climbing is a local search algorithm that continuously moves toward increasing value (or decreasing cost) — it is like climbing to the top of a hill. The algorithm selects the neighbor with the highest value and moves to it. Variants include: (1) Steepest-Ascent — evaluates all neighbors and moves to the best; (2) Stochastic — randomly selects among uphill moves; (3) Random-Restart — runs multiple hill climbs from random starting points. Limitations include getting stuck at local maxima, ridges, and plateaus. Despite these limitations, hill climbing is effective for many optimization problems due to its simplicity and low memory requirements. Simulated Annealing addresses local maxima by occasionally accepting worse moves.",
             "topic-heuristic-search", "src-coursework", "hill climbing,local search,optimization,local maxima,simulated annealing"),

            # Knowledge Representation
            ("k-knowledge-rep", "Knowledge Representation in AI",
             "Knowledge representation is the study of how beliefs, intentions, and value judgments of an intelligent agent can be expressed in a form suitable for automated reasoning. Key approaches include: (1) Semantic Networks — graph structures where nodes represent concepts and edges represent relationships; (2) Frames — data structures with slots for attributes and their values, supporting inheritance; (3) Ontologies — formal, explicit specifications of shared conceptualizations, defining concepts, properties, and relationships in a domain; (4) Production Rules — IF-THEN rules capturing procedural knowledge; (5) Logic-based — using propositional or predicate logic for precise, formal representation. Good representations should be expressive, concise, unambiguous, context-independent, and support efficient inference.",
             "topic-knowledge-rep", "src-textbook", "knowledge representation,semantic network,frames,ontology,representation"),

            # Predicate Logic
            ("k-predicate-logic", "Predicate Logic (First-Order Logic)",
             "Predicate Logic, also called First-Order Logic (FOL), extends propositional logic by introducing predicates, variables, quantifiers, and functions. It can express statements about objects and their relationships that propositional logic cannot. Key components: (1) Constants — specific objects (e.g., John, 42); (2) Variables — placeholders for objects (x, y); (3) Predicates — properties or relationships (e.g., Student(x), Teaches(x,y)); (4) Quantifiers — Universal (∀x: for all x) and Existential (∃x: there exists an x); (5) Connectives — AND (∧), OR (∨), NOT (¬), IMPLIES (→), IFF (↔). Example: ∀x(Student(x) → ∃y(Teaches(y,x))) means 'every student has at least one teacher'. FOL is the foundation for many AI reasoning systems.",
             "topic-predicate-logic", "src-textbook", "predicate logic,first-order logic,FOL,quantifiers,predicates,variables"),

            # Forward and Backward Chaining
            ("k-forward-chaining", "Forward Chaining",
             "Forward chaining is a data-driven inference strategy that starts with known facts and applies rules to derive new facts until a goal is reached or no more rules can fire. The process: (1) Start with initial facts in working memory; (2) Check which rules have their conditions satisfied; (3) Select a rule using conflict resolution if multiple rules match; (4) Fire the selected rule, adding its conclusion to working memory; (5) Repeat until the goal is derived or no rules apply. Forward chaining is used in monitoring systems, real-time control, and production systems like OPS5. It is efficient when many inputs lead to few conclusions (data-rich problems).",
             "topic-forward-backward", "src-textbook", "forward chaining,data-driven,inference,production system,rules"),

            ("k-backward-chaining", "Backward Chaining",
             "Backward chaining is a goal-driven inference strategy that starts with a goal and works backward to find supporting facts. The process: (1) Start with the goal to prove; (2) Find rules whose conclusion matches the goal; (3) Check if the rule's premises are known facts; (4) If not, set each unknown premise as a new sub-goal and recurse; (5) The goal is proved when all sub-goals resolve to known facts. Backward chaining is used in diagnostic systems, expert systems like MYCIN, and Prolog programming. It is efficient when there are many possible conclusions but the query asks about specific goals. It avoids deriving irrelevant facts, unlike forward chaining.",
             "topic-forward-backward", "src-textbook", "backward chaining,goal-driven,inference,diagnostic,Prolog"),

            # Expert Systems
            ("k-expert-systems", "Expert Systems",
             "An expert system is an AI program that emulates the decision-making ability of a human expert in a specific domain. Architecture: (1) Knowledge Base — contains domain-specific facts and rules (usually IF-THEN production rules); (2) Inference Engine — applies logical rules to the knowledge base to derive conclusions, using forward or backward chaining; (3) Explanation Facility — explains the reasoning process to the user (why a conclusion was reached); (4) User Interface — allows users to interact with the system. Famous examples include MYCIN (bacterial infection diagnosis), DENDRAL (chemical structure analysis), XCON/R1 (computer configuration), and CLIPS (general-purpose expert system shell). Expert systems excel in narrow, well-defined domains.",
             "topic-expert-systems", "src-textbook", "expert system,knowledge base,inference engine,MYCIN,DENDRAL,rules"),

            # Machine Learning
            ("k-machine-learning", "Introduction to Machine Learning",
             "Machine Learning (ML) is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. Main paradigms: (1) Supervised Learning — trained on labeled data to predict outputs (classification for discrete labels, regression for continuous values). Examples: spam detection, price prediction; (2) Unsupervised Learning — finds patterns in unlabeled data (clustering, dimensionality reduction). Examples: customer segmentation, anomaly detection; (3) Reinforcement Learning — learns by interacting with an environment, receiving rewards or penalties. Examples: game playing, robot control. Key concepts include training/test splits, overfitting/underfitting, bias-variance tradeoff, cross-validation, and feature engineering.",
             "topic-machine-learning", "src-textbook", "machine learning,ML,supervised,unsupervised,reinforcement,classification,regression"),

            ("k-ml-prerequisites", "Prerequisites for Studying Machine Learning",
             "To study machine learning effectively, you need foundations in: (1) Mathematics — linear algebra (vectors, matrices, eigenvalues), calculus (derivatives, gradients, optimization), probability and statistics (distributions, Bayes' theorem, hypothesis testing); (2) Programming — proficiency in Python, familiarity with libraries like NumPy, Pandas, Scikit-learn; (3) Data Analysis — understanding data preprocessing, feature engineering, exploratory data analysis; (4) AI Fundamentals — basic understanding of search algorithms, knowledge representation, and problem-solving strategies. Start with supervised learning (linear regression, decision trees) before advancing to deep learning. Practice with real datasets from sources like Kaggle or UCI Machine Learning Repository.",
             "topic-machine-learning", "src-coursework", "prerequisites,math,linear algebra,calculus,statistics,preparation"),

            # Problem Solving
            ("k-problem-solving", "Problem-Solving in AI",
             "Problem-solving in AI involves formulating tasks as search problems with well-defined components: (1) Initial State — the starting configuration; (2) Actions — operations available to the agent; (3) Transition Model — describes the result of applying an action to a state; (4) Goal Test — determines whether a given state is a goal state; (5) Path Cost — assigns a numeric cost to each path. A solution is a sequence of actions leading from the initial state to a goal state; an optimal solution has the lowest path cost. Examples include route finding (initial: start city, goal: destination), 8-puzzle (initial: scrambled tiles, goal: ordered tiles), and constraint satisfaction (initial: empty assignment, goal: consistent complete assignment).",
             "topic-problem-solving", "src-textbook", "problem solving,state space,initial state,goal,actions,search"),

            # Study Preparation
            ("k-exam-prep", "Exam Preparation Strategies for AI",
             "Effective strategies for preparing for an AI examination: (1) Understand core concepts deeply rather than memorizing — know why BFS is complete but DFS may not be; (2) Practice tracing algorithms by hand — walk through BFS/DFS on sample graphs, apply A* with given heuristics; (3) Draw diagrams — represent search trees, semantic networks, and agent architectures visually; (4) Implement key algorithms in code — programming reinforces understanding of data structures and edge cases; (5) Connect topics — understand how knowledge representation feeds into inference engines which power expert systems; (6) Work through past problems — practice applying concepts to novel scenarios; (7) Form study groups — explaining concepts to peers deepens your own understanding.",
             "topic-study-prep", "src-coursework", "exam,preparation,study,tips,strategies,review"),

            ("k-study-resources", "Recommended Study Resources for AI",
             "Recommended resources for learning Artificial Intelligence: (1) Textbooks — 'Artificial Intelligence: A Modern Approach' by Russell and Norvig (the standard reference), 'Artificial Intelligence' by Elaine Rich and Kevin Knight; (2) Online Courses — Stanford CS221 (AI principles), MIT 6.034 (AI techniques), Coursera AI specializations; (3) Practice — implement search algorithms, build a simple expert system, design knowledge representations; (4) Visualization Tools — use algorithm visualizers to understand search tree expansion, step through inference processes; (5) Community — participate in AI study groups, forums, and discussion boards; (6) Projects — apply concepts to real problems like chatbot development, game-playing agents, or recommendation systems.",
             "topic-study-prep", "src-coursework", "resources,textbook,courses,learning,books,online"),

            # Additional knowledge
            ("k-turing-test", "The Turing Test",
             "The Turing Test, proposed by Alan Turing in 1950 in his paper 'Computing Machinery and Intelligence,' is a test of a machine's ability to exhibit intelligent behavior equivalent to or indistinguishable from a human. In the test, a human evaluator engages in natural language conversations with both a human and a machine without knowing which is which. If the evaluator cannot reliably distinguish the machine from the human, the machine is said to have passed the test. The test evaluates capabilities including natural language processing, knowledge representation, automated reasoning, and machine learning. While influential, the Turing Test has been criticized for testing imitation rather than understanding — a machine could pass by clever tricks without true intelligence.",
             "topic-ai-foundations", "src-textbook", "Turing test,Alan Turing,intelligence test,imitation game"),

            ("k-search-complexity", "Search Algorithm Complexity",
             "Understanding the complexity of search algorithms is essential for choosing the right approach: Breadth-First Search has time and space complexity O(b^d); Depth-First Search has time O(b^m) and space O(b*m); Iterative Deepening has time O(b^d) and space O(b*d); Uniform-Cost Search has time and space O(b^(1+⌊C*/ε⌋)) where C* is optimal cost and ε is minimum step cost; A* has time exponential in depth but is optimally efficient (no other optimal algorithm expands fewer nodes for a given heuristic). Here, b = branching factor, d = depth of shallowest solution, m = maximum depth. The choice depends on whether you need completeness, optimality, or are constrained by memory.",
             "topic-search-bfs-dfs", "src-coursework", "complexity,time complexity,space complexity,big O,branching factor"),

            ("k-propositional-logic", "Propositional Logic",
             "Propositional Logic (also called Boolean logic or sentential logic) deals with propositions that are either true or false. Key elements: (1) Atomic propositions — simple statements (P, Q, R); (2) Connectives — AND (∧), OR (∨), NOT (¬), IMPLIES (→), BICONDITIONAL (↔); (3) Truth tables — define the semantics of connectives; (4) Inference rules — Modus Ponens (from P and P→Q, derive Q), Modus Tollens (from ¬Q and P→Q, derive ¬P), Resolution (from P∨Q and ¬P∨R, derive Q∨R). Propositional logic is decidable and has well-defined proof procedures, but it cannot express relationships between objects or use variables. First-Order Logic extends it with these capabilities.",
             "topic-predicate-logic", "src-textbook", "propositional logic,boolean,connectives,truth table,modus ponens,resolution"),

            # Unit II Search & Knowledge Innovations
            ("k-bidirectional-search", "Bidirectional Search in AI",
             "Bidirectional Search is an uninformed graph search strategy that runs two simultaneous searches: one forward from the initial state and one backward from the goal state along reversed directed edges, stopping when their search frontiers intersect. Properties: (1) In unweighted directed graphs, it finds the shortest path by edge count just like BFS, but with reduced time and space complexity O(b^(d/2)) instead of O(b^d); (2) Requires reverse-edge traversal from the goal, which requires computing predecessors in directed graphs; (3) Meeting point detection checks when a generated state exists in the opposite frontier; (4) Path reconstruction splices the forward path with the reversed backward path at the meeting node. It is widely used in route planning, puzzle solving, and knowledge-graph pathfinding.",
             "topic-bidirectional-search", "src-textbook", "bidirectional search,uninformed search,forward search,backward search,meeting point,frontier,shortest path"),

            ("k-greedy-best-first", "Greedy Best-First Search",
             "Greedy Best-First Search is an informed search algorithm that evaluates candidate nodes using solely a heuristic function h(n) which estimates the cost or semantic distance from node n to the goal. At each step, it expands the node with the lowest h(n) using a priority queue. Key properties: (1) Fast and memory-efficient in guiding the search directly toward the goal; (2) NOT guaranteed to be optimal — it does not guarantee finding the shortest path because it ignores the cost already incurred g(n); (3) Can be susceptible to false leads and local traps. It contrasts with BFS (which guarantees shortest paths on unweighted graphs) and A* (which combines g(n) and h(n) to guarantee optimality).",
             "topic-heuristic-search", "src-textbook", "greedy best-first search,heuristic,informed search,priority queue,evaluation function,h(n),best first"),

            ("k-csp-backtracking", "Constraint Satisfaction Problems (CSP) and Backtracking",
             "A Constraint Satisfaction Problem (CSP) is formulated in terms of variables X = {X1, ..., Xn}, domains D = {D1, ..., Dn} of allowable values, and constraints C = {C1, ..., Cm} specifying allowable combinations of values. A solution is a consistent, complete assignment of values to variables. Backtracking Search is the standard depth-first algorithm for CSPs: it chooses an unassigned variable, tries values from its domain, checks for constraint satisfaction, and backtracks upon encountering a conflict. In study planning, variables represent learning sessions, domains represent available time slots, and constraints enforce prerequisite precedence, daily hour limits, and student availability.",
             "topic-csp-search", "src-textbook", "constraint satisfaction,CSP,backtracking,MRV,variables,domains,constraints,scheduler,study planning"),

            ("k-neural-networks", "Neural Networks and Deep Learning",
             "Neural networks are computational models inspired by biological nervous systems, consisting of layers of interconnected artificial neurons (perceptrons). Each neuron computes a weighted sum of its inputs, adds a bias, and applies a non-linear activation function (such as ReLU, Sigmoid, or Tanh). Deep learning refers to neural networks with multiple hidden layers. Training involves forward propagation to compute predictions, loss calculation against target values, and backpropagation using gradient descent and the chain rule to update weights. Prerequisites include linear algebra, calculus, and foundational machine learning.",
             "topic-neural-networks", "src-textbook", "neural networks,deep learning,perceptrons,backpropagation,activation function,layers,weights"),

            ("k-bayesian-reasoning", "Bayesian Reasoning and Probabilistic Inference",
             "Bayesian Reasoning provides a mathematical framework for reasoning under uncertainty based on Bayes' Theorem: P(A|B) = [P(B|A) * P(A)] / P(B). It updates the prior probability of a hypothesis as new evidence is observed to compute the posterior probability. Bayesian Belief Networks (BBNs) are directed acyclic graphs representing probabilistic dependencies between random variables, where nodes represent variables and directed edges represent conditional dependencies. Inference algorithms compute posterior probability distributions given observed evidence, forming the foundation for diagnostic systems and decision theory.",
             "topic-bayesian", "src-textbook", "Bayesian reasoning,Bayes theorem,probability,probabilistic reasoning,Bayesian networks,uncertainty"),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO knowledge (id, title, content, topic_id, source_id, keywords) VALUES (?, ?, ?, ?, ?, ?)",
            knowledge,
        )

        # --- FAQ entries ---
        faqs = [
            ("faq-what-is-learnify", "What is Learnify AI?",
             "Learnify AI is an intelligent student-support chatbot that helps you explore academic knowledge related to Artificial Intelligence. It retrieves answers from a curated knowledge base and shows you exactly how it processes your questions through ProofLens — a transparent AI-execution panel. Learnify AI is a university micro-project developed to demonstrate foundational AI concepts.",
             "general", "src-demo"),

            ("faq-how-it-works", "How does Learnify AI work?",
             "Learnify AI processes your questions through a pipeline: (1) your query is normalized and analyzed; (2) the system identifies your intent using agent behavior patterns; (3) relevant knowledge is retrieved from the database using text matching; (4) a grounded response is assembled from retrieved records; (5) source references are attached. You can inspect every step in the ProofLens panel.",
             "general", "src-demo"),

            ("faq-what-topics", "What topics can Learnify AI help with?",
             "Learnify AI covers topics from a standard Artificial Intelligence curriculum: AI fundamentals, intelligent agents, search algorithms (BFS, DFS, A*), heuristic search, knowledge representation, predicate logic, forward and backward chaining, expert systems, and machine learning basics. You can also ask about study preparation strategies and recommended resources.",
             "topics", "src-demo"),

            ("faq-accuracy", "How accurate are the answers?",
             "Learnify AI retrieves answers from a curated knowledge base rather than generating text freely. When a relevant record is found, the answer is grounded in that record and the source is shown. When no relevant information is available, the system honestly tells you it doesn't have that information rather than fabricating an answer. Match scores indicate retrieval relevance, not statistical confidence.",
             "accuracy", "src-demo"),

            ("faq-institutional", "Can Learnify AI answer questions about university policies?",
             "No. Learnify AI does not have access to official university policies, attendance records, fee structures, examination dates, or scholarship information. For institutional queries, please consult your university's official website or administrative office. Any illustrative examples shown are clearly labeled as demo data.",
             "institutional", "src-demo"),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO faq (id, question, answer, category, source_id) VALUES (?, ?, ?, ?, ?)",
            faqs,
        )

        # --- Phase 3 (Hiran Antony): Declarative Policies & Reasoning Seed Data ---
        policies = [
            (
                "policy-exam-eligibility-v1",
                "Sample Examination Eligibility Policy",
                "Demonstration policy evaluating student eligibility for semester final examinations based on attendance threshold (75%) and assignment completion.",
                "1.0.0",
                1,
                "Illustrative academic policy for demonstration. This is not an official institutional eligibility decision.",
                "INELIGIBLE"
            ),
            (
                "policy-exception-waiver-v1",
                "Sample Exception Handling & Medical Waiver Policy",
                "Demonstration policy illustrating nonmonotonic reasoning: approved medical or official representation exemptions override standard attendance deficits.",
                "1.0.0",
                1,
                "Illustrative academic policy for demonstration. This is not an official institutional eligibility decision.",
                "INELIGIBLE"
            ),
            (
                "policy-incomplete-info-v1",
                "Sample Incomplete Information & Lab Clearance Policy",
                "Demonstrates truthful uncertainty handling: evaluates attendance, assignments, and required laboratory safety clearance. If safety clearance is unrecorded, the result is reported as unresolved/unknown rather than guessed.",
                "1.0.0",
                1,
                "Illustrative academic policy for demonstration. This is not an official institutional eligibility decision.",
                "INELIGIBLE"
            ),
            (
                "policy-academic-honors-v1",
                "Sample Academic Honors & Merit Recognition Policy",
                "Demonstration criteria for graduation honors: minimum GPA 3.75, completed credits >= 60, and no disciplinary violations.",
                "1.0.0",
                1,
                "Illustrative academic policy for demonstration. This is not an official institutional eligibility decision.",
                "INELIGIBLE"
            ),
        ]
        conn.executemany(
            "INSERT OR REPLACE INTO policies (id, name, description, version, is_illustrative, disclaimer, default_decision) VALUES (?, ?, ?, ?, ?, ?, ?)",
            policies,
        )

        # Declarative Rules
        rules = [
            # Policy 1: Exam Eligibility
            ("rule-exam-att-sat", "policy-exam-eligibility-v1", "Attendance Requirement Met", "Attendance reaches or exceeds 75% threshold",
             json.dumps([{"predicate": "attendance_percentage", "operator": ">=", "expected_value": 75}]),
             json.dumps({"predicate": "attendance_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-exam-att-unsat", "policy-exam-eligibility-v1", "Attendance Deficit", "Attendance below 75% threshold",
             json.dumps([{"predicate": "attendance_percentage", "operator": "<", "expected_value": 75}]),
             json.dumps({"predicate": "attendance_satisfied", "value": False}), 5, 0, None, "src-demo"),
            ("rule-exam-asgn-sat", "policy-exam-eligibility-v1", "Assignment Completion Met", "Required coursework assignments are completed",
             json.dumps([{"predicate": "assignment_completed", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "assignment_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-exam-qual-sat", "policy-exam-eligibility-v1", "Standard Examination Qualification", "Both attendance and assignment requirements are satisfied",
             json.dumps([{"predicate": "attendance_satisfied", "operator": "==", "expected_value": True}, {"predicate": "assignment_satisfied", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "eligible", "value": True}), 10, 0, None, "src-demo"),
            ("rule-exam-qual-unsat", "policy-exam-eligibility-v1", "Examination Disqualification", "Attendance requirement not satisfied",
             json.dumps([{"predicate": "attendance_satisfied", "operator": "==", "expected_value": False}]),
             json.dumps({"predicate": "eligible", "value": False}), 5, 0, None, "src-demo"),

            # Policy 2: Exception Handling & Medical Waiver
            ("rule-exc-att-sat", "policy-exception-waiver-v1", "Ordinary Attendance Met", "Attendance >= 75%",
             json.dumps([{"predicate": "attendance_percentage", "operator": ">=", "expected_value": 75}]),
             json.dumps({"predicate": "attendance_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-exc-att-unsat", "policy-exception-waiver-v1", "Ordinary Attendance Deficit", "Attendance < 75%",
             json.dumps([{"predicate": "attendance_percentage", "operator": "<", "expected_value": 75}]),
             json.dumps({"predicate": "attendance_satisfied", "value": False}), 5, 0, None, "src-demo"),
            ("rule-exc-asgn-sat", "policy-exception-waiver-v1", "Coursework Assignments Met", "Assignments completed",
             json.dumps([{"predicate": "assignment_completed", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "assignment_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-exc-std-qual", "policy-exception-waiver-v1", "Standard Examination Qualification", "Both conditions satisfied",
             json.dumps([{"predicate": "attendance_satisfied", "operator": "==", "expected_value": True}, {"predicate": "assignment_satisfied", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "eligible", "value": True}), 10, 0, None, "src-demo"),
            ("rule-exc-std-disqual", "policy-exception-waiver-v1", "Default Disqualification", "Ordinary attendance not satisfied",
             json.dumps([{"predicate": "attendance_satisfied", "operator": "==", "expected_value": False}]),
             json.dumps({"predicate": "eligible", "value": False}), 5, 0, None, "src-demo"),
            ("rule-exc-approved-override", "policy-exception-waiver-v1", "Approved Exemption Waiver Override", "Official approved exemption overrides ordinary attendance deficit",
             json.dumps([{"predicate": "approved_exemption", "operator": "==", "expected_value": True}, {"predicate": "assignment_satisfied", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "eligible", "value": True}), 50, 1, "rule-exc-std-disqual", "src-demo"),

            # Policy 3: Incomplete Information & Lab Clearance
            ("rule-inc-att", "policy-incomplete-info-v1", "Attendance Check", "Attendance >= 75%",
             json.dumps([{"predicate": "attendance_percentage", "operator": ">=", "expected_value": 75}]),
             json.dumps({"predicate": "attendance_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-inc-asgn", "policy-incomplete-info-v1", "Assignment Check", "Assignments completed",
             json.dumps([{"predicate": "assignment_completed", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "assignment_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-inc-lab", "policy-incomplete-info-v1", "Laboratory Safety Clearance", "Mandatory lab safety clearance certified",
             json.dumps([{"predicate": "lab_clearance", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "lab_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-inc-all", "policy-incomplete-info-v1", "Triple Requirement Clearance", "Attendance, assignment, and lab clearance certified",
             json.dumps([{"predicate": "attendance_satisfied", "operator": "==", "expected_value": True}, {"predicate": "assignment_satisfied", "operator": "==", "expected_value": True}, {"predicate": "lab_satisfied", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "eligible", "value": True}), 10, 0, None, "src-demo"),

            # Policy 4: Academic Honors
            ("rule-honors-gpa", "policy-academic-honors-v1", "GPA Requirement", "GPA >= 3.75",
             json.dumps([{"predicate": "gpa", "operator": ">=", "expected_value": 3.75}]),
             json.dumps({"predicate": "gpa_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-honors-credits", "policy-academic-honors-v1", "Credits Requirement", "Credits completed >= 60",
             json.dumps([{"predicate": "credits_completed", "operator": ">=", "expected_value": 60}]),
             json.dumps({"predicate": "credits_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-honors-conduct", "policy-academic-honors-v1", "Disciplinary Clearance", "No active conduct sanctions",
             json.dumps([{"predicate": "disciplinary_clearance", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "conduct_satisfied", "value": True}), 10, 0, None, "src-demo"),
            ("rule-honors-qual", "policy-academic-honors-v1", "Academic Honors Conferred", "GPA, credit, and conduct criteria satisfied",
             json.dumps([{"predicate": "gpa_satisfied", "operator": "==", "expected_value": True}, {"predicate": "credits_satisfied", "operator": "==", "expected_value": True}, {"predicate": "conduct_satisfied", "operator": "==", "expected_value": True}]),
             json.dumps({"predicate": "eligible", "value": True}), 10, 0, None, "src-demo"),
        ]
        conn.executemany(
            "INSERT OR REPLACE INTO rules (id, policy_id, name, description, conditions_json, conclusion_json, priority, is_exception, overrides_rule_id, source_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rules,
        )

        # Baseline Verified Student Facts for student_01 (Hiran Antony demonstration scenario)
        verified_facts = [
            ("fact-att-student01", "student_01", "attendance_percentage", json.dumps(["student_01"]), json.dumps(68), "src-demo", "VERIFIED", "policy-exam-eligibility-v1", "Baseline academic demo record"),
            ("fact-asgn-student01", "student_01", "assignment_completed", json.dumps(["student_01"]), json.dumps(True), "src-demo", "VERIFIED", "policy-exam-eligibility-v1", "Coursework submission record"),
            ("fact-exemp-student01", "student_01", "approved_exemption", json.dumps(["student_01"]), json.dumps(False), "src-demo", "VERIFIED", "policy-exception-waiver-v1", "Official exemption record"),
            ("fact-gpa-student01", "student_01", "gpa", json.dumps(["student_01"]), json.dumps(3.82), "src-demo", "VERIFIED", "policy-academic-honors-v1", "Academic cumulative GPA"),
            ("fact-credits-student01", "student_01", "credits_completed", json.dumps(["student_01"]), json.dumps(64), "src-demo", "VERIFIED", "policy-academic-honors-v1", "Total completed credit count"),
            ("fact-conduct-student01", "student_01", "disciplinary_clearance", json.dumps(["student_01"]), json.dumps(True), "src-demo", "VERIFIED", "policy-academic-honors-v1", "Office of Student Affairs record"),
        ]
        conn.executemany(
            "INSERT OR REPLACE INTO verified_facts (id, entity_id, predicate, arguments_json, value_json, source_id, verification_status, policy_id, context) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            verified_facts,
        )


def get_all_knowledge() -> List[Dict[str, Any]]:
    """Retrieve all knowledge records with source info."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT k.id, k.title, k.content, k.keywords, k.topic_id,
                   t.name as topic_name, t.unit,
                   s.id as source_id, s.name as source_name, s.description as source_desc
            FROM knowledge k
            LEFT JOIN topics t ON k.topic_id = t.id
            LEFT JOIN sources s ON k.source_id = s.id
            ORDER BY t.unit, k.title
        """).fetchall()
        return [dict(r) for r in rows]


def get_knowledge_by_id(kid: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single knowledge record by ID."""
    with get_db() as conn:
        row = conn.execute("""
            SELECT k.id, k.title, k.content, k.keywords, k.topic_id,
                   t.name as topic_name, t.unit,
                   s.id as source_id, s.name as source_name, s.description as source_desc
            FROM knowledge k
            LEFT JOIN topics t ON k.topic_id = t.id
            LEFT JOIN sources s ON k.source_id = s.id
            WHERE k.id = ?
        """, (kid,)).fetchone()
        return dict(row) if row else None


def get_all_faqs() -> List[Dict[str, Any]]:
    """Retrieve all FAQ entries."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT f.id, f.question, f.answer, f.category,
                   s.name as source_name
            FROM faq f
            LEFT JOIN sources s ON f.source_id = s.id
        """).fetchall()
        return [dict(r) for r in rows]


def search_knowledge(query_terms: List[str]) -> List[Dict[str, Any]]:
    """
    Search knowledge records by matching query terms against title, content, and keywords.
    Returns results sorted by relevance (number of matching terms).
    """
    if not query_terms:
        return []

    with get_db() as conn:
        all_records = conn.execute("""
            SELECT k.id, k.title, k.content, k.keywords, k.topic_id,
                   t.name as topic_name, t.unit,
                   s.id as source_id, s.name as source_name, s.description as source_desc
            FROM knowledge k
            LEFT JOIN topics t ON k.topic_id = t.id
            LEFT JOIN sources s ON k.source_id = s.id
        """).fetchall()

    results = []
    for row in all_records:
        record = dict(row)
        searchable = f"{record['title']} {record['content']} {record.get('keywords', '')}".lower()
        # Count matching terms and compute simple relevance
        matches = sum(1 for term in query_terms if term in searchable)
        if matches > 0:
            # Weight: title matches are worth more
            title_lower = record['title'].lower()
            title_matches = sum(1 for term in query_terms if term in title_lower)
            keyword_str = (record.get('keywords') or '').lower()
            keyword_matches = sum(1 for term in query_terms if term in keyword_str)
            score = (title_matches * 3.0 + keyword_matches * 2.0 + matches) / (len(query_terms) * 6.0)
            score = min(score, 1.0)
            record['relevance_score'] = round(score, 4)
            results.append(record)

    results.sort(key=lambda r: r['relevance_score'], reverse=True)
    return results


def search_faqs(query_terms: List[str]) -> List[Dict[str, Any]]:
    """Search FAQ entries by matching query terms."""
    if not query_terms:
        return []

    with get_db() as conn:
        all_faqs = conn.execute("""
            SELECT f.id, f.question, f.answer, f.category,
                   s.name as source_name
            FROM faq f
            LEFT JOIN sources s ON f.source_id = s.id
        """).fetchall()

    results = []
    for row in all_faqs:
        record = dict(row)
        searchable = f"{record['question']} {record['answer']}".lower()
        matches = sum(1 for term in query_terms if term in searchable)
        if matches > 0:
            q_matches = sum(1 for term in query_terms if term in record['question'].lower())
            score = (q_matches * 3.0 + matches) / (len(query_terms) * 4.0)
            score = min(score, 1.0)
            record['relevance_score'] = round(score, 4)
            results.append(record)

    results.sort(key=lambda r: r['relevance_score'], reverse=True)
    return results


def get_all_topics() -> List[Dict[str, Any]]:
    """
    Retrieve all topics with their prerequisites, dependents, estimated hours,
    unit, category, and metadata for graph search and PathForge.
    """
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, name, unit, description, estimated_hours, category
            FROM topics
            ORDER BY unit, name
        """).fetchall()
        topics = [dict(r) for r in rows]

        rel_rows = conn.execute("""
            SELECT parent_id, child_id, relationship
            FROM topic_relationships
        """).fetchall()

        prereqs_map: Dict[str, List[str]] = {}
        dependents_map: Dict[str, List[str]] = {}
        for r in rel_rows:
            p = r["parent_id"]
            c = r["child_id"]
            prereqs_map.setdefault(c, []).append(p)
            dependents_map.setdefault(p, []).append(c)

        for t in topics:
            t["prerequisites"] = prereqs_map.get(t["id"], [])
            t["dependents"] = dependents_map.get(t["id"], [])

        return topics


def get_topic_by_id(topic_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single topic by ID with prerequisite and dependent lists."""
    with get_db() as conn:
        row = conn.execute("""
            SELECT id, name, unit, description, estimated_hours, category
            FROM topics
            WHERE id = ?
        """, (topic_id,)).fetchone()
        if not row:
            return None
        topic = dict(row)

        prereqs = conn.execute("""
            SELECT parent_id FROM topic_relationships WHERE child_id = ?
        """, (topic_id,)).fetchall()
        topic["prerequisites"] = [r["parent_id"] for r in prereqs]

        dependents = conn.execute("""
            SELECT child_id FROM topic_relationships WHERE parent_id = ?
        """, (topic_id,)).fetchall()
        topic["dependents"] = [r["child_id"] for r in dependents]

        return topic


def get_all_topic_relationships() -> List[Dict[str, str]]:
    """Retrieve all prerequisite relationships."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT parent_id, child_id, relationship
            FROM topic_relationships
        """).fetchall()
        return [dict(r) for r in rows]


# =========================================================================
# Phase 3 (Hiran Antony): Declarative Policies, Rules & Knowledge Database Helpers
# =========================================================================

def get_all_policies() -> List[Dict[str, Any]]:
    """Retrieve all academic decision policies."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, name, description, version, is_illustrative, disclaimer, default_decision
            FROM policies
            ORDER BY id
        """).fetchall()
        policies = []
        for r in rows:
            p = dict(r)
            p["is_illustrative"] = bool(p["is_illustrative"])
            p["rules"] = get_rules_for_policy(p["id"])
            policies.append(p)
        return policies


def get_policy_by_id(policy_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single policy with its declarative rules."""
    with get_db() as conn:
        row = conn.execute("""
            SELECT id, name, description, version, is_illustrative, disclaimer, default_decision
            FROM policies
            WHERE id = ?
        """, (policy_id,)).fetchone()
        if not row:
            return None
        p = dict(row)
        p["is_illustrative"] = bool(p["is_illustrative"])
        p["rules"] = get_rules_for_policy(policy_id)
        return p


def get_rules_for_policy(policy_id: str) -> List[Dict[str, Any]]:
    """Retrieve all rules for a given policy ordered by priority descending."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, policy_id, name, description, conditions_json, conclusion_json,
                   priority, is_exception, overrides_rule_id, source_id
            FROM rules
            WHERE policy_id = ?
            ORDER BY priority DESC, id
        """, (policy_id,)).fetchall()
        rules = []
        for r in rows:
            rule_dict = dict(r)
            rule_dict["conditions"] = json.loads(rule_dict["conditions_json"])
            rule_dict["conclusion"] = json.loads(rule_dict["conclusion_json"])
            rule_dict["is_exception"] = bool(rule_dict["is_exception"])
            rules.append(rule_dict)
        return rules


def get_all_rules() -> List[Dict[str, Any]]:
    """Retrieve all declarative rules across all policies."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, policy_id, name, description, conditions_json, conclusion_json,
                   priority, is_exception, overrides_rule_id, source_id
            FROM rules
            ORDER BY policy_id, priority DESC
        """).fetchall()
        rules = []
        for r in rows:
            rule_dict = dict(r)
            rule_dict["conditions"] = json.loads(rule_dict["conditions_json"])
            rule_dict["conclusion"] = json.loads(rule_dict["conclusion_json"])
            rule_dict["is_exception"] = bool(rule_dict["is_exception"])
            rules.append(rule_dict)
        return rules


def get_verified_facts_for_entity(entity_id: str) -> List[Dict[str, Any]]:
    """Retrieve verified facts for a specific student or entity."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, entity_id, predicate, arguments_json, value_json,
                   source_id, verification_status, policy_id, context, created_at
            FROM verified_facts
            WHERE entity_id = ?
            ORDER BY created_at
        """, (entity_id,)).fetchall()
        facts = []
        for r in rows:
            f = dict(r)
            f["arguments"] = json.loads(f["arguments_json"]) if f["arguments_json"] else []
            f["value"] = json.loads(f["value_json"]) if f["value_json"] else None
            facts.append(f)
        return facts


