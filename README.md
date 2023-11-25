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
```mm/dd/yr, Name, amount```

Example:
```11/23/23, Charity, $50```

## Output
```
2022 Financial Report
Month      Expense ($)
-------  -------------
6               282.5
7               280.01
8               275.91
9               368.15
10             1358.03
11              383.47
12             1313.23
Total          4261.3
```
