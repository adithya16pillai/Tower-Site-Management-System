-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 14, 2023 at 08:58 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tower_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `antennainfo`
--

CREATE TABLE `antennainfo` (
  `antenna_id` int(20) NOT NULL,
  `antenna_size` decimal(5,0) DEFAULT NULL,
  `bandwidth` decimal(5,0) DEFAULT NULL,
  `network_generation` int(1) DEFAULT NULL,
  `antenna_height` decimal(5,0) DEFAULT NULL,
  `antenna_azimuth` decimal(5,2) DEFAULT NULL CHECK (`antenna_azimuth` >= 0 and `antenna_azimuth` <= 180),
  `owner_id` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `maintainanceinfo`
--

CREATE TABLE `maintainanceinfo` (
  `tower_id` int(20) DEFAULT NULL,
  `last_maintained` date DEFAULT NULL,
  `next_maintainance` date DEFAULT NULL,
  `maintainance_type` char(1) DEFAULT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `ownerinfo`
--

CREATE TABLE `ownerinfo` (
  `owner_id` int(20) NOT NULL,
  `owner_name` char(20) DEFAULT NULL,
  `sites_owned` int(5) DEFAULT NULL,
  `towers_owned` int(5) DEFAULT NULL,
  `owner_contact` int(10) DEFAULT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `siteinfo`
--

CREATE TABLE `siteinfo` (
  `site_id` int(20) NOT NULL,
  `site_name` char(20) DEFAULT NULL,
  `site_cordinates` char(15) DEFAULT NULL,
  `site_address` char(40) DEFAULT NULL,
  `site_zip_code` int(6) DEFAULT NULL,
  `site_type` char(1) DEFAULT NULL,
  `owner_id` int(20) DEFAULT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `towerinfo`
--

CREATE TABLE `towerinfo` (
  `tower_id` int(20) NOT NULL,
  `tower_height` decimal(4,0) DEFAULT NULL,
  `date_of_installation` date DEFAULT NULL,
  `operator_name` char(20) DEFAULT NULL,
  `antenna_band` decimal(5,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `antennainfo`
--
ALTER TABLE `antennainfo`
  ADD PRIMARY KEY (`antenna_id`),
  ADD KEY `fk_antenna_owner` (`owner_id`);

--
-- Indexes for table `maintainanceinfo`
--
ALTER TABLE `maintainanceinfo`
  ADD KEY `fk_maintainance_tower_id` (`tower_id`);

--
-- Indexes for table `ownerinfo`
--
ALTER TABLE `ownerinfo`
  ADD PRIMARY KEY (`owner_id`);

--
-- Indexes for table `siteinfo`
--
ALTER TABLE `siteinfo`
  ADD PRIMARY KEY (`site_id`),
  ADD KEY `fk_site_owner` (`owner_id`);

--
-- Indexes for table `towerinfo`
--
ALTER TABLE `towerinfo`
  ADD PRIMARY KEY (`tower_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `antennainfo`
--
ALTER TABLE `antennainfo`
  ADD CONSTRAINT `fk_antenna_owner` FOREIGN KEY (`owner_id`) REFERENCES `ownerinfo` (`owner_id`) ON UPDATE CASCADE;

--
-- Constraints for table `maintainanceinfo`
--
ALTER TABLE `maintainanceinfo`
  ADD CONSTRAINT `fk_maintainance_tower_id` FOREIGN KEY (`tower_id`) REFERENCES `towerinfo` (`tower_id`);

--
-- Constraints for table `siteinfo`
--
ALTER TABLE `siteinfo`
  ADD CONSTRAINT `fk_site_owner` FOREIGN KEY (`owner_id`) REFERENCES `ownerinfo` (`owner_id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
