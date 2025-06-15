SELECT
  SalesOrderID,
  DATEDIFF(DAY, OrderDate, ShipDate) AS DeliveryDays,
  TerritoryID,
  SalesPersonID
FROM Sales.SalesOrderHeader
WHERE ShipDate IS NOT NULL;