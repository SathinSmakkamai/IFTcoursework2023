/*
Author: Sathin Smakkamai
Student number: 22209837
Date: 15/03/2024
Content: NoSQL - MongoDB Queries for CourseWork One
*/

// -----------------------------------------------------------------------------------------------------
// -- Query 1: Find the top 10 large-market-cap equities with the highest dividend yield  --------------
// -----------------------------------------------------------------------------------------------------

// query using Static collection
// db.Static.find({ "MarketCap": { $gt: 10000 } }).sort({ "DividendYield": -1 }).limit(10)
db.Static.find({
    // constrain on market cap size
    "MarketCap": { $gt: 10000 }})
    // Sort on dividend yield, and order in descend
    .sort({ "DividendYield": -1 })
    // get top 10 output
    .limit(10)

// query using NestedStatic collection
// db.NestedStatic.find({ "MarketData.MarketCap": { $gt: 10000 } }).sort({ "FinancialRatios.DividendYield": -1 }).limit(10)
db.NestedStatic.find({
    // constrain on market cap size
    "MarketData.MarketCap": { $gt: 10000 } } )
    // Sort on dividend yield, and order in descend
    .sort({ "FinancialRatios.DividendYield": -1 })
    // get top 10 output
    .limit(10)

// -----------------------------------------------------------------------------------------------------
// -- Query 2: Get the total market capitalization for each subsector in the Industrial sector ---------
// -----------------------------------------------------------------------------------------------------

// query using Static collection
// db.Static.aggregate([{ $match: { GICSSector: 'Industrials' } }, { $group: { _id: "$GICSSubIndustry", totalMarketCap: { $sum: "$MarketCap" } } }, { $sort: { totalMarketCap: -1 } }])
db.Static.aggregate([
    // Match documents with GICSSector equal to 'Industrials'
    { $match: { GICSSector: 'Industrials' } },
    // Group by GICSSubIndustry and calculate the sum of MarketCap
    { $group: { _id: "$GICSSubIndustry",
            // get the total marketcap by using "$sum"
            totalMarketCap: { $sum: "$MarketCap" } } },
    // Sort the results by totalMarketCap in descending order
    { $sort: { totalMarketCap: -1 } } ])

// query using NestedStatic collection
// db.NestedStatic.aggregate([{ $match: { "StaticData.GICSSector": 'Industrials' } }, { $group: { _id: "$StaticData.GICSSubIndustry", totalMarketCap: { $sum: "$MarketData.MarketCap" } } }, { $sort: { totalMarketCap: -1 } }])
db.NestedStatic.aggregate([
    // Match documents with GICSSector equal to 'Industrials'
    { $match: { "StaticData.GICSSector": 'Industrials' } },
    // Group by GICSSubIndustry and calculate the sum of MarketCap
    { $group: { _id: "$StaticData.GICSSubIndustry",
            // get the total marketcap by using "$sum"
            totalMarketCap: { $sum: "$MarketData.MarketCap" } } },
    // Sort the results by totalMarketCap in descending order
    { $sort: { totalMarketCap: -1 } } ])

// -----------------------------------------------------------------------------------------------------
// -- Query 3: Get the number of equities in each sector -----------------------------------------------
// -----------------------------------------------------------------------------------------------------

// query using Static collection
// db.Static.aggregate([{ $group: { _id: "$GICSSector", count: { $sum: 1 } } }, { $sort: { count: -1 } }])
db.Static.aggregate([
    // Group by Sector
    { $group: { _id: "$GICSSector",
            // count
            count: { $sum: 1 } } },
    // Sort the result order in descend
    { $sort: { count: -1 } } ])

// query using NestedStatic collection
// db.NestedStatic.aggregate([{ $group: { _id: "$StaticData.GICSSector", count: { $sum: 1 } } }, { $sort: { count: -1 } }])
db.NestedStatic.aggregate([
    // Group by Sector
    { $group: { _id: "$StaticData.$GICSSector",
            // count
            count: { $sum: 1 } } },
    // Sort the result order in descend
    { $sort: { count: -1 } } ])
