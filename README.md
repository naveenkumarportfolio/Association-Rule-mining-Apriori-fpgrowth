# Association Rule Mining using Apriori and FP-Growth

A Python-based **Association Rule Mining** project that analyzes e-commerce transaction data to discover frequent itemsets and meaningful relationships between categorical attributes using the **Apriori** and **FP-Growth** algorithms.

The project implements both algorithms from scratch and compares their performance based on frequent itemsets, association rules, execution time, support, confidence, and lift.

## 📌 Project Overview

Association Rule Mining is a data mining technique used to discover interesting relationships and patterns among items in a dataset.

This project applies Association Rule Mining to an e-commerce dataset containing information such as:

* Product category
* Price
* Discount
* Final price
* Payment method

The numerical attributes are converted into categorical ranges so that they can be used for transactional pattern mining.

## 🎯 Objectives

* Preprocess the e-commerce transaction dataset.
* Convert numerical attributes into categorical ranges.
* Implement the **Apriori algorithm** from scratch.
* Implement the **FP-Growth algorithm** from scratch.
* Identify frequent itemsets using a minimum support threshold.
* Generate association rules using support and confidence.
* Calculate lift for generated rules.
* Compare Apriori and FP-Growth based on execution time and results.
* Verify that both algorithms produce the same frequent itemsets.

## 📊 Dataset

The dataset contains **3,660 e-commerce transactions** and originally includes 8 columns:

* `User_ID`
* `Product_ID`
* `Category`
* `Price (Rs.)`
* `Discount (%)`
* `Final_Price(Rs.)`
* `Payment Method`
* `Purchase Date`

Since `User_ID` and `Product_ID` are unique identifiers, each purchase row is treated as an individual categorical transaction for the purpose of this project.

### Preprocessing

The numerical attributes are converted into three categories:

* **Low**
* **Medium**
* **High**

Each transaction is represented using five categorical items:

```text
Category=<value>
Payment=<value>
Price=<Price_Range>
Discount=<Discount_Range>
FinalPrice=<Final_Price_Range>
```

## 🔍 Algorithms Implemented

### 1. Apriori

The Apriori algorithm generates candidate itemsets and uses the **Apriori property** to eliminate itemsets that cannot satisfy the minimum support threshold.

The implementation includes:

* Candidate generation
* Candidate pruning
* Support counting
* Frequent itemset generation
* Association rule generation

### 2. FP-Growth

FP-Growth uses an **FP-Tree (Frequent Pattern Tree)** to mine frequent itemsets without generating large numbers of candidate itemsets.

The implementation includes:

* FP-Tree construction
* Node linking
* Conditional pattern bases
* Conditional FP-Trees
* Frequent pattern mining
* Association rule generation

## 📈 Evaluation Metrics

The following metrics are calculated for the generated association rules.

### Support

Measures how frequently an itemset occurs in the dataset.

```text
Support(X) = Number of transactions containing X / Total transactions
```

### Confidence

Measures how often the consequent occurs when the antecedent occurs.

```text
Confidence(X → Y) = Support(X ∪ Y) / Support(X)
```

### Lift

Measures the strength of the relationship between the antecedent and consequent.

```text
Lift(X → Y) = Confidence(X → Y) / Support(Y)
```

A lift value greater than 1 indicates a positive association.

## ⚙️ Parameters

| Parameter              |              Value |
| ---------------------- | -----------------: |
| Number of Transactions |              3,660 |
| Minimum Support        |                 5% |
| Minimum Confidence     |                50% |
| Algorithms             | Apriori, FP-Growth |

## 🏆 Results

Both algorithms successfully identified the same number of frequent itemsets and association rules.

| Metric            |    Apriori |  FP-Growth |
| ----------------- | ---------: | ---------: |
| Frequent Itemsets |        126 |        126 |
| Association Rules |         49 |         49 |
| Execution Time*   | 0.0515 sec | 0.0254 sec |

**Verification:**

```text
Same frequent itemsets: True
Maximum support difference: 0.000000000000
```

*Execution time may vary depending on the computer and Python environment.

## 💡 Sample Association Rules

Some of the strongest rules discovered include:

| Antecedent                                       | Consequent                 |  Support | Confidence |     Lift |
| ------------------------------------------------ | -------------------------- | -------: | ---------: | -------: |
| Discount=Discount_Low, Price=Price_High          | FinalPrice=FinalPrice_High | 0.133060 |   1.000000 | 3.002461 |
| Discount=Discount_Low, FinalPrice=FinalPrice_Low | Price=Price_Low            | 0.103005 |   1.000000 | 3.000000 |
| Discount=Discount_High, Price=Price_Low          | FinalPrice=FinalPrice_Low  | 0.078142 |   1.000000 | 3.000000 |

These rules demonstrate strong relationships between price, discount, and final price categories in the dataset.

## ⚡ Apriori vs FP-Growth

| Feature              | Apriori            | FP-Growth |
| -------------------- | ------------------ | --------- |
| Frequent Itemsets    | 126                | 126       |
| Association Rules    | 49                 | 49        |
| Candidate Generation | Yes                | No        |
| Main Structure       | Candidate Itemsets | FP-Tree   |
| Execution Time       | Higher             | Lower     |
| Result Accuracy      | Same               | Same      |

For this dataset, **FP-Growth executed faster than Apriori** while producing exactly the same frequent itemsets and association rules.

This demonstrates the advantage of FP-Growth in reducing candidate-generation overhead.

## 📁 Project Structure

```text
association-rule-mining-apriori-fpgrowth/
│
├── README.md
├── CIA2_PartA_Association_Rule_Mining.py
├── ecommerce_dataset_updated.csv
├── requirements.txt
│
├── outputs/
│   ├── algorithm_comparison.csv
│   ├── apriori_association_rules.csv
│   ├── apriori_frequent_itemsets.csv
│   ├── fpgrowth_association_rules.csv
│   ├── fpgrowth_frequent_itemsets.csv
│   ├── preprocessed_transactions.csv
│   └── verification.csv
│
└── CIA2_PartA_Final_Report.pdf
```

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Association Rule Mining**
* **Apriori**
* **FP-Growth**
* **Data Preprocessing**
* **Data Mining**

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/association-rule-mining-apriori-fpgrowth.git
```

### 2. Open the project directory

```bash
cd association-rule-mining-apriori-fpgrowth
```

### 3. Install the required libraries

```bash
python -m pip install -r requirements.txt
```

### 4. Run the project

```bash
python CIA2_PartA_Association_Rule_Mining.py
```

The generated frequent itemsets, association rules, and verification results will be saved inside the `outputs` folder.

## 📄 Output Files

The project generates the following outputs:

* `apriori_frequent_itemsets.csv` — Frequent itemsets generated using Apriori.
* `apriori_association_rules.csv` — Association rules generated using Apriori.
* `fpgrowth_frequent_itemsets.csv` — Frequent itemsets generated using FP-Growth.
* `fpgrowth_association_rules.csv` — Association rules generated using FP-Growth.
* `algorithm_comparison.csv` — Performance comparison of both algorithms.
* `preprocessed_transactions.csv` — Transactions after preprocessing.
* `verification.csv` — Verification of results between Apriori and FP-Growth.

## 🔎 Key Takeaways

* Both Apriori and FP-Growth generated **126 frequent itemsets**.
* Both algorithms generated **49 association rules**.
* The frequent itemsets generated by both algorithms were identical.
* FP-Growth required less execution time than Apriori for this dataset.
* Support, confidence, and lift provide useful measures for evaluating association rules.
* Price, discount, and final price categories showed strong associations in the discovered rules.

## 🚀 Future Improvements

Possible improvements to this project include:

* Applying the algorithms to larger transactional datasets.
* Optimizing the implementation for high-dimensional datasets.
* Adding visualizations for frequent itemsets and association rules.
* Testing different minimum support and confidence thresholds.
* Comparing the custom implementations with optimized library implementations.
* Using actual customer-level shopping baskets for more traditional market basket analysis.

## 👨‍💻 Author

**Naveen Kumar**

BBA – Finance & Marketing Analytics

This project was developed as part of an academic data mining project and is also maintained as a portfolio project demonstrating practical implementation of association rule mining algorithms in Python.
