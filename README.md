# UCL - IFT Big Data Quantitative Finance Coursework
- [UCL - IFT Big Data Quantitative Finance Coursework](#ucl---ift-big-data-quantitative-finance-coursework)
  - [Coursework One](#coursework-one)
    - [Objectives](#objectives)
    - [Sql and NoSql database for coursework one](#sql-and-nosql-database-for-coursework-one)
    - [Requirements](#requirements)
      - [Code Submission](#code-submission)
      - [Report](#report)


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

For each coursework submission code must be submitted in bitbucket. The repository for submission is (iftcoursework2023)[https://bitbucket.org/uceslc0/iftcoursework2023/src/master/].

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

Along side to code developments, the student must write a report (1000 Words max) that will be submitted in Turnitin according to the deadlines specified at the top of this page. 

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
