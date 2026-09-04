"""
ExamHub Comprehensive Multi-Disciplinary Question Bank Fixtures
Provides extensive authentic calibrated question items across Computer Science,
Mathematics, Electrical Engineering, and Information Security for test creation.
"""

from typing import List, Dict, Any

EXTENDED_STEM_QUESTION_FIXTURES: List[Dict[str, Any]] = [
    # -------------------------------------------------------------
    # 1. ALGORITHMS & DATA STRUCTURES
    # -------------------------------------------------------------
    {
        "id": "CS-ALG-001",
        "domain": "Algorithms & Data Structures",
        "topic": "Asymptotic Complexity",
        "bloom_level": "ANALYZE",
        "difficulty_b": -0.42,
        "discrimination_a": 1.45,
        "guessing_c": 0.25,
        "prompt": "Consider the recurrence relation T(n) = 4T(n/2) + n^2. According to the Master Theorem, what is the tight asymptotic bound for T(n)?",
        "options": [
            "Theta(n^2)",
            "Theta(n^2 log n)",
            "Theta(n^3)",
            "Theta(2^n)"
        ],
        "correct_index": 1,
        "explanation": "Here a = 4, b = 2, and f(n) = n^2. Log_b(a) = log_2(4) = 2. Since f(n) = Theta(n^(log_b a)) = Theta(n^2), Case 2 of the Master Theorem applies, yielding T(n) = Theta(n^2 log n)."
    },
    {
        "id": "CS-ALG-002",
        "domain": "Algorithms & Data Structures",
        "topic": "Self-Balancing Trees",
        "bloom_level": "APPLY",
        "difficulty_b": 0.28,
        "discrimination_a": 1.62,
        "guessing_c": 0.25,
        "prompt": "In an AVL tree with balance factor defined as height(left) - height(right), inserting a key causes a node to have a balance factor of +2 and its left child has a balance factor of -1. Which rotation sequence restores AVL balance?",
        "options": [
            "Single Right Rotation (LL)",
            "Single Left Rotation (RR)",
            "Left-Right Double Rotation (LR)",
            "Right-Left Double Rotation (RL)"
        ],
        "correct_index": 2,
        "explanation": "A balance factor of +2 at the grandparent followed by -1 at the left child indicates an LR imbalance, which requires a Left rotation on the child followed by a Right rotation on the grandparent."
    },
    {
        "id": "CS-ALG-003",
        "domain": "Algorithms & Data Structures",
        "topic": "Graph Algorithms",
        "bloom_level": "EVALUATE",
        "difficulty_b": 0.85,
        "discrimination_a": 1.80,
        "guessing_c": 0.25,
        "prompt": "Which shortest path algorithm correctly handles directed graphs with negative edge weights and detects negative weight cycles in O(V * E) time?",
        "options": [
            "Dijkstra's Algorithm with Fibonacci Heap",
            "Bellman-Ford Algorithm",
            "Floyd-Warshall Algorithm",
            "Johnson's Algorithm"
        ],
        "correct_index": 1,
        "explanation": "The Bellman-Ford algorithm relaxes all edges V-1 times and detects negative cycles on a V-th relaxation in O(V * E) time. Dijkstra fails on negative edge weights."
    },
    {
        "id": "CS-ALG-004",
        "domain": "Algorithms & Data Structures",
        "topic": "Dynamic Programming",
        "bloom_level": "CREATE",
        "difficulty_b": 1.15,
        "discrimination_a": 1.95,
        "guessing_c": 0.25,
        "prompt": "In the 0/1 Knapsack problem with n items and maximum weight capacity W, what is the worst-case space complexity of the standard space-optimized 1D dynamic programming table?",
        "options": [
            "O(n * W)",
            "O(W)",
            "O(n)",
            "O(log W)"
        ],
        "correct_index": 1,
        "explanation": "By iterating weight backwards from W down to item weight w_i, the 2D DP table can be compressed into a single 1D array of length W + 1, requiring O(W) auxiliary space."
    },
    {
        "id": "CS-ALG-005",
        "domain": "Algorithms & Data Structures",
        "topic": "Disjoint Set Union",
        "bloom_level": "ANALYZE",
        "difficulty_b": 0.65,
        "discrimination_a": 1.70,
        "guessing_c": 0.25,
        "prompt": "When both Union by Rank and Path Compression heuristics are employed in a Disjoint Set Union (DSU) structure, what is the amortized time complexity per find/union operation for m operations on n elements?",
        "options": [
            "O(log n)",
            "O(1)",
            "O(alpha(n)) where alpha is the Inverse Ackermann function",
            "O(sqrt(n))"
        ],
        "correct_index": 2,
        "explanation": "Tarjan (1975) established that combining rank pairing with full path compression yields an amortized bound of O(alpha(n)), effectively constant for all practical n."
    },

    # -------------------------------------------------------------
    # 2. COMPUTER SYSTEMS & OPERATING SYSTEMS
    # -------------------------------------------------------------
    {
        "id": "CS-OS-001",
        "domain": "Operating Systems",
        "topic": "Virtual Memory & Paging",
        "bloom_level": "UNDERSTAND",
        "difficulty_b": -0.65,
        "discrimination_a": 1.30,
        "guessing_c": 0.25,
        "prompt": "In a 32-bit virtual memory architecture with 4 KB page size, how many total entries exist in a conventional flat single-level page table?",
        "options": [
            "1,048,576 (2^20) entries",
            "4,096 (2^12) entries",
            "65,536 (2^16) entries",
            "4,294,967,296 (2^32) entries"
        ],
        "correct_index": 0,
        "explanation": "Page size 4 KB = 2^12 bytes, requiring 12 offset bits. The remaining 32 - 12 = 20 bits index virtual pages, resulting in 2^20 = 1,048,576 page table entries."
    },
    {
        "id": "CS-OS-002",
        "domain": "Operating Systems",
        "topic": "Concurrency & Deadlocks",
        "bloom_level": "ANALYZE",
        "difficulty_b": 0.35,
        "discrimination_a": 1.55,
        "guessing_c": 0.25,
        "prompt": "Which of Coffman's four deadlock conditions is directly eliminated by acquiring all required locks in a globally defined total order?",
        "options": [
            "Mutual Exclusion",
            "Hold and Wait",
            "No Preemption",
            "Circular Wait"
        ],
        "correct_index": 3,
        "explanation": "Imposing a strict total ordering on lock acquisition guarantees an acyclic resource allocation graph, directly preventing Circular Wait."
    },
    {
        "id": "CS-OS-003",
        "domain": "Operating Systems",
        "topic": "CPU Scheduling",
        "bloom_level": "EVALUATE",
        "difficulty_b": 0.45,
        "discrimination_a": 1.40,
        "guessing_c": 0.25,
        "prompt": "In Linux Completely Fair Scheduler (CFS), which data structure is used to track runnable tasks ordered by their accumulated virtual runtime (vruntime)?",
        "options": [
            "Fibonacci Heap",
            "Red-Black Tree",
            "Circular Ring Buffer",
            "Multi-level Priority Array"
        ],
        "correct_index": 1,
        "explanation": "Linux CFS tracks runnable tasks using a self-balancing Red-Black Tree where the leftmost node corresponds to the process with minimum vruntime (O(1) cached pick, O(log N) re-insertion)."
    },
    {
        "id": "CS-OS-004",
        "domain": "Operating Systems",
        "topic": "TLB & Memory Management",
        "bloom_level": "ANALYZE",
        "difficulty_b": 0.95,
        "discrimination_a": 1.75,
        "guessing_c": 0.25,
        "prompt": "What phenomenon occurs when the working set of multiple active processes exceeds the physical capacity of the Translation Lookaside Buffer (TLB) and page frames, resulting in continuous disk page faults and near-zero CPU throughput?",
        "options": [
            "Convoy Effect",
            "Priority Inversion",
            "Thrashing",
            "Belady's Anomaly"
        ],
        "correct_index": 2,
        "explanation": "Thrashing describes the operational state where the system spends significantly more time swapping virtual pages to and from secondary storage than executing user instructions."
    },

    # -------------------------------------------------------------
    # 3. DATABASE SYSTEMS & DATA ENGINEERING
    # -------------------------------------------------------------
    {
        "id": "CS-DB-001",
        "domain": "Database Systems",
        "topic": "Transaction Isolation Levels",
        "bloom_level": "EVALUATE",
        "difficulty_b": 0.55,
        "discrimination_a": 1.65,
        "guessing_c": 0.25,
        "prompt": "Which concurrency phenomenon involves a transaction T1 reading a set of rows satisfying a search predicate, while T2 inserts a new row satisfying the predicate and commits, causing T1 to observe a different count upon re-executing the query?",
        "options": [
            "Dirty Read",
            "Non-Repeatable Read (Fuzzy Read)",
            "Phantom Read",
            "Lost Update"
        ],
        "correct_index": 2,
        "explanation": "A Phantom Read occurs when a range query executed multiple times within a transaction yields different result sets due to concurrent insertions/deletions matching the search condition."
    },
    {
        "id": "CS-DB-002",
        "domain": "Database Systems",
        "topic": "Indexing & Storage Engines",
        "bloom_level": "ANALYZE",
        "difficulty_b": 0.70,
        "discrimination_a": 1.50,
        "guessing_c": 0.25,
        "prompt": "Why are Log-Structured Merge-trees (LSM-trees) frequently preferred over classical B+ Trees in write-heavy distributed storage engines (e.g. RocksDB, Cassandra)?",
        "options": [
            "LSM-trees provide faster point read latency for non-cached keys",
            "LSM-trees convert random write disk I/O into sequential append-only disk writes",
            "LSM-trees eliminate the need for write-ahead logging (WAL)",
            "LSM-trees require zero background compaction overhead"
        ],
        "correct_index": 1,
        "explanation": "LSM-trees buffer writes in an in-memory memtable and flush sequentially to immutable SSTables on disk, replacing expensive random page overwrites with high-throughput sequential writes."
    },
    {
        "id": "CS-DB-003",
        "domain": "Database Systems",
        "topic": "Relational Normalization",
        "bloom_level": "APPLY",
        "difficulty_b": 0.15,
        "discrimination_a": 1.35,
        "guessing_c": 0.25,
        "prompt": "A relational schema R(A, B, C) has functional dependencies A -> B and B -> C. In which normal form is this relation, and why does it violate Boyce-Codd Normal Form (BCNF)?",
        "options": [
            "1NF only; has repeating attribute groups",
            "2NF; contains a transitive functional dependency A -> C via B",
            "3NF; B is a candidate key",
            "BCNF; all determinants are superkeys"
        ],
        "correct_index": 1,
        "explanation": "The primary key is A. A -> B and B -> C creates a transitive dependency A -> C. Because B is not a candidate key, it is in 2NF and violates 3NF and BCNF."
    },

    # -------------------------------------------------------------
    # 4. COMPUTER NETWORKS & DISTRIBUTED SYSTEMS
    # -------------------------------------------------------------
    {
        "id": "CS-NET-001",
        "domain": "Computer Networks",
        "topic": "Transport Layer Congestion Control",
        "bloom_level": "UNDERSTAND",
        "difficulty_b": -0.25,
        "discrimination_a": 1.40,
        "guessing_c": 0.25,
        "prompt": "In TCP Reno congestion control, upon receiving three duplicate acknowledgments (3 dup ACKs), what action does the sender take?",
        "options": [
            "Reset congestion window (cwnd) to 1 MSS and enter Slow Start",
            "Halve ssthresh, set cwnd = ssthresh + 3 MSS, and enter Fast Recovery",
            "Double the congestion window and increase retransmission timeout (RTO)",
            "Immediately terminate the TCP connection with an RST packet"
        ],
        "correct_index": 1,
        "explanation": "Three duplicate ACKs indicate packet loss without complete network collapse. TCP Reno executes Fast Retransmit and Fast Recovery: ssthresh is halved and cwnd is reduced to ssthresh + 3 MSS without dropping to 1 MSS."
    },
    {
        "id": "CS-NET-002",
        "domain": "Distributed Systems",
        "topic": "Consensus & Quorums",
        "bloom_level": "EVALUATE",
        "difficulty_b": 1.05,
        "discrimination_a": 1.85,
        "guessing_c": 0.25,
        "prompt": "In a distributed Raft cluster consisting of 7 nodes, what is the minimum quorum size required to elect a leader and commit a log entry, and how many simultaneous node crashes can the cluster tolerate?",
        "options": [
            "Quorum = 4, Fault tolerance = 3 node crashes",
            "Quorum = 5, Fault tolerance = 2 node crashes",
            "Quorum = 3, Fault tolerance = 4 node crashes",
            "Quorum = 6, Fault tolerance = 1 node crash"
        ],
        "correct_index": 0,
        "explanation": "For N = 7, the majority quorum is ⌊7/2⌋ + 1 = 4 nodes. A consensus cluster tolerates F failures where N = 2F + 1; for N = 7, F = 3."
    },
    {
        "id": "CS-NET-003",
        "domain": "Distributed Systems",
        "topic": "Logical Clocks & Causality",
        "bloom_level": "ANALYZE",
        "difficulty_b": 0.80,
        "discrimination_a": 1.60,
        "guessing_c": 0.25,
        "prompt": "Why are Vector Clocks necessary to establish causality in asynchronous distributed systems when Lamport Timestamps are insufficient?",
        "options": [
            "Lamport timestamps cannot distinguish between causally dependent and concurrent events",
            "Lamport timestamps require synchronized atomic hardware clocks",
            "Vector clocks guarantee bounded message overhead regardless of node count",
            "Lamport timestamps cannot guarantee total ordering of events"
        ],
        "correct_index": 0,
        "explanation": "With Lamport timestamps, if event a causes event b, then L(a) < L(b), but L(a) < L(b) does NOT imply a caused b. Vector Clocks provide an exact isomorphism: V(a) < V(b) if and only if a causally precedes b."
    },

    # -------------------------------------------------------------
    # 5. CRYPTOGRAPHY & SECURITY
    # -------------------------------------------------------------
    {
        "id": "CS-SEC-001",
        "domain": "Applied Cryptography",
        "topic": "Authenticated Encryption",
        "bloom_level": "ANALYZE",
        "difficulty_b": 0.60,
        "discrimination_a": 1.65,
        "guessing_c": 0.25,
        "prompt": "What critical security vulnerability is introduced if an initialization vector (IV) or nonce is reused with the same key in AES-GCM (Galois/Counter Mode)?",
        "options": [
            "The secret key can be extracted through algebraic linear cryptanalysis",
            "The GHASH authentication key (H) can be recovered, allowing arbitrary ciphertext forgery",
            "The block cipher immediately reverts to ECB mode",
            "No vulnerability is introduced as long as the plaintext length is odd"
        ],
        "correct_index": 1,
        "explanation": "AES-GCM nonce reuse reveals the XOR of plaintexts and allows an adversary to solve a polynomial equation over GF(2^128) to extract the GHASH authentication key H, destroying message authenticity and enabling forged packets."
    },
    {
        "id": "CS-SEC-002",
        "domain": "Applied Cryptography",
        "topic": "Public Key Cryptography",
        "bloom_level": "APPLY",
        "difficulty_b": 0.40,
        "discrimination_a": 1.50,
        "guessing_c": 0.25,
        "prompt": "In an RSA public-key cryptosystem with prime factors p = 11 and q = 13, what is Euler's totient function phi(n), and which of the following is a valid public encryption exponent e?",
        "options": [
            "phi(n) = 143, e = 11",
            "phi(n) = 120, e = 7",
            "phi(n) = 120, e = 15",
            "phi(n) = 24, e = 5"
        ],
        "correct_index": 1,
        "explanation": "phi(n) = (p - 1)(q - 1) = (10)(12) = 120. A valid public exponent e must satisfy 1 < e < 120 and gcd(e, 120) = 1. For e = 7: gcd(7, 120) = 1 (coprime), making it valid."
    }
]


def get_all_fixture_questions() -> List[Dict[str, Any]]:
    return EXTENDED_STEM_QUESTION_FIXTURES
