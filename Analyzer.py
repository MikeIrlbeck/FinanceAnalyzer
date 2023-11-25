import re
from datetime import date
from tabulate import tabulate


class Purchase():
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

        def add(self, purchase):
            self.purchases.append(purchase)

        def getMonth(self):
            return self.month

        def getTotal(self):
            total = 0.0
            for p in self.purchases:
                total = total + p.amount
            return total

    def __init__(self, year):
        self.year = year
        self.monthPurchases = []
        for i in range(1, 13):
            self.monthPurchases.append(self.MonthOfPurchase(i))

    def add(self, purchase: Purchase):
        if (purchase.date.month >= 1 and purchase.date.month < 13):
            self.monthPurchases[purchase.date.month - 1].add(purchase)

    def getTotal(self) -> float:
        total = 0.0
        for month in self.monthPurchases:
            total += month.getTotal()
        return total

    def __str__(self) -> str:
        output = "\n%d Financial Report\n" % self.year

        data = []
        for mp in self.monthPurchases:
            if (mp.getTotal() > 0.0):
                data.append(
                    [str(mp.getMonth()), "{:.2f}".format(mp.getTotal())])

        data.append(["Total", "%.2f" % self.getTotal()])
        output += tabulate(data, headers=['Month', 'Expense ($)'])
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

        return Purchase(thisDate, dataList.group(2), dataList.group(3))

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


purchases = read_finance_data(
    "/Users/michaelirlbeck/Documents/FinanceAnalyzer/ExpenseData.txt")


for purchase in purchases:
    index = int(purchase.date.year) - 2022
    yearPurchases[index].add(purchase)

for yp in yearPurchases:
    print(yp)
