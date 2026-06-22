import pandas as pd

fund_master = pd.read_csv("../data/raw/fund_master.csv")

print("Fund Houses")
print(fund_master["fund_house"].unique())

print("\nCategories")
print(fund_master["category"].unique())

print("\nSub Categories")
print(fund_master["subcategory"].unique())

print("\nRisk Grades")
print(fund_master["risk_grade"].unique())
