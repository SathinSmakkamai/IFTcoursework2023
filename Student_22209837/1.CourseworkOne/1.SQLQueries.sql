/*
Author: Sathin Smakkamai
Student number: 22209837
Date: 15/03/2024
Content: SQL Queries for CourseWork One
*/

SET search_path = cash_equity, "$user", public;

--------------------------------------------------------------------------------------------------------
-- Query 1: Get the percentage change of equity in different sectors within the USA --------------------
--------------------------------------------------------------------------------------------------------

-- Calculate statistics for percentage gain/loss in equity prices
SELECT gics_sector,
       ROUND(MAX(((close_price - open_price) / open_price) * 100), 2) AS max_percentage_gain,
       ROUND(MIN(((close_price - open_price) / open_price) * 100), 2) AS max_percentage_loss,
       ROUND(AVG(((close_price - open_price) / open_price) * 100), 4) AS avg_percentage_return,
       ROUND(STDDEV(((close_price - open_price) / open_price) * 100), 4) AS std_gain
-- Join 2 table to get both price and general information
FROM equity_prices
INNER JOIN equity_static ON equity_prices.symbol_id = equity_static.symbol
-- Add constrain on the query (on date and country)
WHERE country = 'US' AND cob_date >= '2021-01-01' AND cob_date < '2022-01-01'
-- Group by sector
GROUP BY gics_sector;
-- Order by avg_percentage_return
ORDER BY avg_percentage_return DESC;

--------------------------------------------------------------------------------------------------------
-- Query 2: Get the portfolio weight by equity in each sector ------------------------------------------
--------------------------------------------------------------------------------------------------------

-- Calculate statistics for portfolio positions
SELECT gics_sector,
       COUNT(gics_sector) as sector_count,
       SUM(net_amount) as sector_net_amount,
       -- Get total portfolio position using sub query
       ROUND((SUM(net_amount) / (SELECT SUM(net_amount) FROM portfolio_positions)*100),2) as sector_weight
-- Join 2 table to get list of invested equity and general information of each equity
FROM portfolio_positions
LEFT JOIN equity_static ON portfolio_positions.symbol = equity_static.symbol
-- Group by sector
GROUP BY gics_sector;
-- Order by sector_weight
ORDER BY sector_weight DESC;

--------------------------------------------------------------------------------------------------------
-- Query 3 (subquery): Get Invested position in USD ----------------------------------------------------
--------------------------------------------------------------------------------------------------------

-- Calculate each position in USD
SELECT *,
       -- Convert purchased currency to USD
       CASE
           -- Return portfolio_positions if currency is already USD
           WHEN portfolio_positions.ccy = 'USD' THEN portfolio_positions.net_amount
           -- Convert purchased currency ti USD using exchangerate
           ELSE portfolio_positions.net_amount * exchange_rates.exchange_rate
           END AS net_amount_USD
-- Join 2 table to get portfolio position and exchangerate
FROM portfolio_positions
LEFT JOIN exchange_rates
    -- Match the date
    ON portfolio_positions.cob_date = exchange_rates.cob_date
    -- Match the purchased currency and currency that has to be converted
    AND portfolio_positions.ccy = exchange_rates.from_currency
-- get USD as a result conversion currency
WHERE exchange_rates.to_currency = 'USD';

--------------------------------------------------------------------------------------------------------
-- Query 3: Get the portfolio values in USD for each trader --------------------------------------------
--------------------------------------------------------------------------------------------------------

-- Calculate investment made by each trader
SELECT trader_name, ROUND(SUM(net_amount_USD), 2) AS portfolio_value_USD
FROM (
    -- From subquery 3.1
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
-- Join 2 table to get trader name for each trader_id
LEFT JOIN trader_static ON subquery.trader = trader_static.trader_id
-- Group by trader
GROUP BY trader_static.trader_name
-- Order by portfolio_value_USD
ORDER BY portfolio_value_USD DESC;