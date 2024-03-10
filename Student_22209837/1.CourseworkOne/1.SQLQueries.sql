/*
Author: Student_22209837
Date: 2022-11-07
Content: SQL Queries for CourseWork One
*/

SET search_path = cash_equity, "$user", public;


-- Query 1 --------------------------------------------------------------------------------

SELECT gics_sector,
    ROUND(MAX(((close_price - open_price) / open_price) * 100), 2) AS max_percentage_gain,
    ROUND(MIN(((close_price - open_price) / open_price) * 100), 2) AS max_percentage_loss,
    ROUND(AVG(((close_price - open_price) / open_price) * 100), 4) AS avg_percentage_return,
    ROUND(STDDEV(((close_price - open_price) / open_price) * 100), 4) AS std_gain
FROM equity_prices
INNER JOIN equity_static ON equity_prices.symbol_id = equity_static.symbol
WHERE country = 'US' AND cob_date >= '2021-01-01' AND cob_date < '2022-01-01'
GROUP BY gics_sector;

-- Query 2.1 ------------------------------------------------------------------------------

SELECT *,
    CASE WHEN portfolio_positions.ccy = 'USD' THEN portfolio_positions.net_amount
         ELSE portfolio_positions.net_amount * exchange_rates.exchange_rate
         END AS net_amount_USD
    FROM portfolio_positions
    LEFT JOIN exchange_rates
         ON portfolio_positions.cob_date = exchange_rates.cob_date
         AND portfolio_positions.ccy = exchange_rates.from_currency
    WHERE exchange_rates.to_currency = 'USD';

-- Query 2.2 ------------------------------------------------------------------------------

SELECT trader, ROUND(SUM(net_amount_USD), 2) AS portfolio_value_USD
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
GROUP BY trader
ORDER BY portfolio_value_USD DESC;
