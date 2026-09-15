"""
CIA 2 Part A - Association Rule Mining
Student: Naveen Kumar
Dataset: ecommerce_dataset_updated.csv

This script:
1. Loads and preprocesses the e-commerce dataset.
2. Converts numerical variables into categorical ranges.
3. Creates transaction records from categorical attributes.
4. Implements Apriori from scratch.
5. Implements FP-Growth from scratch.
6. Calculates support, confidence and lift for association rules.
7. Saves all outputs as CSV files.

Requirements:
    pip install pandas numpy

Run:
    python CIA2_PartA_Association_Rule_Mining.py
"""

import os
import math
import itertools
import time
from collections import Counter

import pandas as pd
import numpy as np


# ============================================================
# 1. SETTINGS
# ============================================================
DATASET = "ecommerce_dataset_updated.csv"
OUTPUT_DIR = "outputs"

MIN_SUPPORT = 0.05       # 5%
MIN_CONFIDENCE = 0.50    # 50%


# ============================================================
# 2. LOAD AND PREPROCESS DATA
# ============================================================
df = pd.read_csv(DATASET)

# Quantile-based bins convert numerical values into categorical
# variables with approximately balanced groups.
df["Price_Range"] = pd.qcut(
    df["Price (Rs.)"], q=3,
    labels=["Price_Low", "Price_Medium", "Price_High"]
).astype(str)

df["Discount_Range"] = pd.qcut(
    df["Discount (%)"], q=3,
    labels=["Discount_Low", "Discount_Medium", "Discount_High"]
).astype(str)

df["Final_Price_Range"] = pd.qcut(
    df["Final_Price(Rs.)"], q=3,
    labels=["FinalPrice_Low", "FinalPrice_Medium", "FinalPrice_High"]
).astype(str)

# Each original row is treated as one categorical transaction.
# Each transaction contains five items, one from each attribute.
transactions = [
    frozenset([
        f"Category={r.Category}",
        f"Payment={r.Payment_Method}",
        f"Price={r.Price_Range}",
        f"Discount={r.Discount_Range}",
        f"FinalPrice={r.Final_Price_Range}",
    ])
    for r in df.itertuples()
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

pd.DataFrame({
    "Transaction_ID": range(1, len(transactions) + 1),
    "Items": [" | ".join(sorted(t)) for t in transactions]
}).to_csv(
    os.path.join(OUTPUT_DIR, "preprocessed_transactions.csv"),
    index=False
)


# ============================================================
# 3. APRIORI ALGORITHM
# ============================================================
def apriori(transactions, min_support=0.05):
    """
    Find all frequent itemsets using the Apriori principle.

    Apriori principle:
    If an itemset is frequent, every non-empty subset of it
    must also be frequent.
    """
    n = len(transactions)

    # Generate frequent 1-itemsets.
    item_counts = Counter(item for t in transactions for item in t)

    frequent = {
        frozenset([item]): count / n
        for item, count in item_counts.items()
        if count / n >= min_support
    }

    all_frequent = dict(frequent)
    previous_frequent = set(frequent)
    k = 2

    while previous_frequent:
        candidates = set()
        previous_list = list(previous_frequent)

        # Candidate generation.
        for i in range(len(previous_list)):
            for j in range(i + 1, len(previous_list)):
                union = previous_list[i] | previous_list[j]

                if len(union) != k:
                    continue

                # Apriori pruning step.
                if all(
                    frozenset(subset) in previous_frequent
                    for subset in itertools.combinations(union, k - 1)
                ):
                    candidates.add(union)

        # Count candidate supports.
        candidate_counts = Counter()

        for transaction in transactions:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    candidate_counts[candidate] += 1

        # Keep only candidates meeting minimum support.
        current_frequent = {
            candidate: count / n
            for candidate, count in candidate_counts.items()
            if count / n >= min_support
        }

        all_frequent.update(current_frequent)
        previous_frequent = set(current_frequent)
        k += 1

    return all_frequent


# ============================================================
# 4. SUPPORT, CONFIDENCE AND LIFT
# ============================================================
def generate_rules(frequent_itemsets, min_confidence=0.50):
    """
    Generate association rules from frequent itemsets.

    Support(X -> Y) = support(X union Y)
    Confidence(X -> Y) = support(X union Y) / support(X)
    Lift(X -> Y) = confidence(X -> Y) / support(Y)
    """
    rules = []

    for itemset, support in frequent_itemsets.items():

        if len(itemset) < 2:
            continue

        items = list(itemset)

        # Every non-empty proper subset can be an antecedent.
        for size in range(1, len(items)):
            for antecedent_tuple in itertools.combinations(items, size):

                antecedent = frozenset(antecedent_tuple)
                consequent = itemset - antecedent

                antecedent_support = frequent_itemsets.get(antecedent)
                consequent_support = frequent_itemsets.get(consequent)

                if antecedent_support is None or consequent_support is None:
                    continue

                confidence = support / antecedent_support

                if confidence >= min_confidence:
                    lift = confidence / consequent_support

                    rules.append({
                        "Antecedent": ", ".join(sorted(antecedent)),
                        "Consequent": ", ".join(sorted(consequent)),
                        "Support": support,
                        "Confidence": confidence,
                        "Lift": lift
                    })

    return pd.DataFrame(rules).sort_values(
        ["Confidence", "Support"],
        ascending=[False, False]
    ).reset_index(drop=True)


# ============================================================
# 5. FP-GROWTH DATA STRUCTURES
# ============================================================
class FPNode:
    """Node used in the FP-tree."""

    def __init__(self, item=None, count=0, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None


def build_fp_tree(transactions, min_count):
    """Build an FP-tree and header table."""

    counts = Counter(item for t in transactions for item in t)

    # Remove items below minimum support.
    frequent_items = {
        item: count
        for item, count in counts.items()
        if count >= min_count
    }

    if not frequent_items:
        return None, frequent_items

    root = FPNode()
    header = {
        item: [frequent_items[item], None]
        for item in frequent_items
    }

    for transaction in transactions:

        # Sort items by descending global frequency.
        ordered_items = sorted(
            [item for item in transaction if item in frequent_items],
            key=lambda item: (-frequent_items[item], item)
        )

        current = root

        for item in ordered_items:

            if item in current.children:
                child = current.children[item]
                child.count += 1

            else:
                child = FPNode(
                    item=item,
                    count=1,
                    parent=current
                )
                current.children[item] = child

                # Link nodes containing the same item.
                if header[item][1] is None:
                    header[item][1] = child
                else:
                    node = header[item][1]

                    while node.link is not None:
                        node = node.link

                    node.link = child

            current = child

    return root, header


# ============================================================
# 6. FP-GROWTH ALGORITHM
# ============================================================
def fp_growth(transactions, min_support=0.05):
    """
    Mine all frequent itemsets using FP-Growth.

    FP-Growth compresses the transaction database into an FP-tree
    and mines conditional pattern bases instead of generating
    large candidate sets like Apriori.
    """

    total_transactions = len(transactions)
    min_count = math.ceil(min_support * total_transactions)

    result = {}

    def mine(transaction_list, suffix, minimum_count):

        root, header = build_fp_tree(
            transaction_list,
            minimum_count
        )

        if root is None:
            return

        # Start from least frequent header items.
        items = sorted(
            header,
            key=lambda item: (header[item][0], item)
        )

        for item in items:

            new_pattern = frozenset(
                set(suffix) | {item}
            )

            result[new_pattern] = (
                header[item][0] / total_transactions
            )

            # Construct the conditional pattern base.
            conditional_base = []

            node = header[item][1]

            while node is not None:

                path = []
                parent = node.parent

                while parent is not None and parent.item is not None:
                    path.append(parent.item)
                    parent = parent.parent

                if path:
                    conditional_base.extend(
                        [path] * node.count
                    )

                node = node.link

            if conditional_base:

                conditional_transactions = [
                    frozenset(path)
                    for path in conditional_base
                ]

                mine(
                    conditional_transactions,
                    new_pattern,
                    minimum_count
                )

    mine(
        transactions,
        frozenset(),
        min_count
    )

    return result


# ============================================================
# 7. OUTPUT HELPERS
# ============================================================
def itemsets_to_dataframe(itemsets):
    rows = []

    for itemset, support in itemsets.items():
        rows.append({
            "Itemset": ", ".join(sorted(itemset)),
            "Itemset_Size": len(itemset),
            "Support": support
        })

    return pd.DataFrame(rows).sort_values(
        ["Itemset_Size", "Support", "Itemset"],
        ascending=[True, False, True]
    ).reset_index(drop=True)


# ============================================================
# 8. RUN APRIORI
# ============================================================
print("\n=== CIA 2 PART A: ASSOCIATION RULE MINING ===")
print(f"Transactions: {len(transactions)}")
print(f"Minimum support: {MIN_SUPPORT:.0%}")
print(f"Minimum confidence: {MIN_CONFIDENCE:.0%}")

start = time.perf_counter()
apriori_frequent = apriori(
    transactions,
    MIN_SUPPORT
)
apriori_time = time.perf_counter() - start

apriori_itemsets = itemsets_to_dataframe(
    apriori_frequent
)

apriori_rules = generate_rules(
    apriori_frequent,
    MIN_CONFIDENCE
)

apriori_itemsets.to_csv(
    os.path.join(OUTPUT_DIR, "apriori_frequent_itemsets.csv"),
    index=False
)

apriori_rules.to_csv(
    os.path.join(OUTPUT_DIR, "apriori_association_rules.csv"),
    index=False
)

print(f"\nApriori frequent itemsets: {len(apriori_frequent)}")
print(f"Apriori rules: {len(apriori_rules)}")
print(f"Apriori execution time: {apriori_time:.6f} seconds")


# ============================================================
# 9. RUN FP-GROWTH
# ============================================================
start = time.perf_counter()
fpgrowth_frequent = fp_growth(
    transactions,
    MIN_SUPPORT
)
fpgrowth_time = time.perf_counter() - start

fpgrowth_itemsets = itemsets_to_dataframe(
    fpgrowth_frequent
)

fpgrowth_rules = generate_rules(
    fpgrowth_frequent,
    MIN_CONFIDENCE
)

fpgrowth_itemsets.to_csv(
    os.path.join(OUTPUT_DIR, "fpgrowth_frequent_itemsets.csv"),
    index=False
)

fpgrowth_rules.to_csv(
    os.path.join(OUTPUT_DIR, "fpgrowth_association_rules.csv"),
    index=False
)

print(f"\nFP-Growth frequent itemsets: {len(fpgrowth_frequent)}")
print(f"FP-Growth rules: {len(fpgrowth_rules)}")
print(f"FP-Growth execution time: {fpgrowth_time:.6f} seconds")


# ============================================================
# 10. VERIFY RESULTS AND COMPARE ALGORITHMS
# ============================================================
same_itemsets = (
    set(apriori_frequent.keys())
    == set(fpgrowth_frequent.keys())
)

max_support_difference = max(
    abs(apriori_frequent[k] - fpgrowth_frequent[k])
    for k in apriori_frequent
)

comparison = pd.DataFrame([
    {
        "Algorithm": "Apriori",
        "Frequent_Itemsets": len(apriori_frequent),
        "Association_Rules": len(apriori_rules),
        "Execution_Time_Seconds": apriori_time
    },
    {
        "Algorithm": "FP-Growth",
        "Frequent_Itemsets": len(fpgrowth_frequent),
        "Association_Rules": len(fpgrowth_rules),
        "Execution_Time_Seconds": fpgrowth_time
    }
])

comparison.to_csv(
    os.path.join(OUTPUT_DIR, "algorithm_comparison.csv"),
    index=False
)

verification = pd.DataFrame([{
    "Same_Frequent_Itemsets": same_itemsets,
    "Maximum_Support_Difference": max_support_difference
}])

verification.to_csv(
    os.path.join(OUTPUT_DIR, "verification.csv"),
    index=False
)

print("\n=== VERIFICATION ===")
print(f"Same frequent itemsets: {same_itemsets}")
print(
    "Maximum support difference:",
    f"{max_support_difference:.12f}"
)

print("\n=== TOP APRIORI RULES ===")
print(apriori_rules.head(10).to_string(index=False))

print("\n=== TOP FP-GROWTH RULES ===")
print(fpgrowth_rules.head(10).to_string(index=False))

print("\nAll output files have been saved in the 'outputs' folder.")
