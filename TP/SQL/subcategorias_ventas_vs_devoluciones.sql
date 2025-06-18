-- Subcategorías con productos vendidos
WITH SubcatsWithSales AS (
    SELECT DISTINCT ps.ProductSubcategoryID
    FROM Sales.SalesOrderDetail sod
    JOIN Production.Product p ON sod.ProductID = p.ProductID
    JOIN Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
),

-- Subcategorías con productos devueltos (ventas con razón de devolución)
SubcatsWithReturns AS (
    SELECT DISTINCT ps.ProductSubcategoryID
    FROM Sales.SalesOrderDetail sod
    JOIN Production.Product p ON sod.ProductID = p.ProductID
    JOIN Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
    JOIN Sales.SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
    JOIN Sales.SalesOrderHeaderSalesReason sr ON soh.SalesOrderID = sr.SalesOrderID
)

-- Comparación final
SELECT
    (SELECT COUNT(*) FROM SubcatsWithSales) AS SubcategoriesWithSales,
    (SELECT COUNT(*) FROM SubcatsWithReturns) AS SubcategoriesWithReturns;