-- Create the table Customers

create table Customers ( name varchar(20)  );


-- Insert records into the Customers table
INSERT INTO Customers (FirstName, Surname, Address) VALUES
('Joe', 'Murphy', 'Dundalk'),
('Ann', 'Glynn', 'Ardee'),
('Sam', 'Neary', 'Drogheda'),
('Tim', 'Woolworth', 'Dundalk'),
('Audrey', 'White', 'Blackrock'),
('Vera', 'Nolan', 'Ardee'),
('Harry', 'Scully', 'Dundalk'),
('Bob', 'Green', 'Drogheda');

-- All customers who live in 'Ardee'
SELECT * FROM Customer WHERE Address = 'Ardee';


-- All customers with the first name 'Harry' or the surname 'White'
SELECT * FROM Customer WHERE FirstName = 'Harry' OR Surname = 'White';


-- The first name and surname of all customers who live in 'Blackrock'
SELECT FirstName, Surname FROM Customer WHERE Address = 'Blackrock';


-- The first name and surname of all customers whose address starts with the letter 'D'
SELECT FirstName, Surname FROM Customer WHERE Address LIKE 'D%';

-- All customers whose surname starts with the letter 'G' and who live in 'Ardee'
SELECT * FROM Customer WHERE Surname LIKE 'G%' AND Address = 'Ardee';

-- The address of the customer with the first name 'Tim' and surname 'Woolworth'
SELECT Address FROM Customer WHERE FirstName = 'Tim' AND Surname = 'Woolworth';
