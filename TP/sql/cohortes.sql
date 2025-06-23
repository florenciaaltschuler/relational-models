WITH
    FirstOrder
    AS
    (
        SELECT
            soh.CustomerID,
            MIN(soh.OrderDate) AS FirstOrderDate
        FROM Sales.SalesOrderHeader soh
        GROUP BY soh.CustomerID
    ),
    FirstOrderDetails
    AS
    (
        SELECT
            fo.CustomerID,
            fo.FirstOrderDate,
            sod.SalesOrderDetailID,
            sod.ProductID,
            ROW_NUMBER() OVER (
            PARTITION BY fo.CustomerID 
            ORDER BY soh.OrderDate, sod.SalesOrderDetailID
        ) AS rn
        FROM FirstOrder fo
            JOIN Sales.SalesOrderHeader soh
            ON fo.CustomerID = soh.CustomerID
                AND fo.FirstOrderDate = soh.OrderDate
            JOIN Sales.SalesOrderDetail sod
            ON soh.SalesOrderID = sod.SalesOrderID
    ),
    FirstPurchase
    AS
    (
        SELECT
            fod.CustomerID,
            fod.FirstOrderDate,
            FORMAT(fod.FirstOrderDate, 'yyyy-MM') AS CohortMonth,
            pc.Name AS FirstCategory,
            cr.Name AS CountryName,
            CASE WHEN c.StoreID IS NOT NULL THEN 'B2B' ELSE 'B2C' END AS CustomerType
        FROM FirstOrderDetails fod
            JOIN Production.Product p
            ON fod.ProductID = p.ProductID
            JOIN Production.ProductSubcategory psc
            ON p.ProductSubcategoryID = psc.ProductSubcategoryID
            JOIN Production.ProductCategory pc
            ON psc.ProductCategoryID = pc.ProductCategoryID
            LEFT JOIN Sales.Customer c
            ON fod.CustomerID = c.CustomerID
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
        WHERE fod.rn = 1
    ),
    CohortOrders
    AS
    (
        SELECT
            soh.CustomerID,
            soh.OrderDate,
            sod.LineTotal AS OrderAmount,
            fp.FirstOrderDate,
            fp.CohortMonth,
            fp.FirstCategory,
            fp.CountryName,
            fp.CustomerType,
            DATEDIFF(MONTH, fp.FirstOrderDate, soh.OrderDate) AS MonthsAfterFirstOrder,
            pc.Name AS OrderCategory
        FROM Sales.SalesOrderHeader soh
            JOIN Sales.SalesOrderDetail sod
            ON soh.SalesOrderID = sod.SalesOrderID
            JOIN Production.Product prod
            ON sod.ProductID = prod.ProductID
            JOIN Production.ProductSubcategory psc
            ON prod.ProductSubcategoryID = psc.ProductSubcategoryID
            JOIN Production.ProductCategory pc
            ON psc.ProductCategoryID = pc.ProductCategoryID
            INNER JOIN FirstPurchase fp
            ON soh.CustomerID = fp.CustomerID
    ),
    CohortSizes
    AS
    (
        SELECT
            CohortMonth,
            FirstCategory,
            CountryName,
            CustomerType,
            COUNT(DISTINCT CustomerID) AS CohortSize
        FROM FirstPurchase
        GROUP BY CohortMonth, FirstCategory, CountryName, CustomerType
    )
SELECT
    co.CohortMonth,
    co.MonthsAfterFirstOrder,
    co.FirstCategory,
    co.CountryName,
    co.CustomerType,
    COUNT(DISTINCT co.CustomerID) AS ActiveCustomers,
    FORMAT(1.0 * COUNT(DISTINCT co.CustomerID) / MAX(cs.CohortSize), 'P2') AS RetentionRate,
    SUM(co.OrderAmount) AS TotalSpending,
    COUNT(DISTINCT CASE WHEN co.OrderCategory <> co.FirstCategory THEN co.CustomerID END) AS CrossCategoryBuyers,
    FORMAT(1.0 * COUNT(DISTINCT CASE WHEN co.OrderCategory <> co.FirstCategory THEN co.CustomerID END) 
           / COUNT(DISTINCT co.CustomerID), 'P2') AS CrossCategoryRate,
    AVG(co.OrderAmount) AS AvgOrderValue
FROM CohortOrders co
    JOIN CohortSizes cs
    ON co.CohortMonth = cs.CohortMonth
        AND co.FirstCategory = cs.FirstCategory
        AND co.CountryName = cs.CountryName
        AND co.CustomerType = cs.CustomerType
WHERE co.MonthsAfterFirstOrder >= 0
GROUP BY 
    co.CohortMonth,
    co.MonthsAfterFirstOrder,
    co.FirstCategory,
    co.CountryName,
    co.CustomerType
ORDER BY 
    co.CohortMonth,
    co.MonthsAfterFirstOrder,
    co.FirstCategory,
    co.CountryName;