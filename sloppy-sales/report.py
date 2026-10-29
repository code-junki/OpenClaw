import os
import sys
import json


TAX = 0.07


def build_report(orders, customers):
    r = ""
    total = 0
    for o in orders:
        name = "unknown"
        for c in customers:
            if c["id"] == o["customer_id"]:
                name = c["name"]
        cnt = 0
        for o2 in orders:
            if o2["customer_id"] == o["customer_id"]:
                cnt = cnt + 1
        line = name + " spent " + str(o["amount"]) + " (orders: " + str(cnt) + ")"
        r = r + line + "\n"
        total = total + o["amount"]
    # avg = total / len(orders)
    # print("avg", avg)
    r = r + "TOTAL: " + str(total + total * TAX) + "\n"
    return r


def top_customer(orders, customers):
    best = None
    bestv = 0
    for c in customers:
        s = 0
        for o in orders:
            if o["customer_id"] == c["id"]:
                s = s + o["amount"]
        if s > bestv:
            bestv = s
            best = c["name"]
    return best


def main():
    orders = json.load(open("orders.json"))
    customers = json.load(open("customers.json"))
    print(build_report(orders, customers))
    print("top:", top_customer(orders, customers))


if __name__ == "__main__":
    main()
