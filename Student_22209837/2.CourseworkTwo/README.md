

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

In this coursework, we use PGadmin and PostgreSQL as a SQL database. Within our database "cash_equity", we have six different tables. The three following queries from the SQL database represent the possible usage and implications of big data that can improve real-world decision-making.

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

For NoSQL databases, in this case, we use MongoDB, a non-relational document database. Its document-oriented structure allows for storing data in JSON-like documents, making it easy to work with dynamic and evolving data models. In MongoDB, data is structured as key-value pairs within documents, which are organized into collections. This can be compared to the SQL structure where collections correspond to tables, documents to rows, and keys to columns. Consequently, data is stored separately, and the database is less suitable for establishing relationships between data but rather primarily provides search queries with basic aggregate functions.

#### Query 1: Find Equity in the Energy Sector with Some Constraints
```
db.CourseworkOne.find({
    "StaticData.GICSSector": "Energy",
    "MarketData.MarketCap": { $gt: 10000 },
    "MarketData.Beta": { $gte: 0.7, $lte: 1.3 },
    "FinancialRatios.DividendYield": { $gt: 5.0 } })
```

#### Query 2: Find the top 10 large-market-cap Equities with the highest dividend yield
```
db.CourseworkOne.find({
    "MarketData.MarketCap": { $gt: 10000 }})
    .sort({ "FinancialRatios.DividendYield": -1 })
    .limit(10)
```

#### Query 3: Find the top 5 equities from either the energy sector or the consumer discretionary
```
db.CourseworkOne.find({
    $and: [
        { $or: [{ "StaticData.GICSSector": "Energy" }, { "StaticData.GICSSector": "Consumer Discretionary" } ] },
        { "MarketData.Beta": { $gt: 0.7 } } ]})
    .sort({ "MarketData.Beta": -1})
    .limit(5)
```

#### Query 4: Get the total market capitalization for each subsector in the Industrial sector
```
db.CourseworkOne.aggregate([
    { $match: { "StaticData.GICSSector": 'Industrials' } },
    { $group: { _id: "$StaticData.GICSSubIndustry",
            totalMarketCap: { $sum: "$MarketData.MarketCap" } } },
    { $sort: { totalMarketCap: -1 } }])
```

#### Query 5: Get the number of equities in each sector
```
db.CourseworkOne.aggregate([
    { $group: { _id: "$ StaticData.GICSSector",
            count: { $sum: 1 } } },
    { $sort: { count: -1 } } ])
```
