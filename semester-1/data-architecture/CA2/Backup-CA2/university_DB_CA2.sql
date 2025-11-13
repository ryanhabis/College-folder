-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 11, 2025 at 04:38 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `university_DB_CA2`
--

-- --------------------------------------------------------

--
-- Table structure for table `Courses`
--

CREATE TABLE `Courses` (
  `CourseID` int(11) NOT NULL,
  `CourseName` varchar(100) NOT NULL,
  `Credits` int(11) DEFAULT NULL,
  `InstructorID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Courses`
--

INSERT INTO `Courses` (`CourseID`, `CourseName`, `Credits`, `InstructorID`) VALUES
(101, 'Database Systems', 5, 1),
(102, 'Quantum Mechanics', 10, 2),
(103, 'Calculus I', 5, 3),
(104, 'Evolutionary Biology', 5, 4),
(105, 'Organic Chemistry', 10, 5);

-- --------------------------------------------------------

--
-- Table structure for table `Enrolments`
--

CREATE TABLE `Enrolments` (
  `EnrolmentID` int(11) NOT NULL,
  `StudentID` int(11) DEFAULT NULL,
  `CourseID` int(11) DEFAULT NULL,
  `EnrolmentDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Enrolments`
--

INSERT INTO `Enrolments` (`EnrolmentID`, `StudentID`, `CourseID`, `EnrolmentDate`) VALUES
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

-- --------------------------------------------------------

--
-- Table structure for table `Instructors`
--

CREATE TABLE `Instructors` (
  `InstructorID` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Department` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Instructors`
--

INSERT INTO `Instructors` (`InstructorID`, `Name`, `Email`, `Department`) VALUES
(1, 'Dr. Alan Turing', 'alan@uni.com', 'Computer Science'),
(2, 'Dr. Marie Curie', 'marie@uni.com', 'Physics'),
(3, 'Dr. Isaac Newton', 'isaac@uni.com', 'Mathematics'),
(4, 'Dr. Charles Darwin', 'charles@uni.com', 'Biology'),
(5, 'Dr. Rosalind Franklin', 'rosalind@uni.com', 'Chemistry');

-- --------------------------------------------------------

--
-- Table structure for table `Students`
--

CREATE TABLE `Students` (
  `StudentID` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `DOB` date DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Students`
--

INSERT INTO `Students` (`StudentID`, `Name`, `DOB`, `Email`, `Phone`) VALUES
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

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Courses`
--
ALTER TABLE `Courses`
  ADD PRIMARY KEY (`CourseID`),
  ADD KEY `InstructorID` (`InstructorID`);

--
-- Indexes for table `Enrolments`
--
ALTER TABLE `Enrolments`
  ADD PRIMARY KEY (`EnrolmentID`),
  ADD KEY `StudentID` (`StudentID`),
  ADD KEY `CourseID` (`CourseID`);

--
-- Indexes for table `Instructors`
--
ALTER TABLE `Instructors`
  ADD PRIMARY KEY (`InstructorID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `Students`
--
ALTER TABLE `Students`
  ADD PRIMARY KEY (`StudentID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Courses`
--
ALTER TABLE `Courses`
  ADD CONSTRAINT `Courses_ibfk_1` FOREIGN KEY (`InstructorID`) REFERENCES `Instructors` (`InstructorID`);

--
-- Constraints for table `Enrolments`
--
ALTER TABLE `Enrolments`
  ADD CONSTRAINT `Enrolments_ibfk_1` FOREIGN KEY (`StudentID`) REFERENCES `Students` (`StudentID`),
  ADD CONSTRAINT `Enrolments_ibfk_2` FOREIGN KEY (`CourseID`) REFERENCES `Courses` (`CourseID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
