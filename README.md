# Association Rule Mining: Apriori & FP-Growth

A Python-based data mining project that discovers frequent itemsets and association rules from e-commerce transaction data using **Apriori** and **FP-Growth** algorithms implemented from scratch.

The project demonstrates the complete association rule mining workflow, including data preprocessing, frequent itemset generation, support and confidence calculation, association rule generation, and algorithm comparison.

---

## Project Overview

Association Rule Mining is a data mining technique used to discover relationships and recurring patterns among items or attributes in transactional data.

This project applies two classical frequent itemset mining algorithms:

* **Apriori**
* **FP-Growth**

Both algorithms are implemented from scratch in Python and evaluated using the same dataset and minimum thresholds.

The project also calculates:

* Support
* Confidence
* Lift

and compares the frequent itemsets and execution performance produced by both algorithms.

---

## Objectives

The main objectives of this project are to:

1. Preprocess e-commerce transaction data for association rule mining.
2. Generate frequent itemsets using the Apriori algorithm.
3. Generate association rules using support, confidence, and lift.
4. Generate frequent itemsets using the FP-Growth algorithm.
5. Compare the results produced by Apriori and FP-Growth.
6. Verify that both algorithms generate consistent frequent itemsets.

---

## Dataset

The project uses an e-commerce dataset containing **3,660 transactions**.

The original dataset contains attributes related to:

* Product category
* Payment method
* Product price
* Discount
* Final price

For association rule mining, the numerical attributes were transformed into categorical ranges.

### Preprocessing

The following numerical attributes were converted into three categories using quantile-based binning:

* `Price (Rs.)` → Low / Medium / High
* `Discount (%)` → Low / Medium / High
* `Final_Price(Rs.)` → Low / Medium / High

Each transaction was then represented using categorical items such as:

```text
Category=Electronics
Payment=Credit Card
Price=Price_High
Discount=Discount_Low
FinalPrice=FinalPrice_High
```

This preprocessing allows the data to be represented in a transaction format suitable for frequent itemset mining.

---

## Algorithms

### Apriori

Apriori is a candidate-generation based frequent itemset mining algorithm.

The implementation:

1. Finds frequent 1-itemsets.
2. Generates candidate itemsets.
3. Applies the Apriori pruning principle.
4. Calculates support.
5. Retains itemsets satisfying the minimum support threshold.
6. Repeats the process for larger itemsets.

The implementation was developed without using a pre-built association rule mining library.

---

### FP-Growth

FP-Growth uses an **FP-tree** structure to mine frequent itemsets without repeatedly generating large candidate sets.

The implementation includes:

* FP-tree construction
* Header table
* Node linking
* Conditional pattern bases
* Recursive FP-tree mining

This provides an alternative approach to the candidate-generation strategy used by Apriori.

---

## Association Rules

Association rules are generated from frequent itemsets using:

### Support

Support measures how frequently an itemset occurs in the complete dataset.

```text
Support(X) = Transactions containing X / Total Transactions
```

### Confidence

Confidence measures how often the consequent occurs when the antecedent occurs.

```text
Confidence(X → Y) = Support(X ∪ Y) / Support(X)
```

### Lift

Lift measures the strength of association between the antecedent and consequent.

```text
Lift(X → Y) = Confidence(X → Y) / Support(Y)
```

A lift value greater than 1 indicates a positive association.

---

## Parameters

The following thresholds were used:

| Parameter          | Value |
| ------------------ | ----: |
| Minimum Support    |    5% |
| Minimum Confidence |   50% |

These thresholds were applied consistently to both Apriori and FP-Growth.

---

## Results

Both algorithms produced consistent results on the dataset.

| Metric                  | Apriori | FP-Growth |
| ----------------------- | ------: | --------: |
| Frequent Itemsets       |     126 |       126 |
| Association Rules       |      49 |        49 |
| Maximum Itemset Size    |       3 |         3 |
| Frequent Itemsets Match |     Yes |       Yes |

The verification process confirmed that both algorithms generated the same frequent itemsets and matching support values.

### Execution Performance

In the tested execution environment:

* Apriori execution time: approximately **0.052 seconds**
* FP-Growth execution time: approximately **0.025 seconds**

FP-Growth completed faster in this particular run.

Execution time can vary depending on the hardware, Python environment, and system load, so the timing should be treated as an experimental observation rather than a general benchmark.

---

## Example Association Rules

Some of the strongest discovered rules include relationships such as:

```text
Discount=Discount_Low, Price=Price_High
→ FinalPrice=FinalPrice_High
```

with:

* Support ≈ 13.31%
* Confidence = 100%
* Lift ≈ 3.00

Another example:

```text
Discount=Discount_Low, FinalPrice=FinalPrice_Low
→ Price=Price_Low
```

with:

* Support ≈ 10.30%
* Confidence = 100%
* Lift ≈ 3.00

These rules demonstrate strong relationships between price, discount, and final price categories within the dataset.

---

## Apriori vs FP-Growth

| Aspect               | Apriori                                  | FP-Growth                        |
| -------------------- | ---------------------------------------- | -------------------------------- |
| Approach             | Candidate generation                     | FP-tree                          |
| Candidate generation | Yes                                      | No                               |
| Data scanning        | Multiple scans                           | More efficient tree-based mining |
| Implementation       | Relatively simple                        | More complex                     |
| Scalability          | Can become expensive with large datasets | Generally more scalable          |
| Result               | 126 frequent itemsets                    | 126 frequent itemsets            |

### Key Observation

Both algorithms produced identical frequent itemsets under the same minimum support threshold.

The main difference is **how they discover those itemsets**.

Apriori explicitly generates and evaluates candidate itemsets, while FP-Growth compresses the transaction database into an FP-tree and mines the tree recursively.

For larger or denser datasets, FP-Growth can generally provide better scalability by avoiding extensive candidate generation.

---

## Project Structure

```text
association-rule-mining-apriori-fpgrowth/
│
├── CIA2_PartA_Association_Rule_Mining.py
├── ecommerce_dataset_updated.csv
├── requirements.txt
├── README.md
│
└── outputs/
    ├── algorithm_comparison.csv
    ├── apriori_association_rules.csv
    ├── apriori_frequent_itemsets.csv
    ├── fpgrowth_association_rules.csv
    ├── fpgrowth_frequent_itemsets.csv
    ├── preprocessed_transactions.csv
    └── verification.csv
```

---

## Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Apriori**
* **FP-Growth**
* **Association Rule Mining**
* **Data Preprocessing**

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/association-rule-mining-apriori-fpgrowth.git
```

### 2. Navigate to the project

```bash
cd association-rule-mining-apriori-fpgrowth
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the project

```bash
python CIA2_PartA_Association_Rule_Mining.py
```

The generated frequent itemsets, association rules, and comparison results will be saved in the `outputs` directory.

---

## Key Takeaways

This project demonstrates practical understanding of:

* Transactional data preprocessing
* Frequent itemset mining
* Apriori candidate generation and pruning
* FP-tree construction
* FP-Growth mining
* Support and confidence
* Lift-based association analysis
* Algorithm validation
* Performance comparison

---

## Limitations

The dataset is not a conventional product-level market basket dataset. Instead, each purchase record is treated as a transaction containing categorical purchase attributes.

Therefore, the discovered rules represent relationships between attributes such as price, discount, payment method, category, and final price rather than relationships between individual products.

---

## Future Improvements

Possible extensions include:

* Applying the algorithms to larger transaction datasets
* Using product-level basket data
* Adding interactive visualizations
* Comparing additional association rule mining algorithms
* Experimenting with different support and confidence thresholds
* Building a recommendation system using discovered rules
* Creating a Streamlit dashboard for interactive exploration

---

## Author

**Naveen Kumar**

BBA – Finance & Marketing Analytics

This project demonstrates practical implementation and understanding of association rule mining algorithms using Python.
