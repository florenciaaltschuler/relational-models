WITH
    DateRange
    AS
    (
        SELECT
            MIN(OrderDate) AS MinDate,
            MAX(OrderDate) AS MaxDate
        FROM Sales.SalesOrderHeader
    ),
    -- Generate all months between min/max dates
    AllMonths
    AS
    (
                    SELECT
                DATEFROMPARTS(YEAR(MinDate), MONTH(MinDate), 1) AS MonthStart
            FROM DateRange
        UNION ALL
            SELECT
                DATEADD(MONTH, 1, MonthStart)
            FROM AllMonths
            WHERE DATEADD(MONTH, 1, MonthStart) <= (SELECT MaxDate
            FROM DateRange)
    ),
    -- Get distinct territories
    AllTerritories
    AS
    (
        SELECT
            TerritoryID,
            Name AS TerritoryName
        FROM Sales.SalesTerritory
    ),
    -- Calculate monthly sales per territory
    MonthlySales
    AS
    (
        SELECT
            h.TerritoryID,
            DATEFROMPARTS(YEAR(h.OrderDate), MONTH(h.OrderDate), 1) AS MonthStart,
            SUM(h.TotalDue) AS TotalSales
        FROM Sales.SalesOrderHeader h
        GROUP BY 
        h.TerritoryID,
        YEAR(h.OrderDate),
        MONTH(h.OrderDate)
    )
-- Combine all territories with all months
SELECT
    t.TerritoryName,
    m.MonthStart,
    COALESCE(s.TotalSales, 0) AS TotalSales
FROM AllTerritories t
CROSS JOIN AllMonths m
    LEFT JOIN MonthlySales s
    ON t.TerritoryID = s.TerritoryID
        AND m.MonthStart = s.MonthStart
ORDER BY 
    t.TerritoryName, 
    m.MonthStart
OPTION
(MAXRECURSION
0); -- Allows unlimited date generation
