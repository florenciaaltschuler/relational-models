
-- Coordenadas de cada tienda
WITH Tiendas AS (
    SELECT 
        s.BusinessEntityID,
        s.Name AS StoreName,
        a.SpatialLocation AS StoreLocation,
        a.City AS StoreCity,
        sp.Name AS StoreState
    FROM Sales.Store s
    JOIN Person.BusinessEntityAddress bea ON s.BusinessEntityID = bea.BusinessEntityID
    JOIN Person.Address a ON bea.AddressID = a.AddressID
    JOIN Person.StateProvince sp ON a.StateProvinceID = sp.StateProvinceID
    WHERE a.SpatialLocation IS NOT NULL
),

-- Ventas con dirección de envío
Ventas AS (
    SELECT 
        h.SalesOrderID,
        c.StoreID,
        a.SpatialLocation AS DeliveryLocation,
        a.City AS DeliveryCity,
        sp.Name AS DeliveryState
    FROM Sales.SalesOrderHeader h
    JOIN Sales.Customer c ON h.CustomerID = c.CustomerID
    JOIN Person.Address a ON h.ShipToAddressID = a.AddressID
    JOIN Person.StateProvince sp ON a.StateProvinceID = sp.StateProvinceID
    WHERE c.StoreID IS NOT NULL AND a.SpatialLocation IS NOT NULL
)

-- Calcular distancia entre tienda y dirección de envío
SELECT 
    t.StoreName,
    t.StoreCity,
    t.StoreState,
    v.SalesOrderID,
    v.DeliveryCity,
    v.DeliveryState,
    t.StoreLocation.Lat AS StoreLat,
    t.StoreLocation.Long AS StoreLong,
    v.DeliveryLocation.Lat AS DeliveryLat,
    v.DeliveryLocation.Long AS DeliveryLong,
    t.StoreLocation.STDistance(v.DeliveryLocation) / 1000.0 AS DistanceKm
FROM Ventas v
JOIN Tiendas t ON v.StoreID = t.BusinessEntityID;
