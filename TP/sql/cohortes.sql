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
                WHEN cr.Name IN ('United States', 'Canada') THEN 'North America'
                WHEN cr.Name IN ('United Kingdom', 'Germany', 'France') THEN 'Western Europe'
                ELSE 'Other'
            END AS Region,
            CASE 
                WHEN c.StoreID IS NOT NULL THEN 'B2B' 
                ELSE 'B2C' 
            END AS CustomerType
        FROM FirstOrder fo
            LEFT JOIN Sales.Customer c
            ON fo.CustomerID = c.CustomerID
            LEFT JOIN Person.Person per
            ON c.PersonID = per.BusinessEntityID
            LEFT JOIN Person.BusinessEntityAddress bea
            ON per.BusinessEntityID = bea.BusinessEntityID
            LEFT JOIN Person.Address a
            ON bea.AddressID = a.AddressID
            LEFT JOIN Person.StateProvince sp
            ON a.StateProvinceID = sp.StateProvinceID
            LEFT JOIN Person.CountryRegion cr
            ON sp.CountryRegionCode = cr.CountryRegionCode
    ),

    CohortSizes
    AS
    (
        SELECT
            CohortQuarter,
            Region,
            CustomerType,
            COUNT(DISTINCT CustomerID) AS CohortSize
        FROM FirstPurchase
        GROUP BY CohortQuarter, Region, CustomerType
        HAVING COUNT(DISTINCT CustomerID) >= 50
        -- mínimo tamaño
    ),

    CohortOrders
    AS
    (
        SELECT
            soh.CustomerID,
            soh.OrderDate,
            soh.TotalDue AS OrderAmount,
            fp.FirstOrderDate,
            fp.CohortQuarter,
            fp.Region,
            fp.CustomerType,
            DATEDIFF(MONTH, fp.FirstOrderDate, soh.OrderDate) AS MonthsAfterFirstOrder
        FROM Sales.SalesOrderHeader soh
            INNER JOIN FirstPurchase fp
            ON soh.CustomerID = fp.CustomerID
        WHERE EXISTS (
            SELECT 1
        FROM CohortSizes cs
        WHERE fp.CohortQuarter = cs.CohortQuarter
            AND fp.Region = cs.Region
            AND fp.CustomerType = cs.CustomerType
        )
    )

SELECT
    co.CohortQuarter,
    co.MonthsAfterFirstOrder,
    co.Region,
    co.CustomerType,
    COUNT(DISTINCT co.CustomerID) AS ActiveCustomers,
    FORMAT(1.0 * COUNT(DISTINCT co.CustomerID) / MAX(cs.CohortSize), 'P2') AS RetentionRate,
    SUM(co.OrderAmount) AS TotalSpending,
    AVG(co.OrderAmount) AS AvgOrderValue,
    MAX(cs.CohortSize) AS CohortSize
FROM CohortOrders co
    JOIN CohortSizes cs
    ON co.CohortQuarter = cs.CohortQuarter
        AND co.Region = cs.Region
        AND co.CustomerType = cs.CustomerType
WHERE co.MonthsAfterFirstOrder >= 0
GROUP BY 
    co.CohortQuarter,
    co.MonthsAfterFirstOrder,
    co.Region,
    co.CustomerType
ORDER BY 
    co.CohortQuarter,
    co.MonthsAfterFirstOrder,
    co.Region;