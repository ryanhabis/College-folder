-- Students Table
CREATE TABLE Students (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    DOB DATE,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15)
);

-- Instructors Table
CREATE TABLE Instructors (
    InstructorID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Department VARCHAR(50)
);

-- Courses Table
CREATE TABLE Courses (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(100) NOT NULL,
    Credits INT,
    InstructorID INT,
    FOREIGN KEY (InstructorID) REFERENCES Instructors(InstructorID)
);

-- Enrolments Table
CREATE TABLE Enrolments (
    EnrolmentID INT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    EnrolmentDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Insert sample data

INSERT INTO Students VALUES
(1, 'Alice Brown', '2000-05-14', 'alice@email.com', '1234567890'),
(2, 'Bob Smith', '1999-08-21', 'bob@email.com', '1234567891'),
(3, 'Charlie Green', '2001-02-10', 'charlie@email.com', '1234567892'),
(4, 'Diana White', '2000-11-30', 'diana@email.com', '1234567893'),
(5, 'Eve Black', '1998-07-05', 'eve@email.com', '1234567894'),
(6, 'Frank Blue', '2002-03-18', 'frank@email.com', '1234567895'),
(7, 'Grace Red', '2001-09-22', 'grace@email.com', '1234567896'),
(8, 'Henry Yellow', '1999-12-25', 'henry@email.com', '1234567897'),
(9, 'Ivy Pink', '2000-04-08', 'ivy@email.com', '1234567898'),
(10, 'Jack Purple', '2001-06-12', 'jack@email.com', '1234567899');

INSERT INTO Instructors VALUES
(1, 'Dr. Alan Turing', 'alan@uni.com', 'Computer Science'),
(2, 'Dr. Marie Curie', 'marie@uni.com', 'Physics'),
(3, 'Dr. Isaac Newton', 'isaac@uni.com', 'Mathematics'),
(4, 'Dr. Charles Darwin', 'charles@uni.com', 'Biology'),
(5, 'Dr. Rosalind Franklin', 'rosalind@uni.com', 'Chemistry');

INSERT INTO Courses VALUES
(101, 'Database Systems', 5, 1),
(102, 'Quantum Mechanics', 10, 2),
(103, 'Calculus I', 5, 3),
(104, 'Evolutionary Biology', 5, 4),
(105, 'Organic Chemistry', 10, 5);

INSERT INTO Enrolments VALUES
(1, 1, 101, '2024-01-15'),
(2, 2, 101, '2024-01-16'),
(3, 3, 102, '2024-01-17'),
(4, 4, 102, '2024-01-18'),
(5, 5, 103, '2024-01-19'),
(6, 6, 103, '2024-01-20'),
(7, 7, 104, '2024-01-21'),
(8, 8, 104, '2024-01-22'),
(9, 9, 105, '2024-01-23'),
(10, 10, 105, '2024-01-24'),
(11, 1, 102, '2024-01-25'),
(12, 2, 103, '2024-01-26'),
(13, 3, 104, '2024-01-27'),
(14, 4, 105, '2024-01-28'),
(15, 5, 101, '2024-01-29');