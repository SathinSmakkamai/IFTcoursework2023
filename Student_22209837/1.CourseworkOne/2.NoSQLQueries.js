/*
Author: Sathin Smakkamai
Student number: 22209837
Date: 15/03/2024
Content: NoSQL - MongoDB Queries for CourseWork One
*/

// -----------------------------------------------------------------------------------------------------
// -- Query 1: Find the top 10 large-market-cap equities with the highest dividend yield  --------------
// -----------------------------------------------------------------------------------------------------

// db.CourseworkOne.find({"MarketData.MarketCap": { $gt: 10000 }}).sort({"FinancialRatios.DividendYield": -1 }).limit(10)
db.CourseworkOne.find({
    // constrain on market cap size
    "MarketData.MarketCap": { $gt: 10000 }})
    // Sort on dividend yield, and order in descend
    .sort({ "FinancialRatios.DividendYield": -1 })
    // get top 10 output
    .limit(10)

// -----------------------------------------------------------------------------------------------------
// -- Query 2: Get the total market capitalization for each sub-sector in the Industrial sector --------
// -----------------------------------------------------------------------------------------------------

// db.CourseworkOne.aggregate([{ $match: { "StaticData.GICSSector": 'Industrials' } }, { $group: { _id: "$StaticData.GICSSubIndustry", totalMarketCap: { $sum: "$MarketData.MarketCap" } } }, { $sort: { totalMarketCap: -1 } }])
db.CourseworkOne.aggregate([
    // Match documents with GICSSector equal to 'Industrials'
    { $match: { "StaticData.GICSSector": 'Industrials' } },
    // Group by GICSSubIndustry and calculate the sum of MarketCap
    { $group: { _id: "$StaticData.GICSSubIndustry",
            // get the total Marketcap by using "$sum"
            totalMarketCap: { $sum: "$MarketData.MarketCap" } } },
    // Sort the results by totalMarketCap in descending order
    { $sort: { totalMarketCap: -1 } }])

// -----------------------------------------------------------------------------------------------------
// -- Query 3: Get the number of equities in each sector -----------------------------------------------
// -----------------------------------------------------------------------------------------------------

// db.CourseworkOne.aggregate([{ $group: { _id: "$StaticData.GICSSector", count: { $sum: 1 } } }, { $sort: { count: -1 } }])
db.CourseworkOne.aggregate([
    // Group by Sector
    { $group: { _id: "$ StaticData.GICSSector",
            // count
            count: { $sum: 1 } } },
    // Sort the result order in descend
    { $sort: { count: -1 } } ])

