# CIA 2 Part A — Association Rule Mining

**Student:** Naveen Kumar  
**Topic:** Apriori vs FP-Growth  
**Dataset:** `ecommerce_dataset_updated.csv`

## Project files
- `ecommerce_dataset_updated.csv` — dataset used
- `CIA2_PartA_Association_Rule_Mining.py` — complete commented implementation
- `requirements.txt` — Python packages
- `outputs/` — frequent itemsets, rules, comparison and verification

## Parameters
- Minimum support: 5%
- Minimum confidence: 50%

## Important preprocessing decision
The supplied dataset contains 3,660 purchase rows, with a unique User_ID and Product_ID for each row. Therefore, using User_ID as a basket would produce one-item baskets and would not be useful for association rules. Instead, each purchase row is treated as one categorical transaction containing:
1. Category
2. Payment Method
3. Price Range
4. Discount Range
5. Final Price Range

Numerical values are converted into three quantile-based categories (Low, Medium, High). This makes the data appropriate for categorical association-rule mining.

## How to run
Open this folder in VS Code and run:

```bash
python -m pip install -r requirements.txt
python CIA2_PartA_Association_Rule_Mining.py
```

If `python` is not recognized on Windows, try:

```bash
py -m pip install -r requirements.txt
py CIA2_PartA_Association_Rule_Mining.py
```

The program creates/updates the `outputs` folder.

## Verification
Apriori and FP-Growth are expected to produce exactly the same frequent itemsets and support values when the same minimum-support threshold is used. Their internal approaches are different, but the mathematical result should agree.
