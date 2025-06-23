WITH
    FirstOrder
    AS
    (
        SELECT
            CustomerID,
            MIN(OrderDate) AS FirstOrderDate
        FROM Sales.SalesOrderHeader
        GROUP BY CustomerID
    ),
    FirstPurchase
    AS
    (
        SELECT
            fo.CustomerID,
            fo.FirstOrderDate,
            CONCAT(
            YEAR(fo.FirstOrderDate), 
            '-Q', 
            DATEPART(QUARTER, fo.FirstOrderDate)
        ) AS CohortQuarter,
            CASE 
            WHEN c.StoreID IS NOT NULL THEN 'B2B' 
            ELSE 'B2C' 
        END AS CustomerType
        FROM FirstOrder fo
            LEFT JOIN Sales.Customer c
            ON fo.CustomerID = c.CustomerID
    ),
    SalesReasons
    AS
    (
        SELECT
            soh.CustomerID,
            soh.SalesOrderID,
            sr.Name AS SalesReason
        FROM Sales.SalesOrderHeader soh
            JOIN Sales.SalesOrderHeaderSalesReason sohsr
            ON soh.SalesOrderID = sohsr.SalesOrderID
            JOIN Sales.SalesReason sr
            ON sohsr.SalesReasonID = sr.SalesReasonID
    ),
    CohortSizes
    AS
    (
        SELECT
            CohortQuarter,
            CustomerType,
            COUNT(DISTINCT CustomerID) AS CohortSize
        FROM FirstPurchase
        GROUP BY CohortQuarter, CustomerType
        HAVING COUNT(DISTINCT CustomerID) >= 50
    ),
    CohortOrders
    AS
    (
        SELECT
            soh.CustomerID,
            soh.SalesOrderID,
            soh.OrderDate,
            soh.TotalDue AS OrderAmount,
            fp.FirstOrderDate,
            fp.CohortQuarter,
            fp.CustomerType,
            DATEDIFF(MONTH, fp.FirstOrderDate, soh.OrderDate) AS MonthsAfterFirstOrder
        FROM Sales.SalesOrderHeader soh
            INNER JOIN FirstPurchase fp
            ON soh.CustomerID = fp.CustomerID
        WHERE EXISTS (
        SELECT 1
        FROM CohortSizes cs
        WHERE fp.CohortQuarter = cs.CohortQuarter
            AND fp.CustomerType = cs.CustomerType
    )
    ),
    ReasonStats
    AS
    (
        SELECT
            co.CohortQuarter,
            co.MonthsAfterFirstOrder,
            co.CustomerType,
            sr.SalesReason,
            COUNT(DISTINCT co.SalesOrderID) AS OrdersWithReason
        FROM CohortOrders co
            JOIN SalesReasons sr ON co.SalesOrderID = sr.SalesOrderID
        GROUP BY 
        co.CohortQuarter,
        co.MonthsAfterFirstOrder,
        co.CustomerType,
        sr.SalesReason
    ),
    TopReasons
    AS
    (
        SELECT
            CohortQuarter,
            MonthsAfterFirstOrder,
            CustomerType,
            SalesReason AS MostCommonReason,
            OrdersWithReason AS ReasonCount,
            ROW_NUMBER() OVER (
            PARTITION BY CohortQuarter, MonthsAfterFirstOrder, CustomerType
            ORDER BY OrdersWithReason DESC
        ) AS ReasonRank
        FROM ReasonStats
    )
SELECT
    co.CohortQuarter,
    co.MonthsAfterFirstOrder,
    co.CustomerType,
    COUNT(DISTINCT co.CustomerID) AS ActiveCustomers,
    FORMAT(1.0 * COUNT(DISTINCT co.CustomerID) / MAX(cs.CohortSize), 'P2') AS RetentionRate,
    SUM(co.OrderAmount) AS TotalSpending,
    AVG(co.OrderAmount) AS AvgOrderValue,
    MAX(cs.CohortSize) AS CohortSize,

    COUNT(DISTINCT co.SalesOrderID) AS TotalOrders,
    COUNT(DISTINCT sr.SalesOrderID) AS OrdersWithReason,
    tr.MostCommonReason,
    FORMAT(1.0 * tr.ReasonCount / COUNT(DISTINCT co.SalesOrderID), 'P2') AS MostCommonReasonPct
FROM CohortOrders co
    JOIN CohortSizes cs
    ON co.CohortQuarter = cs.CohortQuarter
        AND co.CustomerType = cs.CustomerType
    LEFT JOIN SalesReasons sr ON co.SalesOrderID = sr.SalesOrderID
    LEFT JOIN TopReasons tr
    ON co.CohortQuarter = tr.CohortQuarter
        AND co.MonthsAfterFirstOrder = tr.MonthsAfterFirstOrder
        AND co.CustomerType = tr.CustomerType
        AND tr.ReasonRank = 1
WHERE co.MonthsAfterFirstOrder >= 0
GROUP BY 
    co.CohortQuarter,
    co.MonthsAfterFirstOrder,
    co.CustomerType,
    tr.MostCommonReason,
    tr.ReasonCount
ORDER BY 
    co.CohortQuarter,
    co.MonthsAfterFirstOrder,
    co.CustomerType;