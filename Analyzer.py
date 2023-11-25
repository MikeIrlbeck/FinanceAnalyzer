
import json
import re
import os.path
from datetime import date

data = open(
    "/Users/michaelirlbeck/Documents/FinanceAnalyzer/ExpenseData.txt", "r")


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

for x in data:
    if filter(x):
        try:
            purchases.append(parsePurchaseLine(x))
        except ValueError:
            raise Exception("Error: " + str(x))

        # print("{} : {}".format(len(x), x))

data.close()

purchases.sort(key=lambda el: el.date)  # sort by date

total = 0.0
for purchase in purchases:
    total = total + float(purchase.amount)
    # print(p)
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
# ab = filter(lambda mp: mp.getTotal() > 0.0, monthPurchases)
# TypeError: filter() takes 1 positional argument but 2 were given

# filtered = []
# for mp in monthPurchases:
#     if (mp.getTotal() > 0.0):
#         filtered.append(mp)

# monthPurchases = filtered

for yp in yearPurchases:
    print(yp)


# Attempt to sort into categories
class Category(object):
    def __init__(self, name):  # , purchases = []): doing this causes shared data; why??
        self.name = name
        self.purchases = []

    def add(self, purchase):
        self.purchases.append(purchase)

    def toJSON(self):
        string = ""
        append = ""
        for p in self.purchases:
            string = string + append + str(p)
            append = ","
        return {"name": self.name, "purchases": string}


names = ["Car", "Groceries", "Eating Out", "Personal", "Miscellaneous"]

categories = []

for name in names:
    categories.append(Category(name))

string = ""
m = 0
for name in names:
    string = "{}\t{}:{}".format(string, str(m), name)
    m = m + 1

print(string)

m = 0
for purchase in purchases:
    i = input("{}: ".format(str(purchase.item)))
    print("selected {}, len: {}".format(
        categories[int(i)].name, len(categories[int(i)].purchases)))
    categories[int(i)].add(purchase)
    m = m + 1
    if m > 3:
        break

# if os.path.exists(modelPath):
#     print("Exists! - " + modelPath)
#     mode = "r"
# else:
#     print("Does not exists - " + modelPath)
#     mode = "w"

modelPath = "/Users/michaelirlbeck/Desktop/Finances/Model.json"
model = open(modelPath, "w+")

for category in categories:
    # model.write(str(category))
    model.write(json.dumps(category.toJSON()) + "\n")

model.close()

model = open(modelPath, "r")

loadedPurchases = []

for line in model:
    x = json.loads(line)
    # print(str(type(x)))
    # print(x)
    # print("{}".format(x["name"]))
    # print("{}".format(x["purchases"]))
    # print("{}".format(x["purchases"].split(",")))

    if x["purchases"]:
        for purchase in x["purchases"].split(","):
            data = purchase.split(":")
            dateData = data[0].strip().split("-")
            # create list of purchases
            loadedPurchases.append(Purchase(date(int(dateData[0]), int(dateData[1]), int(dateData[2])),
                                            data[1].strip(), data[2].strip()))
            # recreate list of categories with their purchases

total = 0.0
for purchase in loadedPurchases:
    total = total + float(purchase.amount)
    # print(p)
print("total amount: ${:.2f}".format(total))

model.close()
