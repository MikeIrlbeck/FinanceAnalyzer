
import re
from datetime import date


class Purchase():
    def __init__(self, date, item, amount):
        self.date = date
        self.item = item
        self.amount = float(amount)

    def __str__(self) -> str:
        return "{} : {} : {}".format(self.date, self.item, self.amount)


def filter(line):
    return (re.search(r"^\s$", line)) is None  # true if no whitepsace


def parsePurchaseLine(line):
    dataList = re.search(
        r"(^[0-9|/\*]+),{1}\s*([^,]*)\s*,\s*\$?(\d*(\.\d+)?)", line)

    if dataList is None:
        raise Exception("Bad read of: {}".format(line))

    dateList = dataList.group(1).split("/")
    year = dateList[-1] if len(dateList[-1]) > 2 else "20" + str(dateList[-1])
    day = int(dateList[1]) if bool(
        re.search(r"[0-9]+", dateList[1])) else int(1)
    thisDate = date(int(year), int(dateList[0]), day)

    return Purchase(thisDate, dataList.group(2), dataList.group(3))


purchases = []

with open("/Users/michaelirlbeck/Documents/FinanceAnalyzer/ExpenseData.txt", "r") as data:

    for x in data:
        if filter(x):
            try:
                purchases.append(parsePurchaseLine(x))
            except ValueError:
                raise Exception("Error: " + str(x))


purchases.sort(key=lambda el: el.date)  # sort by date

total = 0.0
for purchase in purchases:
    total = total + float(purchase.amount)
print("total amount: ${:.2f}".format(total))


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
        output = "Purchases of year %d\n" % self.year
        output += "Total $%.2f\n" % self.getTotal()

        for mp in self.monthPurchases:
            if (mp.getTotal() > 0.0):
                output += "{:d} : {:.2f}\n".format(
                    mp.getMonth(), mp.getTotal())

        return output


yearPurchases = []

for j in range(2022, 2023 + 1):
    yearPurchases.append(YearOfPurchase(j))
print(len(yearPurchases))
for purchase in purchases:
    index = int(purchase.date.year) - 2022
    yearPurchases[index].add(purchase)

for yp in yearPurchases:
    print(yp)
