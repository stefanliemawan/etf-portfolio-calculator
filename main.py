import matplotlib.pyplot as plt
import pandas as pd

INVESTMENT_AMOUNT = 18054.07

PIES = {
    "VWRP": 0.40,
    "CNX1": 0.33,
    "VFEG": 0.15,
    "VEUA": 0.12,
}

PIES = {
    "VWRP": 0.9,
}

iitu_holdings_df = pd.read_csv("holding/IITU_14_02_2025.csv", header=2)
iitu_holdings_df = iitu_holdings_df[
    ["Ticker", "Name", "Sector", "Weight (%)", "Location"]
]
iitu_holdings_df["Region"] = iitu_holdings_df["Location"].apply(
    lambda x: "US" if x == "United States" else "-"
)
iitu_holdings_df.drop("Location", axis=1, inplace=True)
iitu_holdings_df.rename(
    columns={"Name": "Holding name", "Weight (%)": "% of market value"}, inplace=True
)

cnx1_holdings_df = pd.read_csv("holding/CNX1_14_02_2025.csv", header=2)
cnx1_holdings_df = cnx1_holdings_df[
    ["Ticker", "Name", "Sector", "Weight (%)", "Location"]
]
cnx1_holdings_df["Region"] = cnx1_holdings_df["Location"].apply(
    lambda x: "US" if x == "United States" else "-"
)
cnx1_holdings_df.drop("Location", axis=1, inplace=True)
cnx1_holdings_df.rename(
    columns={"Name": "Holding name", "Weight (%)": "% of market value"}, inplace=True
)

# TODO - fix later

pie_holdings_df = pd.DataFrame()

for etf, dist in PIES.items():
    if etf == "IITU":
        holdings_df = iitu_holdings_df
    elif etf == "CNX1":
        holdings_df = cnx1_holdings_df
    else:
        holdings_df = pd.read_excel(f"holding/{etf}_14_02_2025.xlsx", header=6)

    try:
        holdings_df["pie_percentage"] = (
            holdings_df["% of market value"].str.rstrip("%").astype(float) / 100
        ) * dist
    except:
        holdings_df["pie_percentage"] = (
            holdings_df["% of market value"].astype(float) / 100
        ) * dist

    pie_holdings_df = pd.concat([pie_holdings_df, holdings_df], ignore_index=True)
    # print(holdings_df)

pie_holdings_df = pie_holdings_df.groupby(["Ticker", "Region"], as_index=False)[
    "pie_percentage"
].sum()
pie_holdings_df.sort_values(by=["pie_percentage"], inplace=True, ascending=False)
pie_holdings_df["% of investment"] = (pie_holdings_df["pie_percentage"] * 100).round(
    6
).astype(str) + "%"
pie_holdings_df["amount_invested"] = (
    pie_holdings_df["pie_percentage"] * INVESTMENT_AMOUNT
)

print(pie_holdings_df.head())

pie_holdings_df.to_csv("results/pie_holdings.csv", index=False)


pie_regions_df = (
    pie_holdings_df.groupby("Region")["amount_invested"].sum().reset_index()
)

total_investment = pie_regions_df["amount_invested"].sum()
pie_regions_df["percentage"] = pie_regions_df["amount_invested"] / total_investment
pie_regions_df.sort_values(by=["percentage"], inplace=True, ascending=False)
pie_regions_df["percentage"] = (
    (pie_regions_df["amount_invested"] / total_investment) * 100
).round(2).astype(str) + "%"

pie_regions_df.to_csv("results/pie_regions.csv", index=False)
