# UCL - IFT Big Data Quantitative Finance Coursework
- [UCL - IFT Big Data Quantitative Finance Coursework](#ucl---ift-big-data-quantitative-finance-coursework)
  - [Coursework Two](#coursework-two)
    - [Objectives](#objectives)
    - [Use case: incorrect trade detection](#use-case-incorrect-trade-detection)
    - [Use case: risk policy breach](#use-case-risk-policy-breach)
    - [Use case: benchmark trader performance](#use-case-benchmark-trader-performance)
    - [Code Submission](#code-submission)
    - [Report](#report)
    - [Marking Criteria](#marking-criteria)
  - [Coursework One](#coursework-one)
    - [Objectives](#objectives-1)
    - [Sql and NoSql database for coursework one](#sql-and-nosql-database-for-coursework-one)
    - [Requirements](#requirements)
      - [Code Submission](#code-submission-1)
      - [Report](#report-1)
      - [Marking Criteria](#marking-criteria-1)

## Coursework Two

### Objectives

The objective of Coursework Two is to demonstrate a practical understanding of building data pipelines in order to extract data from a database, manipulate data and then load into a database.

In order to achieve this objective, the student can use R/Python programming languages and perform the following tasks:

- design a data pipeline by selecting one of the three use cases listed below;
- extract from a file/database using Python/R, transform data with Python/R and load transformed data into a database;
- extract data from a database, load into another database and transform data using a set of stored database procedures.

The student should select one of the following use cases:

### Use case: incorrect trade detection

Your front office data science engineering team has been tasked with the challenge of building a data pipelines which performs the following tasks:

- Process the batch trade file generated every day (approximately every 30 minutes);
- Set-up a data pipeline that enables to store trades and positions in the team database(s).

**Specs:**

Files are generated every day and stored in a shared file location folder '/IFTCourseWork2023/000.Database/DataLake/FOTrades';
- The trade file contains all trades of the last 30 minutes;
- the trade files has naming convention as following: FrontOfficeTrades_YYYYMMDDHHmmSS.parquet ("mm" are minutes while "MM" refers to the month);
- The trade file contains the following columns: DateTime, TradeId, Trader, Symbol, Quantity, Notional, TradeType, Ccy, Counterparty;
- The trade file is generated along side a ctl file which is written when all trades have been successfully written to the parquet file;

For each day, the objective of this use case is to:

1. design, develop and implement a process that retrieve all trades from /IFTCourseWork2023/000.Database/DataLake/FOTrades, stores both trades and positions in the database;
2. In order to achieve this result you can leverage on any database Postgres and/or MongoDB;
3. apply a model that checks on trades for consistency with expectations (i.e. there is no fat fingers error, inconsistency between quantity traded and notional amounts, genuine mis-pricing on the trade); Here, you can apply any model to detect whether a trade is genuine or not. This can be done in multiple ways (trade vs other trades, trade vs price, hypothesis testing, clustering analysis), any approach is valid however please describe in the methodology section why you pick one approach over another.
4. if any, create a new table in SQLite Database called trades_suspects. Load suspect trades into a new table in SQL. The creation statement for this table should be stored in "./modules/db/SQL/CreateTable.*" where * should be replaced by .sql, .py or .R. Table should be designed to follow best practices and must then include a primary key and a foreign key.
5. You can create any further table(s) in sql, if so, please add all creation statements to CreateTable file (see previous point);
6. in order to obtain the positions, you will need to aggregate Quantity and Notional for all trades by date, trader, symbol, ccy and insert the results into portfolio_positions.(see section on Database description)

For development purposes, a test-case file is provided in the folder IFTCourseWork2023\000.Database\DataLake\FOTrades with the name EquityTrades_20231123110001.parquet;



### Use case: risk policy breach

Second Line Risk has agreed with your Front Office risk team to set-up controls and limits in order to monitor all risk positions for our traders.

You have been tasked with the design of a process that performs the following tasks:

In MongoDB database, the Database ExchangeTraded contains a collection called EquityTrades which contains all End of Day trades for all traders
- on any given day, retrieve all trades as per end of day from MongoDB Database ExchangeTraded contains a collection called EquityTrades;
- aggregate all trades by Trader, ISIN, Currency and Date;
- retrieve all policy limits from SQL database;
- check if any new aggregated position is breaching a policy limit (check for at least one of the below policy limits);
- if a policy limit is breached, design and create a new SQLite table called policy_breaches and load all breaches into the new table. The creation statement for this table should be stored in "./modules/db/SQL/CreateTable.*" where * should be replaced by .py or .R. Table should be designed to follow best practices and must then include a primary key and a foreign key.
- load all trades into portfolio_positions (see section on Database description)

Policy limits description:

- if limit_end is not null, limit has been changed or decommissioned;
- long/short consideration: max amount in USD$ (mark to market) for a single stock position;
- volume relative (%): max position given daily volumes. The trader cannot have more than X% of daily volume as ratio of position consideration. position must be mark to market over the volume;
- sector relative: max concentration of portfolio allocations by sector. all stocks in a portfolio for a sector cannot exceed the X% specified. this is the result of sum portfolio value as quantity times market price (mark to market positions) by sector over the total mark to market portfolio value.
- ES relative (%): the trader cannot run a portfolio that has an expected shortfall greater than X%. Expected shortfall is calculated as the average of 5 biggest losses of the last 50Days portfolio returns with an holding period of 3 days (i.e. Price today / Price 3 Days ago - 1)
- Volatility (%): the trader cannot run a portfolio that has a portfolio annualised return volatility greater than the limit express in percentages. Look-back for volatility calculations is 50Days.
- VaR Relative (%): the trader cannot run a portfolio that has a Value at Risk greater than X%. Value at Risk is calculated on the fully revaluated portfolios returns, look-back period 50Days, holding period 3 days, 99% confidence level. Value at Risk can be estimated by using either historical simulations or the Variance-Covariance Method. If the Variance-Covariance Method is used, all parameters described above should be used to estimate the portfolio variance over 50Days. The assumption of normal distributions of returns is accepted.

Mongo Data Description:

```

DateTime: Mongo ISODate. gte,gt,lt,lte,eq can be used as an example {ISODate("2020-01-06T08:19:56.000+00:00")};
TradeId: Unique identifier of a trade;
Trader: Trader identifier;
Symbol: Stock identifier;
Quantity: Number of shares exchanged;
Notional: Value of shares exchanged;
TradeType: describes whether trade is a "BUY" or a sell;
Ccy: currency in which notional is denominated;
Counterparty: trading counterparty.

```
To achieve net positions at the end of the day, trades should be filtered for a given date and aggregated by Trader, Symbol, Ccy by summing Quantity and Notional.

PSQL Data description:

```
portfolio_positions (
    pos_id TEXT PRIMARY KEY, -- unique identifier made of traderid + cob_date (Ymd) + symbol_id
    cob_date TEXT NOT NULL,  -- date in format of DD-Mmm-YYYY
    trader TEXT NOT NULL,    -- trader identifier
    symbol TEXT NOT NULL,    -- stock identifier
    ccy TEXT NOT NULL,       -- currency for notional amount   
    net_quantity INTEGER NOT NULL,      -- aggregation of all trades made in a given date by trader & stock as sum
    net_amount INTEGER NOT NULL,        -- aggregation of all notional made in a given date by trader & stock as sum
    FOREIGN KEY (symbol) REFERENCES equity_static (symbol)
)

```

For development purposes, a test-case/dev-case collection is provided in the database ExchangeTraded, collection called EquityPositions.


### Use case: benchmark trader performance

As front office analyst, we would like to verify if one of our traders strategy is outperforming a given benchmark. In order to achieve this goal:

- design, develop and implement a data pipelines which 
- can generate daily allocations and total value of a custom benchmark;
- for each trader construct a relative and absolute performance against the custom benchmark.

Accordingly,

1. as starting point, construct a benchmark (Equally Weighted, Liquidity Weighted or MarketCap weighted). In order to construct a weighted benchmark it is possible to follow different specification (MSCI, FTSE, Blackrock or Axioma). It is further possible to tilt the benchmark towards a particular factor that you think fits best the trader. This can be achieved by tilting on industry/sector, on market conditions (volatility, momentum, liquidity) or on dividend yield / beta / cash flows. Some starting info can be found here;
2. When a benchmark is derived, it's components and weights can be stored in SQL or NoSQL database at the discretion of the designer;
3. Once a benchmark is derived, create a table and store all benchmark returns for the past year into a new sql table called benchmark_returns.

### Code Submission

Code must be submitted in Github. The repository for submission is iftcoursework2023. Students upload Coursework Number 2 code in their own folders created in Coursework One.

The folder structure is as per following (with * replaced by py or R extension)

```
Student_<insert your student number>
    ├── CHANGELOG.md
    ├── 1.CourseworkOne/
        ├── 1.SQLQueries.sql
        ├── 2.NoSQLQueries.js
        ├── README.md
        └── .gitkeep
    ├── 2.CourseworkTwo/
        ├── config/
            ├── script.config
            └── script.params
        ├── modules/
        ├── static/
        ├── test/
        ├── Main.*
        ├── .gitkeep
        └── README.md    

```

Not all sub-folders must be used. If a given folder is empty, please make sure a .gitkeep is placed in the directory so that it will be retained in the commit.

Subfolder ./modules can be further structured in sub-folders name after what the contain. an example could be:

```
├── modules/
    ├──db/
        └── db_connection.*
    ├── input/
        └── input_loader.*
    ├── output/
        ├── script_purposes.*
        └── etc..etc.. 
```

All scripts should be parametrised in such a way that it is possible to trigger them by any environment.

As an example:
- Rscript Main.R param1 param2 param3 ...
- Python Main.py param1 param2 param3 ...

config sub-folder should contain all the configurations and params that can be amended without affecting the code logic.

test sub-folder contains a test files. While is non-mandatory part of the coursework, it is encouraged to perform some functional or unit test to evaluate if modules or functions are fit for use. Any standard module/library can be used for this, it is suggested to look into pytest or unittest (python) and testthat (R).

While the script might run on a specific date, it is paramount to organise your R or Python scripts so that they are reproducible on any date without amending the code.

IMPORTANT: in order to complete the Coursework Two assignments, the student needs to fetch and merge the master branch into it's personal local folder and re-build the mongo_seed container:

```
docker compose up --build mongo_seed

```

Do not copy databases in other folders. There is one source only for databases  and this is in folder 000.Database.

In addition, un-stage any change to 000.Database folder before committing to Git.

### Report

Along side to code developments, the student must write a report (10,000 Words max) that will be submitted in Turnitin according to the deadlines specified at the top of this page.

The report should be structured with:

1. Introduction;
2. Section 2. Present business case, challenges and data;
3. Section 3. Present the solution to the challenge:
  What are the possible approaches (literature review, model selection),
  Which approach is used and why it is preferable among others,
  Implementation,
5. Results.
6. Conclusion: conclude the work and summarise the key findings.

In the report headers please make sure to include your student number only as needs to link to your dev folder in the bitbucket repository.

### Marking Criteria

The marking criteria of this coursework is as follows:

1. Clear definition and structuring of data pipelines (20% of Total).
2. The submitted Code respects best practices, is well organised, reproducible and flexible to cater for different usages  (35% of total).
3. The quantitative model implementation is independent and innovative (35% of total);
4. Write final report based on the given instructions and structure (10% of Total).


## Coursework One
[Published 19/02/2024 11:00:00]


### Objectives

Coursework One has three objectives:

- demonstrate familiarity with Git workflow by submitting the main queries into Bitbucket;
- demonstrate understanding of docker technology;
- demonstrate familiarity with both SQL and NoSQL MongoDB syntax for querying data.


### Sql and NoSql database for coursework one

In order to complete this coursework, the student must use the databases stored in [iftcoursework2023](https://bitbucket.org/uceslc0/iftcoursework2023/src/master/) under folder 000.DataBases. 

All databases will be setup and launched by docker compose file in the root directory of this repository.

In order to set-up the tools needed, please cd in the root directory of this repo and execute the command : `docker compose up --build`.

All databases and softwares will be set up in docker container and will be exposed as per docker-compose.yml specs. Please, read carefully docker compose file to identify the specification of the software needed.



### Requirements

The student should develop at least two queries for each SQL and NoSQL database. The complexity and sophistication of the query is left at student discretion.


#### Code Submission

For each coursework submission code must be submitted in bitbucket. The repository for submission is [iftcoursework2023](https://bitbucket.org/uceslc0/iftcoursework2023/src/master/).

In order to submit the coursework, the student needs to follow the following steps:

1. Clone the repository;
2. create a new branch;
3. add your own developments in a dedicated folder;
4. the dedicated folder has to be placed under "./iftcoursework2023/" and is structured as following:

```
Student_<insert your student number>
    ├── CHANGELOG.md
    ├── 1.CourseworkOne/
        ├── 1.SQLQueries.sql
        ├── 2.NoSQLQueries.js
        ├── README.md
        └── .gitkeep
    ├── 2.CourseworkTwo/
        └── .gitkeep   
```

*Please see example under this directory for folder name called "Student_00000000"*

Two files for Coursework One submission will then be placed under 1.CourseworkOne with following naming conventions:

* "1.SQLQueries.sql"
* "2.NoSQLQueries.js"
* "README.md"

Once this is completed, in order to submit the code to Bitbucket:

1. check git status;
2. if the local repository is behind the master, please perform a git pull;
3. add & commit;
4. push the origin to the branch;
5. go to bitbucket and create a pull request by merging your branch into the master.



#### Report

Along side to code developments, the student must write a report (10,000 Words max) that will be submitted in Turnitin according to the deadlines specified at the top of this page. 

The report should be structured as following:

1. Short Introduction;
2. Brief description of SQL vs NoSQL database;
3. Query documentation: for each query provided, please list: 
   1. background (why I need this query), 
   2. aims (what I will achieve with my query), 
   3. approach (how I addressed the challenge and what each statement does), 
   4. output (describe main results obtained).
4. Conclusion: conclude the work and summary of key findings.

In the report headers please make sure to include your *student number* only as needs to link to your dev folder in the bitbucket repository.


#### Marking Criteria

The marking criteria of this coursework is as follows:

1. Understanding of Git workflow - create branch, push code to Bitbucket, create a pull request and successfully merge code commit into the master branch (20% of Total).
2. Understanding of Docker infrastructure (5% of total).
3. Understanding of SQL language by writing two queries (35% of Total);
4. Understanding of NoSQL language (MongoDB) by writing two queries (35% of Total).
5. Write final report based on the given instructions and structure (5% of Total).
