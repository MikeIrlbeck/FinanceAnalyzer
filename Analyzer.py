import re
import os
from datetime import date
from tabulate import tabulate


class Item():
    def __init__(self, date, item, amount):
        self.date = date
        self.item = item
        self.amount = float(amount)

    def __str__(self) -> str:
        return "{} : {} : {}".format(self.date, self.item, self.amount)


class YearOfPurchase:
    class MonthOfPurchase:
        def __init__(self, month):
            self.month = month
            self.purchases = []
            self.revenue = []

        def addExpense(self, item):
            self.purchases.append(item)

        def addRevenue(self, item):
            self.revenue.append(item)

        def getMonth(self):
            return self.month

        @staticmethod
        def _getTotal(items: list):
            total = 0.0
            for p in items:
                total = total + p.amount
            return total

        def getTotalExpenses(self):
            return self._getTotal(self.purchases)

        def getTotalRevenue(self):
            return self._getTotal(self.revenue)

        def getTotalProfit(self):
            return self.getTotalRevenue() - self.getTotalExpenses()

    def __init__(self, year):
        self.year = year
        self.monthPurchases = []
        for i in range(1, 13):
            self.monthPurchases.append(self.MonthOfPurchase(i))

    def _addItem(self, item: Item, callback: None):
        if (item.date.month >= 1 and item.date.month < 13):
            callback(self.monthPurchases[item.date.month - 1], item)

    def addExpense(self, item: Item):
        self._addItem(item, lambda x, y: x.addExpense(y))

    def addRevenue(self, item: Item):
        self._addItem(item, lambda x, y: x.addRevenue(y))

    def _getTotal(self, x: None) -> float:
        total = 0.0
        for month in self.monthPurchases:
            total += x(month)
        return total

    def getTotalExpenses(self) -> float:
        return self._getTotal(lambda x: x.getTotalExpenses())

    def getTotalRevenue(self) -> float:
        return self._getTotal(lambda x: x.getTotalRevenue())

    def getTotalProfit(self) -> float:
        return self._getTotal(lambda x: x.getTotalProfit())

    def __str__(self) -> str:
        output = "\n%d Financial Report\n" % self.year

        formatNumber = "{:.2f}"
        data = []
        for mp in self.monthPurchases:
            if (mp.getTotalExpenses() > 0.0):
                profit = mp.getTotalProfit()
                data.append(
                    [str(mp.getMonth()),
                     formatNumber.format(mp.getTotalExpenses()),
                     formatNumber.format(mp.getTotalRevenue()),
                     formatNumber.format(profit) if profit > 0 else ("(%s)" % formatNumber).format(abs(profit))])

        data.append(["Total",
                     formatNumber.format(self.getTotalExpenses()),
                     formatNumber.format(self.getTotalRevenue()),
                     formatNumber.format(self.getTotalProfit())])
        output += tabulate(data,
                           headers=['Month', 'Expense ($)', 'Income ($)', 'Profit ($)'])
        return output


yearPurchases = []

for j in range(2022, 2023 + 1):
    yearPurchases.append(YearOfPurchase(j))


def read_finance_data(file_str: str) -> list:
    def parsePurchaseLine(line):
        dataList = re.search(
            r"(^[0-9|/\*]+),{1}\s*([^,]*)\s*,\s*\$?(\d*(\.\d+)?)", line)

        if dataList is None:
            raise Exception("Bad read of: {}".format(line))

        dateList = dataList.group(1).split("/")
        year = dateList[-1] if len(dateList[-1]
                                   ) > 2 else "20" + str(dateList[-1])
        day = int(dateList[1]) if bool(
            re.search(r"[0-9]+", dateList[1])) else int(1)
        thisDate = date(int(year), int(dateList[0]), day)

        return Item(thisDate, dataList.group(2), dataList.group(3))

    def filter(line):
        return (re.search(r"^\s$", line)) is None  # true if no whitepsace

    items = []
    with open(file_str, "r") as data:
        for x in data:
            if filter(x):
                try:
                    items.append(parsePurchaseLine(x))
                except ValueError:
                    raise Exception("Error: " + str(x))

    items.sort(key=lambda el: el.date)  # sort by date
    return items


cwd = os.getcwd()
purchases = read_finance_data(cwd + "/ExpenseData.txt")

revenue = read_finance_data(cwd + "/IncomeData.txt")


groups = []
groups.append({'items': purchases, 'callback': lambda x, y: x.addExpense(y)})
groups.append({'items': revenue, 'callback': lambda x, y: x.addRevenue(y)})
for items in groups:
    for item in items['items']:
        index = int(item.date.year) - 2022
        items['callback'](yearPurchases[index], item)

for yp in yearPurchases:
    print(yp)
