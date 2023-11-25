# FinanceAnalyzer

A simple script to aid in personal finance by providing a tabular display of expenses, income, and profit over time.

To run the script:
`python Analyzer.py`

## Recording expenses and income

Place the following two files in the same directory as this repository:

- ExpenseData.txt
- IncomeData.txt

Each line represents an expense or source of income with the following format:

Format:
`mm/dd/yr, Name, amount`

Example:
`11/23/23, Charity, $50`

## Output

```
2022 Financial Report
Month      Expense ($)    Income ($)  Profit ($)
-------  -------------  ------------  ------------
6               282.5           0     (282.50)
7               280.01          0     (280.01)
8               275.91       1755.89  1479.98
9               368.15        962.8   594.65
10             1358.03       1462.8   104.77
11              383.47       1537.8   1154.33
12             1313.23       2169.2   855.97
Total          4261.3        7888.49  3627.19
```
