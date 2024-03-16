

# IFTE0003: Big Data in Quantitative Finance Coursework 1
# Sathin Smakkamai 22209837
## My first coursework

- [My first coursework](#my-first-coursework)
  - [Introduction](#introduction)
  - [SQL Query explain](#sql-query-explain)
  - [NoSQL Query Explain](#nosql-query-explain)

## Introduction

In the realm of finance, the introduction of big data in recent decades has revolutionized many decision-making processes, allowing financial institutions to transform these vast volumes of information to gain insights. Within this state of the art, big data has already been integrated into multiple areas in finance, ranging from simple searches into historical data to more advanced practices such as market trend prediction, understanding customer behaviors, risk management strategies, and optimizing investment portfolios.

In this case of big data in quantitative finance coursework, we will delve into the practice of utilizing inquiry tools to access and understand SQL and NoSQL databases. The project will be constructed using Docker as the main platform to integrate databases, query languages (PostgreSQL and MongoDB), and their graphical user interfaces (GUI) into the same development space. Furthermore, to mimic a real development workflow, we are also adding Git as a tool to keep track of our project, facilitate upgrades and downgrades, and enable scalability in the future if more developers are involved.


## SQL Query explain

#### Query 1: Get the percentage change of equity in different sectors within the USA

```
SELECT gics_sector,
    ROUND(MAX(((close_price - open_price) / open_price) * 100), 2) AS max_percentage_gain,
    ROUND(MIN(((close_price - open_price) / open_price) * 100), 2) AS max_percentage_loss,
    ROUND(AVG(((close_price - open_price) / open_price) * 100), 4) AS avg_percentage_return,
    ROUND(STDDEV(((close_price - open_price) / open_price) * 100), 4) AS std_gain
FROM equity_prices
INNER JOIN equity_static ON equity_prices.symbol_id = equity_static.symbol
WHERE country = 'US' AND cob_date >= '2021-01-01' AND cob_date < '2022-01-01'
GROUP BY gics_sector;
```

#### Query 2: Get the portfolio weight by equity in each sector

```
SELECT gics_sector,
    COUNT(gics_sector) as sector_count,
    SUM(net_amount) as sector_net_amount,
    ROUND((SUM(net_amount) / (SELECT SUM(net_amount) FROM portfolio_positions)*100),2) as sector_weight
FROM portfolio_positions
LEFT JOIN equity_static ON portfolio_positions.symbol = equity_static.symbol
GROUP BY gics_sector;
```
#### Query 3: Get the portfolio values in USD for each trader

```
SELECT trader_name, ROUND(SUM(net_amount_USD), 2) AS portfolio_value_USD
FROM (
    SELECT *,
	    CASE WHEN portfolio_positions.ccy = 'USD' THEN portfolio_positions.net_amount
             ELSE portfolio_positions.net_amount * exchange_rates.exchange_rate
             END AS net_amount_USD
    FROM portfolio_positions
    LEFT JOIN exchange_rates
        ON portfolio_positions.cob_date = exchange_rates.cob_date
        AND portfolio_positions.ccy = exchange_rates.from_currency
    WHERE exchange_rates.to_currency = 'USD'	
     )
AS subquery
LEFT JOIN trader_static ON subquery.trader = trader_static.trader_id
GROUP BY trader_static.trader_name
ORDER BY portfolio_value_USD DESC;

```


## NoSQL Query Explain

#### Query 1: Find the top 10 large-market-cap equities with the highest dividend yield

```
db.Static.find({
    "MarketCap": { $gt: 10000 }})
    .sort({ "DividendYield": -1 })
    .limit(10)
```
#### Query 2: Get the total market capitalization for each subsector in the Industrial sector

```
db.Static.aggregate([
    { $match: { GICSSector: 'Industrials' } },
    { $group: { _id: "$GICSSubIndustry",
            totalMarketCap: { $sum: "$MarketCap" } } },
    { $sort: { totalMarketCap: -1 } } ])
```

#### Query 3: Get the number of equities in each sector

```
db.Static.aggregate([
    { $group: { _id: "$GICSSector",
            count: { $sum: 1 } } },
    { $sort: { count: -1 } } ])
```
