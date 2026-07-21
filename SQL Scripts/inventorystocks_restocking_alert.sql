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
-- Table structure for table `restocking_alert`
--

DROP TABLE IF EXISTS `restocking_alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restocking_alert` (
  `Alert_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Alert_Date` date DEFAULT NULL,
  `Quantity_Below_Threshold` int(11) DEFAULT NULL,
  `Restock_Quantity` int(11) DEFAULT NULL,
  `Alert_Status` varchar(45) DEFAULT NULL,
  `Supply_ID` int(11) NOT NULL,
  PRIMARY KEY (`Alert_ID`,`Supply_ID`),
  KEY `fk_Restocking_Alert_Molecular_Supply1_idx` (`Supply_ID`),
  CONSTRAINT `fk_Restocking_Alert_Molecular_Supply1` FOREIGN KEY (`Supply_ID`) REFERENCES `molecular_supply` (`Supply_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restocking_alert`
--

LOCK TABLES `restocking_alert` WRITE;
/*!40000 ALTER TABLE `restocking_alert` DISABLE KEYS */;
INSERT INTO `restocking_alert` VALUES (1,'2025-03-18',5,50,'Pending',1),(2,'2025-03-18',15,100,'Pending',2),(3,'2025-04-23',-1,1,'Pending',4),(4,'2025-04-23',-2,2,'Pending',5),(5,'2025-04-24',-1,1,'Pending',4),(6,'2025-04-24',-2,2,'Pending',5),(7,'2025-04-24',-1,1,'Pending',7),(8,'2025-05-01',-1,1,'Pending',4),(9,'2025-05-01',-2,2,'Pending',5),(10,'2025-05-01',-1,1,'Pending',7);
/*!40000 ALTER TABLE `restocking_alert` ENABLE KEYS */;
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
