CREATE DATABASE  IF NOT EXISTS `inventorystocks` /*!40100 DEFAULT CHARACTER SET utf32 */;
USE `inventorystocks`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: inventorystocks
-- ------------------------------------------------------
-- Server version	5.7.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `molecular_supply`
--

DROP TABLE IF EXISTS `molecular_supply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `molecular_supply` (
  `Supply_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Supply_Type` varchar(45) DEFAULT NULL,
  `Supply_Name` varchar(45) DEFAULT NULL,
  `Brand` varchar(45) DEFAULT NULL,
  `Quantity_Available` int(11) DEFAULT NULL,
  `Unit` varchar(45) DEFAULT NULL,
  `Unit_Price` decimal(65,0) DEFAULT NULL,
  `Expiration_Date` date DEFAULT NULL,
  `Threshold_Quantity` int(11) DEFAULT NULL,
  `Supplier_ID` int(11) NOT NULL,
  PRIMARY KEY (`Supply_ID`,`Supplier_ID`),
  KEY `fk_Molecular_Supply_Supplier1_idx` (`Supplier_ID`),
  CONSTRAINT `fk_Molecular_Supply_Supplier1` FOREIGN KEY (`Supplier_ID`) REFERENCES `supplier` (`Supplier_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `molecular_supply`
--

LOCK TABLES `molecular_supply` WRITE;
/*!40000 ALTER TABLE `molecular_supply` DISABLE KEYS */;
INSERT INTO `molecular_supply` VALUES (1,'Reagent','PCR Primer','Zymo',100,'Vial',50,'2026-12-31',10,1),(2,'Chemical','Ethanol','Thermo Fisher',200,'mL',20,'2026-06-15',20,2),(4,'water','water','thermo',5,'ml',5,'2027-02-02',6,1),(5,'chemical','ethanol','thermofisher',10,'mL',76,'2026-05-03',12,2),(6,'chemical','butane','',100,'ml',75,'2027-01-01',25,1),(7,'water','water','thermo',5,'ML',10,'2026-02-02',6,1),(8,'liquid','H2O','Thermo Fisher',5,'500 mL',50,'2027-01-01',3,2);
/*!40000 ALTER TABLE `molecular_supply` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-01 14:32:42
