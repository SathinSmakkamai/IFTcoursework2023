/*
Author: Sathin Smakkamai
Student number: 22209837
Date: 15/03/2024
Content: NoSQL - MongoDB Queries for CourseWork One
*/

// -----------------------------------------------------------------------------------------------------
// -- Query 1: Find Equity in the Energy Sector with Some Constraints ----------------------------------
// -----------------------------------------------------------------------------------------------------

// db.CourseworkOne.find({"StaticData.GICSSector": "Energy", "MarketData.MarketCap": { $gt: 10000 }, "MarketData.Beta": { $gte: 0.7, $lte: 1.3 }, "FinancialRatios.DividendYield": { $gt: 5.0 }})
db.CourseworkOne.find({
    // find equity from Energy sector
    "StaticData.GICSSector": "Energy",
    // constrain on market cap size (>10000)
    "MarketData.MarketCap": { $gt: 10000 },
    // constrain on beta (between 0.7 and 1.3)
    "MarketData.Beta": { $gte: 0.7, $lte: 1.3 },
    // constrain on dividend yield (>5.0)
    "FinancialRatios.DividendYield": { $gt: 5.0 } })

// -----------------------------------------------------------------------------------------------------
// -- Query 2: Find the top 10 large-market-cap Equities with the highest dividend yield  --------------
// -----------------------------------------------------------------------------------------------------

// db.CourseworkOne.find({"MarketData.MarketCap": { $gt: 10000 }}).sort({"FinancialRatios.DividendYield": -1 }).limit(10)
db.CourseworkOne.find({
    // constrain on market cap size
    "MarketData.MarketCap": { $gt: 10000 } })
    // Sort on dividend yield, and order in descend
    .sort({ "FinancialRatios.DividendYield": -1 })
    // get top 10 output
    .limit(10)

// -----------------------------------------------------------------------------------------------------
// -- Query 3: Find the top 5 equities from either the energy sector or the consumer discretionary -----
// -----------------------------------------------------------------------------------------------------

// db.CourseworkOne.find({ $and: [{ $or: [{ "StaticData.GICSSector": "Energy" }, { "StaticData.GICSSector": "Consumer Discretionary" }] }, { "MarketData.Beta": { $gt: 0.7 } }] }).sort({ "MarketData.Beta": -1 }).limit(5)
db.CourseworkOne.find({
    // filter by 2 conditions using $and
    $and: [
        // 1st condition: find equity from either energy sector or consumer discretionary sector, by using $or
        { $or: [{ "StaticData.GICSSector": "Energy" }, { "StaticData.GICSSector": "Consumer Discretionary" } ] },
        // 2nd condition: beta more than 0.7
        { "MarketData.Beta": { $gt: 0.7 } } ]})
    // Sort on Beta, and order in descend
    .sort({ "MarketData.Beta": -1})
    // get top 5 output
    .limit(5)

// -----------------------------------------------------------------------------------------------------
// -- Query 4: Get the total market capitalization for each sub-sector in the Industrial sector --------
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
// -- Query 5: Get the number of equities in each sector -----------------------------------------------
// -----------------------------------------------------------------------------------------------------

// db.CourseworkOne.aggregate([{ $group: { _id: "$StaticData.GICSSector", count: { $sum: 1 } } }, { $sort: { count: -1 } }])
db.CourseworkOne.aggregate([
    // Group by Sector
    { $group: { _id: "$ StaticData.GICSSector",
            // count
            count: { $sum: 1 } } },
    // Sort the result order in descend
    { $sort: { count: -1 } } ])

