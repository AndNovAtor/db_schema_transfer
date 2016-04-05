CREATE TABLE "Employees" (
    EmployeeID int(None), 
    LastName varchar(20), 
    FirstName varchar(10), 
    Title varchar(30), 
    TitleOfCourtesy varchar(25), 
    BirthDate timestamp(None), 
    HireDate timestamp(None), 
    Address varchar(60), 
    City varchar(15), 
    Region varchar(15), 
    PostalCode varchar(10), 
    Country varchar(15), 
    HomePhone varchar(24), 
    Extension varchar(4), 
    Photo bytea(2147483647), 
    Notes text(1073741823), 
    ReportsTo int(None), 
    PhotoPath varchar(255), 
    PRIMARY KEY(EmployeeID)
);


CREATE TABLE "Categories" (
    CategoryID int(None), 
    CategoryName varchar(15), 
    Description text(1073741823), 
    Picture bytea(2147483647), 
    PRIMARY KEY(CategoryID)
);


CREATE TABLE "Customers" (
    CustomerID nchar(5), 
    CompanyName varchar(40), 
    ContactName varchar(30), 
    ContactTitle varchar(30), 
    Address varchar(60), 
    City varchar(15), 
    Region varchar(15), 
    PostalCode varchar(10), 
    Country varchar(15), 
    Phone varchar(24), 
    Fax varchar(24), 
    PRIMARY KEY(CustomerID)
);


CREATE TABLE "Shippers" (
    ShipperID int(None), 
    CompanyName varchar(40), 
    Phone varchar(24), 
    PRIMARY KEY(ShipperID)
);


CREATE TABLE "Suppliers" (
    SupplierID int(None), 
    CompanyName varchar(40), 
    ContactName varchar(30), 
    ContactTitle varchar(30), 
    Address varchar(60), 
    City varchar(15), 
    Region varchar(15), 
    PostalCode varchar(10), 
    Country varchar(15), 
    Phone varchar(24), 
    Fax varchar(24), 
    HomePage text(1073741823), 
    PRIMARY KEY(SupplierID)
);


CREATE TABLE "Orders" (
    OrderID int(None), 
    CustomerID nchar(5), 
    EmployeeID int(None), 
    OrderDate timestamp(None), 
    RequiredDate timestamp(None), 
    ShippedDate timestamp(None), 
    ShipVia int(None), 
    Freight money(None), 
    ShipName varchar(40), 
    ShipAddress varchar(60), 
    ShipCity varchar(15), 
    ShipRegion varchar(15), 
    ShipPostalCode varchar(10), 
    ShipCountry varchar(15), 
    PRIMARY KEY(OrderID)
);


CREATE TABLE "Products" (
    ProductID int(None), 
    ProductName varchar(40), 
    SupplierID int(None), 
    CategoryID int(None), 
    QuantityPerUnit varchar(20), 
    UnitPrice money(None), 
    UnitsInStock smallint(None), 
    UnitsOnOrder smallint(None), 
    ReorderLevel smallint(None), 
    Discontinued boolean(None), 
    PRIMARY KEY(ProductID)
);


CREATE TABLE "Order Details" (
    OrderID int(None), 
    ProductID int(None), 
    UnitPrice money(None), 
    Quantity smallint(None), 
    Discount real(None), 
    PRIMARY KEY(OrderID, ProductID)
);


CREATE TABLE "CustomerCustomerDemo" (
    CustomerID nchar(5), 
    CustomerTypeID nchar(10), 
    PRIMARY KEY(CustomerID, CustomerTypeID)
);


CREATE TABLE "CustomerDemographics" (
    CustomerTypeID nchar(10), 
    CustomerDesc text(1073741823), 
    PRIMARY KEY(CustomerTypeID)
);


CREATE TABLE "Region" (
    RegionID int(None), 
    RegionDescription nchar(50), 
    PRIMARY KEY(RegionID)
);


CREATE TABLE "Territories" (
    TerritoryID varchar(20), 
    TerritoryDescription nchar(50), 
    RegionID int(None), 
    PRIMARY KEY(TerritoryID)
);


CREATE TABLE "EmployeeTerritories" (
    EmployeeID int(None), 
    TerritoryID varchar(20), 
    PRIMARY KEY(EmployeeID, TerritoryID)
);


ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (EmployeeID) REFERENCES "Employees" ;
ALTER TABLE "EmployeeTerritories" ADD FOREIGN KEY (TerritoryID) REFERENCES "Territories" ;
