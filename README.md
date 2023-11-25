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
Month    Income ($)    Expense ($)    Profit ($)
-------  ------------  -------------  ------------
6        0.00          282.50         (282.50)
7        0.00          280.01         (280.01)
8        1,755.89      275.91         1,479.98
9        962.80        368.15         594.65
10       1,462.80      1,358.03       104.77
11       1,537.80      383.47         1,154.33
12       2,169.20      1,313.23       855.97
Total    7,888.49      4,261.30       3,627.19
```
