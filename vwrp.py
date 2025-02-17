import pandas as pd

INVESTMENT_AMOUNT = 15000

PIES = {
    "VWRP": 1,
}


pie_holdings_df = pd.DataFrame()

for etf, dist in PIES.items():
    holdings_df = pd.read_excel(f"holding/{etf}_14_02_2025.xlsx", header=6)

    holdings_df["pie_percentage"] = (
        holdings_df["% of market value"].str.rstrip("%").astype(float) / 100
    ) * dist

    pie_holdings_df = pd.concat([pie_holdings_df, holdings_df], ignore_index=True)

pie_holdings_df["Ticker"] = pie_holdings_df["Ticker"].astype(str)
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

pie_holdings_df.to_csv("results/pie_holdings_full_vwrp.csv", index=False)


pie_regions_df = (
    pie_holdings_df.groupby("Region")["amount_invested"].sum().reset_index()
)

total_investment = pie_regions_df["amount_invested"].sum()
pie_regions_df["percentage"] = pie_regions_df["amount_invested"] / total_investment
pie_regions_df.sort_values(by=["percentage"], inplace=True, ascending=False)
pie_regions_df["percentage"] = (
    (pie_regions_df["amount_invested"] / total_investment) * 100
).round(2).astype(str) + "%"

pie_regions_df.to_csv("results/pie_regions_full_vwrp.csv", index=False)
