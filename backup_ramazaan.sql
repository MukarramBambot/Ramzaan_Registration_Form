-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: sherullah_1447_db
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Token',7,'add_token'),(26,'Can change Token',7,'change_token'),(27,'Can delete Token',7,'delete_token'),(28,'Can view Token',7,'view_token'),(29,'Can add Token',8,'add_tokenproxy'),(30,'Can change Token',8,'change_tokenproxy'),(31,'Can delete Token',8,'delete_tokenproxy'),(32,'Can view Token',8,'view_tokenproxy'),(33,'Can add crontab',9,'add_crontabschedule'),(34,'Can change crontab',9,'change_crontabschedule'),(35,'Can delete crontab',9,'delete_crontabschedule'),(36,'Can view crontab',9,'view_crontabschedule'),(37,'Can add interval',10,'add_intervalschedule'),(38,'Can change interval',10,'change_intervalschedule'),(39,'Can delete interval',10,'delete_intervalschedule'),(40,'Can view interval',10,'view_intervalschedule'),(41,'Can add periodic task',11,'add_periodictask'),(42,'Can change periodic task',11,'change_periodictask'),(43,'Can delete periodic task',11,'delete_periodictask'),(44,'Can view periodic task',11,'view_periodictask'),(45,'Can add periodic task track',12,'add_periodictasks'),(46,'Can change periodic task track',12,'change_periodictasks'),(47,'Can delete periodic task track',12,'delete_periodictasks'),(48,'Can view periodic task track',12,'view_periodictasks'),(49,'Can add solar event',13,'add_solarschedule'),(50,'Can change solar event',13,'change_solarschedule'),(51,'Can delete solar event',13,'delete_solarschedule'),(52,'Can view solar event',13,'view_solarschedule'),(53,'Can add clocked',14,'add_clockedschedule'),(54,'Can change clocked',14,'change_clockedschedule'),(55,'Can delete clocked',14,'delete_clockedschedule'),(56,'Can view clocked',14,'view_clockedschedule'),(57,'Can add registration',15,'add_registration'),(58,'Can change registration',15,'change_registration'),(59,'Can delete registration',15,'delete_registration'),(60,'Can view registration',15,'view_registration'),(61,'Can add audition file',16,'add_auditionfile'),(62,'Can change audition file',16,'change_auditionfile'),(63,'Can delete audition file',16,'delete_auditionfile'),(64,'Can view audition file',16,'view_auditionfile'),(65,'Can add duty assignment',17,'add_dutyassignment'),(66,'Can change duty assignment',17,'change_dutyassignment'),(67,'Can delete duty assignment',17,'delete_dutyassignment'),(68,'Can view duty assignment',17,'view_dutyassignment'),(69,'Can add reminder',18,'add_reminder'),(70,'Can change reminder',18,'change_reminder'),(71,'Can delete reminder',18,'delete_reminder'),(72,'Can view reminder',18,'view_reminder'),(73,'Can add reminder log',19,'add_reminderlog'),(74,'Can change reminder log',19,'change_reminderlog'),(75,'Can delete reminder log',19,'delete_reminderlog'),(76,'Can view reminder log',19,'view_reminderlog'),(77,'Can add unlock log',20,'add_unlocklog'),(78,'Can change unlock log',20,'change_unlocklog'),(79,'Can delete unlock log',20,'delete_unlocklog'),(80,'Can view unlock log',20,'view_unlocklog'),(81,'Can add assignment request log',21,'add_assignmentrequestlog'),(82,'Can change assignment request log',21,'change_assignmentrequestlog'),(83,'Can delete assignment request log',21,'delete_assignmentrequestlog'),(84,'Can view assignment request log',21,'view_assignmentrequestlog'),(85,'Can add khidmat request',22,'add_khidmatrequest'),(86,'Can change khidmat request',22,'change_khidmatrequest'),(87,'Can delete khidmat request',22,'delete_khidmatrequest'),(88,'Can view khidmat request',22,'view_khidmatrequest'),(89,'Can add registration correction',23,'add_registrationcorrection'),(90,'Can change registration correction',23,'change_registrationcorrection'),(91,'Can delete registration correction',23,'delete_registrationcorrection'),(92,'Can view registration correction',23,'view_registrationcorrection'),(93,'Can add duty reminder call',24,'add_dutyremindercall'),(94,'Can change duty reminder call',24,'change_dutyremindercall'),(95,'Can delete duty reminder call',24,'delete_dutyremindercall'),(96,'Can view duty reminder call',24,'view_dutyremindercall');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (2,'pbkdf2_sha256$1000000$swQgaj5XnW7h81A3iV4RJV$FTWmaJb/iA0+spIuNaxfyFu2SrKy74hscuIqcY1ac1U=',NULL,1,'40414853','','','bhftech.info@gmail.com',1,1,'2026-02-10 15:15:16.000000'),(3,'pbkdf2_sha256$1000000$vcJg62GUOenHT3pRtdUOvX$zXIiFbEX3owyfcFEu9GShiDZMuupUQNmqWppRsz3+Po=',NULL,1,'admin','','','',1,1,'2026-02-14 20:23:47.876237'),(4,'pbkdf2_sha256$1000000$NkN9mlRfNO2vLbNN6dz0TX$qxo+8Y3j3E4cJGfSESkpSxwYEI2VsoI/bHDtZjFlbl4=','2026-02-21 01:26:39.606932',1,'60451866','','','mukbambot118@gmail.com',1,1,'2026-02-15 08:59:46.689473'),(6,'',NULL,1,'admin_test','','','',1,1,'2026-02-16 06:48:22.560279'),(7,'',NULL,0,'test_admin','','','',1,1,'2026-02-17 05:44:42.613432');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (93,'2026-02-15 14:58:09.788721','84','efjsuesjbvuo (23125654)',3,'',15,4),(94,'2026-02-15 14:58:09.789216','83','efjsuesjbvuo (78895645)',3,'',15,4),(95,'2026-02-15 14:58:09.789260','64','Pharaoh jsjdjdn (40404040)',3,'',15,4);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_clockedschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_clockedschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_clockedschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `clocked_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_clockedschedule`
--

LOCK TABLES `django_celery_beat_clockedschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_clockedschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_clockedschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_crontabschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hour` varchar(96) COLLATE utf8mb4_unicode_ci NOT NULL,
  `day_of_week` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `day_of_month` varchar(124) COLLATE utf8mb4_unicode_ci NOT NULL,
  `month_of_year` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `timezone` varchar(63) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_crontabschedule`
--

LOCK TABLES `django_celery_beat_crontabschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` DISABLE KEYS */;
INSERT INTO `django_celery_beat_crontabschedule` VALUES (1,'0','4','*','*','*','Asia/Kolkata'),(2,'*/15','*','*','*','*','Asia/Kolkata'),(3,'0','2','*','*','*','Asia/Kolkata'),(4,'*/5','*','*','*','*','Asia/Kolkata');
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_intervalschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `every` int NOT NULL,
  `period` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_intervalschedule`
--

LOCK TABLES `django_celery_beat_intervalschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictask`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_periodictask` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `task` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `args` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `kwargs` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `queue` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `exchange` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `routing_key` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `crontab_id` int DEFAULT NULL,
  `interval_id` int DEFAULT NULL,
  `solar_id` int DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `priority` int unsigned DEFAULT NULL,
  `headers` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb4'{}'),
  `clocked_id` int DEFAULT NULL,
  `expire_seconds` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  KEY `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` (`clocked_id`),
  CONSTRAINT `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` FOREIGN KEY (`clocked_id`) REFERENCES `django_celery_beat_clockedschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`),
  CONSTRAINT `django_celery_beat_periodictask_chk_1` CHECK ((`total_run_count` >= 0)),
  CONSTRAINT `django_celery_beat_periodictask_chk_2` CHECK ((`priority` >= 0)),
  CONSTRAINT `django_celery_beat_periodictask_chk_3` CHECK ((`expire_seconds` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictask`
--

LOCK TABLES `django_celery_beat_periodictask` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` DISABLE KEYS */;
INSERT INTO `django_celery_beat_periodictask` VALUES (1,'celery.backend_cleanup','celery.backend_cleanup','[]','{}',NULL,NULL,NULL,NULL,1,'2026-02-17 22:30:00.015261',2,'2026-02-17 22:30:40.062390','',1,NULL,NULL,0,NULL,NULL,'{}',NULL,43200),(2,'process-reminders-every-15-min','registrations.process_reminders','[]','{}',NULL,NULL,NULL,NULL,1,'2026-02-18 06:45:00.014856',149,'2026-02-18 06:45:15.052908','',2,NULL,NULL,0,NULL,NULL,'{}',NULL,NULL),(3,'cleanup-old-reminders-daily','registrations.cleanup_old_reminders','[]','{}',NULL,NULL,NULL,NULL,1,'2026-02-17 20:30:00.015240',2,'2026-02-17 20:30:30.088570','',3,NULL,NULL,0,NULL,NULL,'{}',NULL,NULL),(4,'process-voice-reminders-every-5-min','registrations.process_due_reminder_calls','[]','{}',NULL,NULL,NULL,NULL,1,'2026-02-18 06:50:00.000699',447,'2026-02-18 06:50:20.045269','',4,NULL,NULL,0,NULL,NULL,'{}',NULL,NULL);
/*!40000 ALTER TABLE `django_celery_beat_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictasks`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictasks`
--

LOCK TABLES `django_celery_beat_periodictasks` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` DISABLE KEYS */;
INSERT INTO `django_celery_beat_periodictasks` VALUES (1,'2026-02-16 17:38:13.857951');
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_solarschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event` varchar(24) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_solarschedule`
--

LOCK TABLES `django_celery_beat_solarschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'authtoken','token'),(8,'authtoken','tokenproxy'),(5,'contenttypes','contenttype'),(14,'django_celery_beat','clockedschedule'),(9,'django_celery_beat','crontabschedule'),(10,'django_celery_beat','intervalschedule'),(11,'django_celery_beat','periodictask'),(12,'django_celery_beat','periodictasks'),(13,'django_celery_beat','solarschedule'),(21,'registrations','assignmentrequestlog'),(16,'registrations','auditionfile'),(17,'registrations','dutyassignment'),(24,'registrations','dutyremindercall'),(22,'registrations','khidmatrequest'),(15,'registrations','registration'),(23,'registrations','registrationcorrection'),(18,'registrations','reminder'),(19,'registrations','reminderlog'),(20,'registrations','unlocklog'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-02-10 11:25:48.660095'),(2,'auth','0001_initial','2026-02-10 11:25:49.614261'),(3,'admin','0001_initial','2026-02-10 11:25:49.776526'),(4,'admin','0002_logentry_remove_auto_add','2026-02-10 11:25:49.785421'),(5,'admin','0003_logentry_add_action_flag_choices','2026-02-10 11:25:49.793213'),(6,'contenttypes','0002_remove_content_type_name','2026-02-10 11:25:49.901540'),(7,'auth','0002_alter_permission_name_max_length','2026-02-10 11:25:49.973376'),(8,'auth','0003_alter_user_email_max_length','2026-02-10 11:25:50.019807'),(9,'auth','0004_alter_user_username_opts','2026-02-10 11:25:50.029678'),(10,'auth','0005_alter_user_last_login_null','2026-02-10 11:25:50.122017'),(11,'auth','0006_require_contenttypes_0002','2026-02-10 11:25:50.129674'),(12,'auth','0007_alter_validators_add_error_messages','2026-02-10 11:25:50.152870'),(13,'auth','0008_alter_user_username_max_length','2026-02-10 11:25:50.255416'),(14,'auth','0009_alter_user_last_name_max_length','2026-02-10 11:25:50.386532'),(15,'auth','0010_alter_group_name_max_length','2026-02-10 11:25:50.425496'),(16,'auth','0011_update_proxy_permissions','2026-02-10 11:25:50.443340'),(17,'auth','0012_alter_user_first_name_max_length','2026-02-10 11:25:50.561828'),(18,'authtoken','0001_initial','2026-02-10 11:25:50.677936'),(19,'authtoken','0002_auto_20160226_1747','2026-02-10 11:25:50.709422'),(20,'authtoken','0003_tokenproxy','2026-02-10 11:25:50.714516'),(21,'authtoken','0004_alter_tokenproxy_options','2026-02-10 11:25:50.720377'),(22,'django_celery_beat','0001_initial','2026-02-10 11:25:51.001085'),(23,'django_celery_beat','0002_auto_20161118_0346','2026-02-10 11:25:51.119162'),(24,'django_celery_beat','0003_auto_20161209_0049','2026-02-10 11:25:51.153516'),(25,'django_celery_beat','0004_auto_20170221_0000','2026-02-10 11:25:51.166595'),(26,'django_celery_beat','0005_add_solarschedule_events_choices','2026-02-10 11:25:51.180868'),(27,'django_celery_beat','0006_auto_20180322_0932','2026-02-10 11:25:51.400233'),(28,'django_celery_beat','0007_auto_20180521_0826','2026-02-10 11:25:51.676034'),(29,'django_celery_beat','0008_auto_20180914_1922','2026-02-10 11:25:51.727513'),(30,'django_celery_beat','0006_auto_20180210_1226','2026-02-10 11:25:51.757251'),(31,'django_celery_beat','0006_periodictask_priority','2026-02-10 11:25:51.894003'),(32,'django_celery_beat','0009_periodictask_headers','2026-02-10 11:25:52.060257'),(33,'django_celery_beat','0010_auto_20190429_0326','2026-02-10 11:25:52.330264'),(34,'django_celery_beat','0011_auto_20190508_0153','2026-02-10 11:25:52.484868'),(35,'django_celery_beat','0012_periodictask_expire_seconds','2026-02-10 11:25:52.632999'),(36,'django_celery_beat','0013_auto_20200609_0727','2026-02-10 11:25:52.647589'),(37,'django_celery_beat','0014_remove_clockedschedule_enabled','2026-02-10 11:25:52.704526'),(38,'django_celery_beat','0015_edit_solarschedule_events_choices','2026-02-10 11:25:52.718792'),(39,'django_celery_beat','0016_alter_crontabschedule_timezone','2026-02-10 11:25:52.733365'),(40,'django_celery_beat','0017_alter_crontabschedule_month_of_year','2026-02-10 11:25:52.746092'),(41,'django_celery_beat','0018_improve_crontab_helptext','2026-02-10 11:25:52.763006'),(42,'django_celery_beat','0019_alter_periodictasks_options','2026-02-10 11:25:52.767550'),(43,'registrations','0001_initial','2026-02-10 11:25:53.155161'),(44,'registrations','0002_alter_registration_options_and_more','2026-02-10 11:25:53.836871'),(45,'registrations','0003_alter_auditionfile_audio_file','2026-02-10 11:25:53.848169'),(46,'registrations','0004_remove_auditionfile_audio_file_and_more','2026-02-10 11:25:54.226721'),(47,'registrations','0005_dutyassignment_allotment_notification_sent_and_more','2026-02-10 11:25:54.546091'),(48,'registrations','0006_registration_registratio_email_2d2215_idx','2026-02-10 11:25:54.593881'),(49,'sessions','0001_initial','2026-02-10 11:25:54.665803'),(50,'registrations','0007_registration_status','2026-02-10 12:07:20.887275'),(51,'registrations','0008_alter_registration_status','2026-02-10 12:21:30.154896'),(52,'registrations','0009_registration_whatsapp_delivered_at_and_more','2026-02-13 11:32:05.757921'),(53,'registrations','0010_add_whatsapp_failed_reason','2026-02-13 14:01:15.810495'),(54,'registrations','0011_update_preference_to_json','2026-02-14 08:13:14.357032'),(55,'registrations','0012_alter_registration_preference','2026-02-14 08:13:14.420161'),(56,'registrations','0013_add_assignment_request_fields','2026-02-14 13:39:27.984646'),(57,'registrations','0014_backfill_dutyassignment_status','2026-02-14 13:39:28.013827'),(58,'registrations','0015_alter_auditionfile_audition_file_path','2026-02-14 13:39:28.020874'),(59,'registrations','0016_khidmatrequest','2026-02-14 14:04:21.001322'),(60,'registrations','0017_registration_is_active_alter_registration_status_and_more','2026-02-14 17:45:15.079887'),(61,'registrations','0018_registration_is_active_alter_registration_status','2026-02-14 17:45:20.276329'),(62,'registrations','0019_remove_khidmatrequest_unique_pending_request_per_assignment_and_more','2026-02-14 17:46:20.645207'),(63,'registrations','0020_fix_database_cascade_constraints','2026-02-14 17:57:03.340412'),(64,'registrations','0021_reminder_whatsapp_message_id_and_more','2026-02-16 04:25:45.064267'),(65,'registrations','0022_auditionfile_is_selected_and_more','2026-02-16 04:50:26.155012'),(66,'registrations','0023_auditionfile_is_selected_and_more','2026-02-16 06:40:08.585964'),(67,'registrations','0024_auditionfile_is_selected_and_more','2026-02-16 17:37:59.724150'),(68,'registrations','0025_auditionfile_is_selected_and_more','2026-02-17 05:43:00.351410'),(69,'registrations','0026_auditionfile_is_selected_and_more','2026-02-18 06:56:58.562313'),(70,'registrations','0027_alter_auditionfile_audition_file_path','2026-02-19 06:30:30.464728');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('ltzn56u2xwxclbkw9p64qhg6mcm9wm65','.eJxVjMsOwiAQRf-FtSG8QZfu-w1kGAapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2YUZdvrdEuCD2g7yHdqtc-xtXebEd4UfdPCpZ3peD_fvoMKo39oGSQazMFDs2Qnlg1ApGQceqAhSEqF4KwiJlDNWQdZBOECdUSZpNXt_AOa9OBU:1vtblX:9p08hwgv2nNdFNC6hafELgvs23vGCdz3IawrPfn6w-U','2026-03-07 01:26:39.620925'),('smrb6u126u2rbynh8jpi6ecfnixbn454','.eJxVjMsOwiAQRf-FtSG8QZfu-w1kGAapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2YUZdvrdEuCD2g7yHdqtc-xtXebEd4UfdPCpZ3peD_fvoMKo39oGSQazMFDs2Qnlg1ApGQceqAhSEqF4KwiJlDNWQdZBOECdUSZpNXt_AOa9OBU:1vrkRt:aJkiIJbamID7W1NUKmV7YcZ3e8uXPbkxRMZdoNi5bDw','2026-03-01 22:18:41.487452'),('t76u4nvmnsxa92tehww9xrrgeblkbkio','.eJxVjMsOwiAQRf-FtSG8QZfu-w1kGAapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2YUZdvrdEuCD2g7yHdqtc-xtXebEd4UfdPCpZ3peD_fvoMKo39oGSQazMFDs2Qnlg1ApGQceqAhSEqF4KwiJlDNWQdZBOECdUSZpNXt_AOa9OBU:1vrXyy:s_YdXJUqbpcb6-vKEQ0OeU9WZkgXNMG-c1rzh2iNWd0','2026-03-01 09:00:00.251842');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_assignmentrequestlog`
--

DROP TABLE IF EXISTS `registrations_assignmentrequestlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_assignmentrequestlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `request_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `requested_by_its` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reason` longtext COLLATE utf8mb4_unicode_ci,
  `preferred_datetime` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `requested_at` datetime(6) NOT NULL,
  `processed` tinyint(1) NOT NULL,
  `duty_assignment_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `registrations_assign_duty_assignment_id_816073b8_fk_registrat` (`duty_assignment_id`),
  CONSTRAINT `registrations_assign_duty_assignment_id_816073b8_fk_registrat` FOREIGN KEY (`duty_assignment_id`) REFERENCES `registrations_dutyassignment` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_assignmentrequestlog`
--

LOCK TABLES `registrations_assignmentrequestlog` WRITE;
/*!40000 ALTER TABLE `registrations_assignmentrequestlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `registrations_assignmentrequestlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_auditionfile`
--

DROP TABLE IF EXISTS `registrations_auditionfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_auditionfile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uploaded_at` datetime(6) NOT NULL,
  `registration_id` bigint NOT NULL,
  `audition_display_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `audition_file_path` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `audition_file_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_selected` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `registrations_auditi_registration_id_f35cca51_fk_registrat` (`registration_id`),
  CONSTRAINT `registrations_auditi_registration_id_f35cca51_fk_registrat` FOREIGN KEY (`registration_id`) REFERENCES `registrations_registration` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_auditionfile`
--

LOCK TABLES `registrations_auditionfile` WRITE;
/*!40000 ALTER TABLE `registrations_auditionfile` DISABLE KEYS */;
INSERT INTO `registrations_auditionfile` VALUES (52,'2026-02-15 05:22:14.643541',61,'Huzaifa – Audition','auditions files/audio/40414853_huzaifa_joshan_tilawat_yaseen_takhbira_sanah_azaan.mp3','audio',0),(56,'2026-02-15 11:12:13.236473',67,'','auditions files/audio/30800629_abbas_mandlewala_takhbira.mp3','audio',0),(57,'2026-02-15 11:19:27.610047',70,'','auditions files/audio/40414141_mulla_aliasger_ujjainwala_takhbira_yaseen_joshan.m4a','audio',0),(58,'2026-02-15 11:19:28.066857',71,'','auditions files/audio/40410439_adnaan_shabbir_karyanawala_takhbira_yaseen_azaan.mp3','audio',0),(59,'2026-02-15 12:38:30.919986',79,'','auditions files/audio/50202244_mehlam_hozefa_gajipurwala_takhbira_azaan.mp3','audio',0),(60,'2026-02-15 12:45:20.852887',80,'','auditions files/audio/40916796_idris_hozefa_gajipurwala_takhbira_azaan.mp3','audio',0),(61,'2026-02-15 14:07:26.278813',81,'','auditions files/audio/40410440_murtaza_shabbir_karyanawala_takhbira_yaseen_azaan.m4a','audio',0),(62,'2026-02-15 14:07:39.395532',82,'','auditions files/audio/40414176_yusuf_skjuzerbhai_ranujwala_takhbira_azaan.m4a','audio',0),(63,'2026-02-15 14:07:39.396389',82,'','auditions files/audio/40414176_yusuf_skjuzerbhai_ranujwala_takhbira_azaan_Drtc6CL.m4a','audio',0),(66,'2026-02-15 15:06:50.087946',85,'','auditions files/audio/20376751_kutbuddin_azaan.m4a','audio',0),(67,'2026-02-16 01:53:47.791233',88,'','auditions files/audio/40415378_yusuf_shk_mohammed_bhai_kitabi_takhbira_azaan.m4a','audio',0),(68,'2026-02-16 01:53:47.792895',88,'','auditions files/audio/40415378_yusuf_shk_mohammed_bhai_kitabi_takhbira_azaan_w4mENKx.m4a','audio',0),(75,'2026-02-16 05:28:05.931889',93,'','auditions files/audio/40411352_mohammed_ranujwala_azaan.m4a','audio',0),(77,'2026-02-16 06:45:44.613688',98,'Mulla shabbir mulla abbas bhai chotaudaipurwala – Audition','auditions files/audio/20417673_mulla_shabbir_mulla_abbas_bhai_chotaudaipurwala_yaseen_ta_cV72SFn.m4a','audio',0),(80,'2026-02-16 07:42:03.828584',107,'Mushtaque altafhussain vahalabhai – Audition','auditions files/audio/20356371_mushtaque_altafhussain_vahalabhai_azaan.m4a','audio',0),(81,'2026-02-16 08:22:15.779553',109,'Ahamed Mushtaque Vahlabhai – Audition','auditions files/audio/40410719_ahamed_mushtaque_vahlabhai_azaan.wav','audio',0),(82,'2026-02-16 09:14:07.914192',110,'Hyder jamnagarwala – Audition','auditions files/audio/40410787_hyder_jamnagarwala_azaan_takhbira.m4a','audio',0),(83,'2026-02-16 11:46:00.799922',111,'Taher Mohammed Bhagat – Audition','auditions files/audio/60451171_taher_mohammed_bhagat_azaan_takhbira.m4a','audio',0),(84,'2026-02-16 12:10:37.860157',112,'Ammar Hasan bhai Kapi – Audition','auditions files/audio/40910776_ammar_hasan_bhai_kapi_takhbira.m4a','audio',0),(85,'2026-02-16 15:08:22.736147',114,'Taha Aziz Kanorewala – Audition','auditions files/audio/60451742_taha_aziz_kanorewala_azaan_takhbira_yaseen_tilawat.m4a','audio',0),(86,'2026-02-17 02:47:22.274100',116,'Mohammed Murtaza Kagalwala – Audition','auditions files/audio/40908018_mohammed_murtaza_kagalwala_takhbira.mp3','audio',0),(89,'2026-02-17 06:18:17.534771',122,'Shabbar Jabir – Audition','auditions files/video/40410887_shabbar_jabir_takhbira_azaan.mov','audio',0),(91,'2026-02-17 09:37:58.991349',132,'Mohammed dula – Audition','auditions files/audio/40920415_mohammed_dula_azaan.mp3','audio',0),(100,'2026-02-18 07:45:47.384896',159,'Hussain Calicutwala – Audition','auditions files/audio/60451268_hussain_calicutwala_takhbira_yaseen.m4a','audio',0),(101,'2026-02-18 09:11:31.131948',160,'aliasgar shk hussain bhai attarwala – Audition','auditions files/audio/40411479_aliasgar_shk_hussain_bhai_attarwala_joshan_yaseen_sanah_t_jtR8Dvl.m4a','audio',0),(102,'2026-02-18 09:11:31.135113',160,'aliasgar shk hussain bhai attarwala – Audition','auditions files/audio/40411479_aliasgar_shk_hussain_bhai_attarwala_joshan_yaseen_sanah_t_GjUWwID.m4a','audio',0),(103,'2026-02-18 09:11:31.138062',160,'aliasgar shk hussain bhai attarwala – Audition','auditions files/audio/40411479_aliasgar_shk_hussain_bhai_attarwala_joshan_yaseen_sanah_t_cwDX1j8.m4a','audio',0),(104,'2026-02-18 09:11:31.139962',160,'aliasgar shk hussain bhai attarwala – Audition','auditions files/audio/40411479_aliasgar_shk_hussain_bhai_attarwala_joshan_yaseen_sanah_t_RPKIAUg.m4a','audio',0),(105,'2026-02-18 09:11:31.142278',160,'aliasgar shk hussain bhai attarwala – Audition','auditions files/audio/40411479_aliasgar_shk_hussain_bhai_attarwala_joshan_yaseen_sanah_t_bIZxlCl.m4a','audio',0),(107,'2026-02-19 11:35:39.964093',169,'Muffadal Bombaywala – Audition','auditions files/audio/60451152_muffadal_bombaywala_takhbira_tilawat_yaseen_azaan.m4a','audio',0),(108,'2026-02-19 11:45:44.385801',170,'Adnan Bombaywala – Audition','auditions files/audio/60451151_adnan_bombaywala_takhbira_tilawat_yaseen_azaan.m4a','audio',0),(109,'2026-02-19 15:55:27.323783',171,'MOHAMMED A RAJA – Audition','auditions files/audio/20363312_mohammed_a_raja_takhbira.m4a','audio',0),(110,'2026-02-20 07:48:03.218776',174,'Mohammed Bambot – Audition','auditions files/audio/40411623_mohammed_bambot_azaan.m4a','audio',0),(111,'2026-02-22 05:39:16.939276',179,'Ibrahim Vithodawala – Audition','auditions files/audio/40410829_ibrahim_vithodawala_takhbira_azaan.m4a','audio',0),(112,'2026-02-22 05:39:16.978551',179,'Ibrahim Vithodawala – Audition','auditions files/audio/40410829_ibrahim_vithodawala_takhbira_azaan_j8Lkrx6.m4a','audio',0),(113,'2026-02-22 05:56:52.393823',168,'Murtaza shabbir vadnagarwala – Audition','auditions files/video/40414360_murtaza_shabbir_vadnagarwala_takhbira_azaan.amr','audio',0),(114,'2026-02-22 09:30:20.794178',181,'Shabbir Vakharia – Audition','auditions files/audio/30141238_shabbir_vakharia_takhbira_tilawat_yaseen_azaan.m4a','audio',0),(115,'2026-02-23 06:06:57.883981',182,'Hussain joher – Audition','auditions files/audio/50458107_hussain_joher_azaan.m4a','audio',0),(116,'2026-02-24 01:56:28.336873',185,'Husain Bhagat – Audition','auditions files/audio/40414040_husain_bhagat_takhbira_yaseen_azaan.m4a','audio',0),(117,'2026-02-24 22:00:21.315422',188,'Idris Abdulhussain Bhai Pindwarawala – Audition','auditions files/audio/30900730_idris_abdulhussain_bhai_pindwarawala_takhbira.m4a','audio',0),(118,'2026-03-01 15:06:21.126254',192,'Adnan Mulla Mufaddal bhai Chanasmawala – Audition','auditions files/audio/40910710_adnan_mulla_mufaddal_bhai_chanasmawala_takhbira.aac','audio',0),(119,'2026-03-02 08:58:41.590061',194,'Mustansir Quilonwala – Audition','auditions files/audio/60447339_mustansir_quilonwala_azaan.m4a','audio',0);
/*!40000 ALTER TABLE `registrations_auditionfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_dutyassignment`
--

DROP TABLE IF EXISTS `registrations_dutyassignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_dutyassignment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `duty_date` date NOT NULL,
  `namaaz_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `locked` tinyint(1) NOT NULL,
  `locked_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assigned_user_id` bigint DEFAULT NULL,
  `allotment_notification_sent` tinyint(1) NOT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cancel_reason` longtext COLLATE utf8mb4_unicode_ci,
  `reallocation_reason` longtext COLLATE utf8mb4_unicode_ci,
  `reallocation_requested_at` datetime(6) DEFAULT NULL,
  `cancel_requested_at` datetime(6) DEFAULT NULL,
  `removal_reason` longtext COLLATE utf8mb4_unicode_ci,
  `removed_at` datetime(6) DEFAULT NULL,
  `removed_by_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `registrations_dutyassignment_duty_date_namaaz_type_11168ba8_uniq` (`duty_date`,`namaaz_type`),
  KEY `registratio_duty_da_18996b_idx` (`duty_date`),
  KEY `registratio_namaaz__dd1859_idx` (`namaaz_type`),
  KEY `registrations_dutyas_removed_by_id_92835c0b_fk_auth_user` (`removed_by_id`),
  KEY `registrations_dutyas_assigned_user_id_22e62129_fk_registrat` (`assigned_user_id`),
  CONSTRAINT `registrations_dutyas_assigned_user_id_22e62129_fk_registrat` FOREIGN KEY (`assigned_user_id`) REFERENCES `registrations_registration` (`id`),
  CONSTRAINT `registrations_dutyas_removed_by_id_92835c0b_fk_auth_user` FOREIGN KEY (`removed_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_dutyassignment`
--

LOCK TABLES `registrations_dutyassignment` WRITE;
/*!40000 ALTER TABLE `registrations_dutyassignment` DISABLE KEYS */;
INSERT INTO `registrations_dutyassignment` VALUES (35,'2026-02-16','MAGRIB_AZAAN',1,'2026-02-16 06:39:19.814452','2026-02-16 06:39:19.814474','2026-02-16 06:39:19.814482',82,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(36,'2026-02-20','ZOHAR_AZAAN',1,'2026-02-16 06:41:38.685716','2026-02-16 06:41:38.685744','2026-02-16 06:41:38.685762',89,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(37,'2026-02-16','ZOHAR_AZAAN',1,'2026-02-16 07:01:38.918928','2026-02-16 07:01:38.918958','2026-02-16 07:01:38.918970',61,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(38,'2026-02-16','MAGRIB_TAKBIRA',1,'2026-02-16 10:09:57.141025','2026-02-16 10:09:57.141060','2026-02-16 10:09:57.141073',81,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(39,'2026-02-17','FAJAR_AZAAN',0,'2026-02-16 17:38:28.793602','2026-02-16 17:38:28.793633','2026-02-19 08:23:41.821573',NULL,0,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-19 08:23:41.821469',2),(41,'2026-02-17','MAGRIB_AZAAN',1,'2026-02-17 05:32:06.209416','2026-02-17 05:32:06.209447','2026-02-17 05:32:06.209458',77,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(43,'2026-02-17','ISHAA_TAKBIRA',1,'2026-02-17 05:32:33.580626','2026-02-17 05:32:33.580648','2026-02-17 05:32:33.580657',98,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(44,'2026-02-20','FAJAR_AZAAN',0,NULL,'2026-02-17 05:44:42.610719','2026-02-17 05:51:56.835019',NULL,0,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-17 05:51:56.834713',7),(45,'2026-02-17','SANAH',0,'2026-02-17 05:46:24.958782','2026-02-17 05:46:24.958807','2026-02-17 06:04:50.698629',NULL,1,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-17 06:04:50.698161',4),(47,'2026-02-25','MAGRIB_AZAAN',0,NULL,'2026-02-17 06:00:50.782114','2026-02-17 06:02:11.134497',NULL,0,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-17 06:02:11.134337',NULL),(48,'2026-03-01','FAJAR_AZAAN',0,NULL,'2026-02-17 06:12:49.473323','2026-02-17 17:35:41.692497',NULL,0,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(49,'2026-02-24','ZOHAR_AZAAN',0,NULL,'2026-02-17 08:45:49.916956','2026-02-17 08:45:55.826402',NULL,1,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-17 08:45:55.826270',4),(51,'2026-02-17','TAJWEED',0,NULL,'2026-02-17 17:07:35.342630','2026-02-17 17:08:13.241748',NULL,1,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-17 17:08:13.241641',4),(52,'2026-02-17','DUA_E_JOSHAN',0,NULL,'2026-02-17 17:13:38.452804','2026-02-17 17:40:54.524021',NULL,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(55,'2026-03-05','FAJAR_AZAAN',0,NULL,'2026-02-17 17:35:41.689132','2026-02-17 17:38:58.718161',NULL,0,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-17 17:38:58.718080',4),(56,'2026-02-18','DUA_E_JOSHAN',0,NULL,'2026-02-17 17:40:54.520271','2026-02-17 17:41:09.893439',NULL,0,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-17 17:41:09.893357',4),(57,'2026-02-18','MAGRIB_AZAAN',1,NULL,'2026-02-18 05:46:06.203977','2026-02-18 05:46:06.204005',109,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(58,'2026-02-18','MAGRIB_TAKBIRA',1,NULL,'2026-02-18 05:51:25.293958','2026-02-18 05:51:25.293981',66,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(59,'2026-02-19','MAGRIB_TAKBIRA',1,NULL,'2026-02-18 05:58:55.795568','2026-02-18 05:58:55.795586',153,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(60,'2026-02-19','ISHAA_TAKBIRA',1,NULL,'2026-02-18 05:59:28.591272','2026-02-18 05:59:28.591311',70,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(62,'2026-02-17','ZOHAR_AZAAN',0,NULL,'2026-02-19 07:11:39.455058','2026-02-19 07:13:10.007224',NULL,1,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-19 07:13:10.007123',4),(63,'2026-02-24','AZAAN',1,NULL,'2026-02-19 07:37:36.010264','2026-02-19 07:37:36.010288',160,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(64,'2026-02-19','ZOHAR_AZAAN',1,NULL,'2026-02-19 08:22:31.795557','2026-02-19 08:22:31.795586',61,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(65,'2026-02-14','FAJAR_AZAAN',1,NULL,'2026-02-19 14:20:10.007885','2026-02-19 14:20:10.008119',61,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(66,'2026-02-20','ZOHAR_TAKBIRA',1,NULL,'2026-02-20 05:19:51.165045','2026-02-20 05:19:51.165074',169,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(67,'2026-02-20','MAGRIB_TAKBIRA',1,NULL,'2026-02-20 05:21:24.327174','2026-02-20 05:21:24.327200',88,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(68,'2026-02-20','ISHAA_TAKBIRA',1,NULL,'2026-02-20 05:21:33.129142','2026-02-20 05:21:33.129544',148,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(69,'2026-02-21','MAGRIB_AZAAN',0,NULL,'2026-02-20 05:23:24.984777','2026-02-21 04:58:22.642311',NULL,1,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-21 04:58:22.641817',2),(70,'2026-02-20','MAGRIB_AZAAN',1,NULL,'2026-02-20 05:24:56.864926','2026-02-20 05:24:56.864963',93,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(71,'2026-02-21','ZOHAR_TAKBIRA',1,NULL,'2026-02-20 05:28:06.516928','2026-02-20 05:28:06.516947',171,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(72,'2026-02-20','ASAR_TAKBIRA',1,NULL,'2026-02-20 05:33:28.516061','2026-02-20 05:33:28.516085',78,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(73,'2026-02-21','ISHAA_TAKBIRA',1,NULL,'2026-02-20 09:28:28.968157','2026-02-20 09:28:28.968426',159,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(74,'2026-02-21','MAGRIB_TAKBIRA',1,NULL,'2026-02-20 09:31:07.877934','2026-02-20 09:31:07.877969',74,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(75,'2026-02-22','MAGRIB_AZAAN',0,NULL,'2026-02-23 05:47:43.779321','2026-02-23 05:54:48.247933',NULL,1,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-23 05:54:48.247194',2),(76,'2026-02-23','MAGRIB_AZAAN',1,NULL,'2026-02-23 05:55:16.344083','2026-02-23 05:55:16.344115',75,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(77,'2026-02-23','MAGRIB_TAKBIRA',1,NULL,'2026-02-23 06:13:29.173794','2026-02-23 06:13:29.173814',170,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(78,'2026-02-24','MAGRIB_AZAAN',1,NULL,'2026-02-24 05:27:48.282672','2026-02-24 05:27:48.282909',179,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(79,'2026-02-26','MAGRIB_AZAAN',1,NULL,'2026-02-24 05:28:19.973922','2026-02-24 05:28:19.974217',182,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(80,'2026-02-27','MAGRIB_AZAAN',1,NULL,'2026-02-24 05:37:34.382292','2026-02-24 05:37:34.382315',114,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(81,'2026-03-02','MAGRIB_AZAAN',0,NULL,'2026-02-24 05:38:31.682321','2026-03-02 05:24:08.915000',NULL,1,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-03-02 05:24:08.914239',2),(82,'2026-02-28','MAGRIB_AZAAN',1,NULL,'2026-02-24 05:40:47.190403','2026-02-24 05:40:47.190688',111,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(83,'2026-03-01','MAGRIB_AZAAN',1,NULL,'2026-02-24 05:41:22.018006','2026-02-24 05:41:22.018032',180,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(84,'2026-02-25','MAGRIB_TAKBIRA',1,NULL,'2026-02-25 06:54:41.577434','2026-02-25 06:54:41.577772',185,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(85,'2026-02-26','MAGRIB_TAKBIRA',0,NULL,'2026-02-26 05:30:32.808818','2026-02-26 05:37:06.950222',NULL,1,'allotted',NULL,NULL,NULL,NULL,'Unassigned via Admin Dashboard','2026-02-26 05:37:06.950102',2),(86,'2026-03-03','MAGRIB_AZAAN',1,NULL,'2026-03-02 05:24:32.264437','2026-03-02 05:24:32.264458',178,1,'allotted',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `registrations_dutyassignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_dutyremindercall`
--

DROP TABLE IF EXISTS `registrations_dutyremindercall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_dutyremindercall` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `scheduled_time` datetime(6) NOT NULL,
  `call_status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `exotel_call_sid` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `duty_assignment_id` bigint DEFAULT NULL,
  `registration_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `registrations_dutyremind_registration_id_schedule_8edebb2b_uniq` (`registration_id`,`scheduled_time`),
  KEY `registrations_dutyre_duty_assignment_id_45509930_fk_registrat` (`duty_assignment_id`),
  CONSTRAINT `registrations_dutyre_duty_assignment_id_45509930_fk_registrat` FOREIGN KEY (`duty_assignment_id`) REFERENCES `registrations_dutyassignment` (`id`),
  CONSTRAINT `registrations_dutyre_registration_id_b258dc61_fk_registrat` FOREIGN KEY (`registration_id`) REFERENCES `registrations_registration` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_dutyremindercall`
--

LOCK TABLES `registrations_dutyremindercall` WRITE;
/*!40000 ALTER TABLE `registrations_dutyremindercall` DISABLE KEYS */;
INSERT INTO `registrations_dutyremindercall` VALUES (1,'2026-02-16 17:38:22.230303','FAILED',NULL,'2026-02-16 17:38:28.839100',39,114),(2,'2026-02-16 17:39:37.612727','FAILED',NULL,'2026-02-16 17:40:37.615406',35,114),(3,'2026-02-16 17:38:37.621586','FAILED',NULL,'2026-02-16 17:40:37.622978',35,114),(4,'2026-02-16 17:37:37.627236','FAILED',NULL,'2026-02-16 17:40:37.628440',35,114),(5,'2026-02-16 17:36:37.631837','FAILED',NULL,'2026-02-16 17:40:37.633037',35,114),(6,'2026-02-16 17:35:37.636497','FAILED',NULL,'2026-02-16 17:40:37.637689',35,114),(7,'2026-02-16 17:34:37.641438','FAILED',NULL,'2026-02-16 17:40:37.642613',35,114),(8,'2026-02-16 17:33:37.645687','FAILED',NULL,'2026-02-16 17:40:37.646687',35,114),(9,'2026-02-16 17:32:37.650377','FAILED',NULL,'2026-02-16 17:40:37.651847',35,114),(10,'2026-02-16 17:31:37.655731','FAILED',NULL,'2026-02-16 17:40:37.657215',35,114),(11,'2026-02-16 17:30:37.660801','FAILED',NULL,'2026-02-16 17:40:37.662211',35,114),(12,'2026-02-17 10:10:00.000000','FAILED',NULL,'2026-02-17 05:32:06.535767',41,77),(14,'2026-02-17 10:10:00.000000','FAILED',NULL,'2026-02-17 05:32:33.632453',43,98),(21,'2026-02-18 10:10:00.000000','PENDING',NULL,'2026-02-18 05:46:06.379372',57,109),(22,'2026-02-18 10:10:00.000000','PENDING',NULL,'2026-02-18 05:51:25.353552',58,66),(23,'2026-02-19 10:10:00.000000','PENDING',NULL,'2026-02-18 05:58:55.869598',59,153),(24,'2026-02-19 10:10:00.000000','PENDING',NULL,'2026-02-18 05:59:28.733277',60,70),(27,'2026-02-19 05:00:00.000000','PENDING',NULL,'2026-02-19 08:22:31.980345',64,61),(28,'2026-02-13 21:50:00.000000','PENDING',NULL,'2026-02-19 14:20:10.623524',65,61),(29,'2026-02-20 05:00:00.000000','PENDING',NULL,'2026-02-20 05:19:51.330160',66,169),(30,'2026-02-20 10:10:00.000000','PENDING',NULL,'2026-02-20 05:21:24.404482',67,88),(31,'2026-02-20 10:10:00.000000','PENDING',NULL,'2026-02-20 05:21:33.431471',68,148),(32,'2026-02-21 10:10:00.000000','PENDING',NULL,'2026-02-20 05:23:25.235080',69,173),(33,'2026-02-20 10:10:00.000000','PENDING',NULL,'2026-02-20 05:24:56.949615',70,93),(34,'2026-02-21 05:00:00.000000','PENDING',NULL,'2026-02-20 05:28:06.695847',71,171),(35,'2026-02-20 05:00:00.000000','PENDING',NULL,'2026-02-20 05:33:28.608991',72,78),(36,'2026-02-21 10:10:00.000000','PENDING',NULL,'2026-02-20 09:28:29.438474',73,159),(37,'2026-02-21 10:10:00.000000','PENDING',NULL,'2026-02-20 09:31:07.986259',74,74),(38,'2026-02-22 10:10:00.000000','PENDING',NULL,'2026-02-23 05:47:44.506209',75,75),(39,'2026-02-23 10:10:00.000000','PENDING',NULL,'2026-02-23 05:55:16.454408',76,75),(40,'2026-02-23 10:10:00.000000','PENDING',NULL,'2026-02-23 06:13:29.233325',77,170),(41,'2026-02-24 10:10:00.000000','PENDING',NULL,'2026-02-24 05:27:48.924730',78,179),(42,'2026-02-26 10:10:00.000000','PENDING',NULL,'2026-02-24 05:28:20.315856',79,182),(43,'2026-02-27 10:10:00.000000','PENDING',NULL,'2026-02-24 05:37:34.436242',80,114),(44,'2026-03-02 10:10:00.000000','PENDING',NULL,'2026-02-24 05:38:31.937566',81,178),(45,'2026-02-28 10:10:00.000000','PENDING',NULL,'2026-02-24 05:40:47.285746',82,111),(46,'2026-03-01 10:10:00.000000','PENDING',NULL,'2026-02-24 05:41:22.097360',83,180),(47,'2026-02-25 10:10:00.000000','PENDING',NULL,'2026-02-25 06:54:42.320246',84,185),(48,'2026-02-26 10:10:00.000000','PENDING',NULL,'2026-02-26 05:30:33.507483',85,180),(49,'2026-03-03 10:10:00.000000','PENDING',NULL,'2026-03-02 05:24:34.416822',86,178);
/*!40000 ALTER TABLE `registrations_dutyremindercall` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_khidmatrequest`
--

DROP TABLE IF EXISTS `registrations_khidmatrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_khidmatrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `request_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `preferred_date` date DEFAULT NULL,
  `preferred_time` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reason` longtext COLLATE utf8mb4_unicode_ci,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `reviewed_by_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `assignment_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `registratio_status_6983f3_idx` (`status`),
  KEY `registratio_assignm_2f3923_idx` (`assignment_id`),
  CONSTRAINT `registrations_khidma_assignment_id_d5b56069_fk_registrat` FOREIGN KEY (`assignment_id`) REFERENCES `registrations_dutyassignment` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_khidmatrequest`
--

LOCK TABLES `registrations_khidmatrequest` WRITE;
/*!40000 ALTER TABLE `registrations_khidmatrequest` DISABLE KEYS */;
INSERT INTO `registrations_khidmatrequest` VALUES (11,'reallocate',NULL,NULL,'User requested reallocation','approved','2026-02-17 06:53:04.299542','2026-02-17 17:22:27.571796','60451866',39),(13,'reallocate',NULL,NULL,'User requested reallocation','approved','2026-02-17 17:07:49.441177','2026-02-17 17:07:58.802477','60451866',51),(17,'reallocate',NULL,NULL,NULL,'REALLOCATION_APPROVED','2026-02-17 17:35:41.628649','2026-02-17 17:35:41.695803','40414853',48),(18,'reallocate',NULL,NULL,'User requested reallocation','approved','2026-02-17 17:37:58.702882','2026-02-17 17:38:28.916925','60451866',52),(19,'reallocate',NULL,NULL,'User requested reallocation','approved','2026-02-17 17:39:27.427664','2026-02-17 17:39:47.036805','60451866',52),(20,'reallocate',NULL,NULL,'User requested reallocation','REALLOCATION_APPROVED','2026-02-17 17:40:40.098485','2026-02-17 17:40:54.528451','60451866',52),(21,'reallocate',NULL,NULL,'User requested reallocation','pending','2026-02-17 18:49:55.531051',NULL,NULL,39),(23,'reallocate',NULL,NULL,'User requested reallocation','approved','2026-02-19 07:11:54.008320','2026-02-19 07:12:51.581460','60451866',62),(24,'cancel',NULL,NULL,'Traveling out of town','pending','2026-02-19 07:37:36.031906',NULL,NULL,63),(25,'cancel',NULL,NULL,'Traveling out of town','pending','2026-02-19 07:38:05.665639',NULL,NULL,63),(26,'reallocate',NULL,NULL,'User requested reallocation','pending','2026-02-26 12:55:45.947584',NULL,NULL,83);
/*!40000 ALTER TABLE `registrations_khidmatrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_registration`
--

DROP TABLE IF EXISTS `registrations_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `its_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `whatsapp_sent` tinyint(1) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `whatsapp_delivered_at` datetime(6) DEFAULT NULL,
  `whatsapp_error` longtext COLLATE utf8mb4_unicode_ci,
  `whatsapp_message_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `whatsapp_read_at` datetime(6) DEFAULT NULL,
  `whatsapp_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `whatsapp_failed_reason` longtext COLLATE utf8mb4_unicode_ci,
  `preference` json NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `its_number` (`its_number`),
  KEY `registratio_its_num_ac61b4_idx` (`its_number`),
  KEY `registratio_email_2d2215_idx` (`email`),
  KEY `registratio_whatsap_a5714f_idx` (`whatsapp_message_id`)
) ENGINE=InnoDB AUTO_INCREMENT=195 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_registration`
--

LOCK TABLES `registrations_registration` WRITE;
/*!40000 ALTER TABLE `registrations_registration` DISABLE KEYS */;
INSERT INTO `registrations_registration` VALUES (61,'Huzaifa','40414853','bhftech.info@gmail.com','9677296252','2026-02-15 05:22:14.641769',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"JOSHAN\", \"TILAWAT\", \"YASEEN\", \"TAKHBIRA\", \"SANAH\", \"AZAAN\"]',1),(65,'Abdulqadir Ratlamwala','30700665','aqstar786@gmail.com','9952092728','2026-02-15 11:03:12.782841',0,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(66,'Khadir Mulla Yusuf Ezzy','40410531','ezzykhadir53@gmail.com','8667409635','2026-02-15 11:08:53.755804',0,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(67,'ABBAS MANDLEWALA','30800629','badriabbas786@gmail.com','9841492989','2026-02-15 11:12:13.218185',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(68,'Huzefa Shk Abbas Kathawala','40415708','akhuzefa53@gmail.com','9962925352','2026-02-15 11:17:28.821933',0,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\"]',1),(69,'Huzefa','40414487','huzefajuzer24@gmail.com','9841511228','2026-02-15 11:17:33.689353',0,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\"]',1),(70,'Mulla Aliasger Ujjainwala','40414141','aliujjainwala52@gmail.com','9840150046','2026-02-15 11:19:27.589409',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\", \"JOSHAN\"]',1),(71,'Adnaan Shabbir Karyanawala','40410439','askaryanawala@gmail.com','8124564753','2026-02-15 11:19:28.064367',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\", \"AZAAN\"]',1),(72,'Saifuddin','30705811','saifuddinaliasgarghantiwala@gmail.com','7984521303','2026-02-15 11:20:00.601274',0,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(73,'Mustafa','40411407','thecentraltools@gmail.com','9840127929','2026-02-15 11:20:17.158965',0,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(74,'Shabbir A Miyajiwala','20417339','ammartradingco53@gmail.com','9790920952','2026-02-15 11:33:20.937286',0,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\", \"AZAAN\"]',1),(75,'Moiz shk. Shamoon bhai Mandleywala','40411468','mmoizco@yahoo.com','9884082452','2026-02-15 11:40:06.275020',0,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"JOSHAN\", \"AZAAN\"]',1),(76,'ALIASGAR MADRAS','60447215','ali_rashu143@yahoo.co.in','9884209587','2026-02-15 11:50:59.679697',0,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(77,'Mustafa Hararwala','40410068','mustafaharar@gmail.com','9840089782','2026-02-15 12:03:55.620985',0,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\", \"AZAAN\"]',1),(78,'Sk.moiz sk mohsin bhai kesharia','40414213','kausertradingco@yahoo.in','9841019552','2026-02-15 12:13:40.471070',0,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\", \"JOSHAN\", \"AZAAN\"]',1),(79,'Mehlam Hozefa Gajipurwala','50202244','fatema_totanawala@yahoo.com','7397346486','2026-02-15 12:38:30.904640',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(80,'IDRIS HOZEFA GAJIPURWALA','40916796','fatema_totanawala@yahoo.com','7397346486','2026-02-15 12:45:20.728378',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(81,'Murtaza Shabbir Karyanawala','40410440','mubarakgraphics@gmail.com','8838460458','2026-02-15 14:07:26.269223',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\", \"AZAAN\"]',1),(82,'Yusuf sk.juzerbhai ranujwala','40414176','yusufmalas@gmail.com','9941047050','2026-02-15 14:07:39.393727',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(85,'Kutbuddin','20376751','kutbuddin52@gmail.com','9789088528','2026-02-15 15:06:50.086728',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(86,'Mohammed Yunus bhai quilonwala','20362482','byagencies@gmail.com','9841878538','2026-02-15 17:00:07.825872',0,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(87,'Murtaza','60447600','savoyengrs100@gmail.com','9840753991','2026-02-15 17:14:22.243559',0,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\", \"JOSHAN\", \"AZAAN\"]',1),(88,'Yusuf shk mohammed bhai kitabi','40415378','yusufkitabi@gmail.com','9840928740','2026-02-16 01:53:47.744490',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(89,'Shk mohammed shk imran unjhawala','40414370','unjhawalamohammed35@gmail.com','9841069034','2026-02-16 04:07:35.305696',0,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(93,'MOHAMMED RANUJWALA','40411352','fastmaster2018@gmail.com','9445968049','2026-02-16 05:28:05.923375',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(98,'Mulla shabbir mulla abbas bhai chotaudaipurwala','20417673','qhs52_shabbir@yahoo.in','9566006032','2026-02-16 06:45:44.606292',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"YASEEN\", \"TAKHBIRA\", \"JOSHAN\", \"AZAAN\"]',1),(107,'Mushtaque altafhussain vahalabhai','20356371','ahmedmushtaq041@yahoo.com','+919003165522','2026-02-16 07:42:03.815247',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(109,'Ahamed Mushtaque Vahlabhai','40410719','ahmedmushtaq041@yahoo.com','9789302160','2026-02-16 08:22:15.766831',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(110,'Hyder jamnagarwala','40410787','hyderjamnagarwal07@gmail.com','9884115205','2026-02-16 09:14:07.906411',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\", \"TAKHBIRA\"]',1),(111,'Taher Mohammed Bhagat','60451171','taherbhagat8@gmail.com','07010579325','2026-02-16 11:46:00.607576',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\", \"TAKHBIRA\"]',1),(112,'Ammar Hasan bhai Kapi','40910776','Kapihasan@yahoo.in','6382612288','2026-02-16 12:10:37.852175',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(114,'Taha Aziz Kanorewala','60451742','hat.sakina@gmail.com','9444034436','2026-02-16 15:08:22.688059',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\", \"TAKHBIRA\", \"YASEEN\", \"TILAWAT\"]',1),(116,'Mohammed Murtaza Kagalwala','40908018','murtazakagal@yahoo.com','8778309707','2026-02-17 02:47:22.229733',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(122,'Shabbar Jabir','40410887','taiyabihydraulics@gmail.com','9884706034','2026-02-17 06:18:17.510269',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(132,'Mohammed dula','40920415','fdc5253@gmail.com','7550005253','2026-02-17 09:37:58.979308',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(148,'Huzefa  bhai gadli','20362182','huzefatoolshardware@yahoo.com','9840751955','2026-02-18 04:02:16.605873',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(149,'Aliasgar siamwala','40415737','intas78611053@gmail.com','8939443644','2026-02-18 04:36:42.716463',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(150,'Mufaddal Burhanuddin Chokhawala','40410261','chokhawalamufaddal@gmail.com','7358205602','2026-02-18 04:44:41.754803',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"YASEEN\", \"TAKHBIRA\", \"AZAAN\", \"TILAWAT\"]',1),(152,'Yusuf Shk Shabbir bhai Zaveri','40411127','yszaveri@gmail.com','09840265169','2026-02-18 04:54:41.619718',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(153,'Yusuf udaipur Bawa','12345677','abcd@gmail.com','9381037084','2026-02-18 05:58:07.307248',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(159,'Hussain Calicutwala','60451268','hcalicutwala@gmail.com','9791390853','2026-02-18 07:45:47.382756',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\"]',1),(160,'Mulla Aliasgar shk hussain Bhai Attarwala','40411479','aliakila@gmail.com','9840384786','2026-02-18 09:11:31.127423',0,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"JOSHAN\", \"YASEEN\", \"SANAH\", \"TAKHBIRA\", \"TILAWAT\", \"AZAAN\"]',1),(168,'Murtaza shabbir vadnagarwala','40414360','fatema.kaizar@gmail.com','8754079814','2026-02-19 09:03:30.835282',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(169,'Muffadal Bombaywala','60451152','muffadalbombay@gmail.com','8778839529','2026-02-19 11:35:39.950247',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"TILAWAT\", \"YASEEN\", \"AZAAN\"]',1),(170,'Adnan Bombaywala','60451151','adnanbombaywala01@gmail.com','8667367060','2026-02-19 11:45:44.359640',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"TILAWAT\", \"YASEEN\", \"AZAAN\"]',1),(171,'MOHAMMED A RAJA','20363312','mohammedraja53@gmail.com','09840077986','2026-02-19 15:55:27.293964',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(172,'Murtaza Saifuddinbhai patanwala','20363350','mspatanwala@gmail.com','9500076252','2026-02-19 17:11:43.851180',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(173,'M saifuddin y lokhandwala','40410739','matrade52@yahoo.com','9884209517','2026-02-20 04:47:00.091578',1,'APPROVED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(174,'Mohammed Bambot','40411623','ujjainwalaburhanuddin@gmail.com','9176552751','2026-02-20 07:48:03.119927',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(175,'Khuzema Taherbhai Zakir','20363437','caltrax_16@yahoo.com','9445560752','2026-02-20 13:30:20.976754',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(177,'Mulls Taher Shk Qaizar bhai Totanawala','60447237','htsm.chn@gmail.com','9500030352','2026-02-21 05:09:35.893696',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(178,'Ammar Hyderi','20313353','anishaideri@yahoo.com','9500132172','2026-02-21 17:32:40.120394',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(179,'Ibrahim Vithodawala','40410829','zenabia.sales@gmail.com','9176792137','2026-02-22 05:39:16.760189',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(180,'Mohammed Jangbar','30601063','mjangbar@gmail.com','7358413253','2026-02-22 06:58:33.055938',1,'APPROVED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\", \"AZAAN\"]',1),(181,'Shabbir Vakharia','30141238','shabbirvakharia22@gmail.com','09940152538','2026-02-22 09:30:20.727866',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"TILAWAT\", \"YASEEN\", \"AZAAN\"]',1),(182,'Hussain joher','50458107','fastmaster2018@gmail.com','7981461231','2026-02-23 06:06:57.859212',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(183,'Aliasgar Kitabi','40415074','rajtrading53@gmail.com','9962025152','2026-02-23 09:23:33.591051',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(184,'Ryan Reichert','Product','aglae_howe@zebyinbox.com','+447723176217','2026-02-24 01:50:05.951665',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"SANAH\", \"TILAWAT\", \"YASEEN\", \"JOSHAN\", \"TAKHBIRA\"]',1),(185,'Husain Bhagat','40414040','hussainbhagat52@gmail.com','9962417577','2026-02-24 01:56:28.297058',1,'ALLOTTED',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"YASEEN\", \"AZAAN\"]',1),(186,'Abbas dahodwala','60447827','abbasdahod99ad@gmail.com','8610792432','2026-02-24 07:26:32.030757',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(187,'Yusuf Attarwala','40411477','eminentyusuf@gmail.com','9840049065','2026-02-24 12:13:00.239035',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(188,'Idris Abdulhussain Bhai Pindwarawala','30900730','idrispin53@gmail.com','9150579052','2026-02-24 22:00:21.265977',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(189,'HUZAIFA M KESHARIA','40414245','huzboy52@gmail.com','08248861048','2026-02-25 14:30:49.333354',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\", \"AZAAN\"]',1),(190,'Khuzaima bhai Yunus bhai Nayyar','40405161','khuzemacool52@yahoo.com','8438001052','2026-02-25 23:03:49.012870',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(191,'Hussain Aziz kitabi','4041 5103','hussainkitabi94@gmail.com','9962483353','2026-02-26 05:39:55.739589',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1),(192,'Adnan Mulla Mufaddal bhai Chanasmawala','40910710','adnanmufaddal393@gmail.com','9176765152','2026-03-01 15:06:21.077449',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"TAKHBIRA\"]',1),(193,'Mustansir','30900731','sunelwalamustansir@gmail.com','6383273876','2026-03-01 16:47:35.176984',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"YASEEN\", \"AZAAN\", \"TAKHBIRA\"]',1),(194,'Mustansir Quilonwala','60447339','mmq5253@gmail.com','9962111761','2026-03-02 08:58:41.568544',1,'PENDING',NULL,NULL,NULL,NULL,'none',NULL,'[\"AZAAN\"]',1);
/*!40000 ALTER TABLE `registrations_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_registrationcorrection`
--

DROP TABLE IF EXISTS `registrations_registrationcorrection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_registrationcorrection` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `field_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `resolved_at` datetime(6) DEFAULT NULL,
  `registration_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `registrations_regist_registration_id_4aaabcfa_fk_registrat` (`registration_id`),
  CONSTRAINT `registrations_regist_registration_id_4aaabcfa_fk_registrat` FOREIGN KEY (`registration_id`) REFERENCES `registrations_registration` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_registrationcorrection`
--

LOCK TABLES `registrations_registrationcorrection` WRITE;
/*!40000 ALTER TABLE `registrations_registrationcorrection` DISABLE KEYS */;
INSERT INTO `registrations_registrationcorrection` VALUES (4,'full_name','Please use your full name as per ITS.','70ee2182b37f4088a9afac72bbc5c734','PENDING','2026-02-19 07:37:33.718866',NULL,160),(5,'full_name','Please use your full name as per ITS.','7470c4e063c54031ae1132c0adbbb7b0','RESOLVED','2026-02-19 07:38:02.905995','2026-02-19 07:43:45.063995',160),(6,'audition_files','PLZ UPLOAD UR RECORDING','92f65bef701242d394ef2194be80b1cb','PENDING','2026-02-21 11:00:17.393201',NULL,175),(7,'audition_files','PLZ UPLOAD UR RECORDING','baaa5f27f63d40d49a3a05bc405f157c','PENDING','2026-02-21 11:00:41.705077',NULL,172),(8,'audition_files','PLZ UPLOAD UR RECORDING','28323e978c2740a48318b97bcd07c231','RESOLVED','2026-02-21 11:01:06.356618','2026-02-22 05:56:52.405248',168);
/*!40000 ALTER TABLE `registrations_registrationcorrection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_reminder`
--

DROP TABLE IF EXISTS `registrations_reminder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_reminder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `scheduled_datetime` datetime(6) NOT NULL,
  `email_sent` tinyint(1) NOT NULL,
  `whatsapp_sent` tinyint(1) NOT NULL,
  `status` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_attempts` int NOT NULL,
  `whatsapp_attempts` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `sent_at` datetime(6) DEFAULT NULL,
  `last_error` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `duty_assignment_id` bigint NOT NULL,
  `whatsapp_message_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `whatsapp_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `duty_assignment_id` (`duty_assignment_id`),
  KEY `registratio_status_273425_idx` (`status`,`scheduled_datetime`),
  CONSTRAINT `registrations_remind_duty_assignment_id_654c3385_fk_registrat` FOREIGN KEY (`duty_assignment_id`) REFERENCES `registrations_dutyassignment` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_reminder`
--

LOCK TABLES `registrations_reminder` WRITE;
/*!40000 ALTER TABLE `registrations_reminder` DISABLE KEYS */;
INSERT INTO `registrations_reminder` VALUES (22,'2026-02-18 07:03:56.275273',1,0,'PENDING',1,2,'2026-02-16 06:39:19.833163',NULL,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AtrpLALkN9VttFzAfat6Uo_\'}',35,NULL,'FAILED'),(23,'2026-02-20 05:00:00.000000',0,0,'PENDING',0,0,'2026-02-16 06:41:38.696291',NULL,'',36,NULL,'none'),(24,'2026-02-16 05:00:00.000000',1,0,'PENDING',1,2,'2026-02-16 07:01:38.926684',NULL,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AmiX4qZWCmSCWiBaPaTKwmL\'}',37,NULL,'FAILED'),(25,'2026-02-16 10:10:00.000000',1,0,'PENDING',1,2,'2026-02-16 10:09:57.166730',NULL,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'Aim9_gduHUzk00Zj07YoMua\'}',38,NULL,'FAILED'),(26,'2026-02-17 10:10:00.000000',1,0,'PENDING',1,2,'2026-02-17 05:32:06.224204',NULL,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AqgvxvCQwrwk_ycK_lRKEED\'}',41,NULL,'FAILED'),(28,'2026-02-17 10:10:00.000000',1,0,'PENDING',1,2,'2026-02-17 05:32:33.589363',NULL,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'A_zw42MwJTEr-s4IdKaKtbW\'}',43,NULL,'FAILED'),(29,'2026-02-16 12:30:00.000000',1,0,'CANCELLED',1,2,'2026-02-17 05:46:24.969259',NULL,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AfV5fdXpP6Ze20yC0RQRAJA\'}',45,NULL,'FAILED'),(31,'2026-02-23 12:30:00.000000',0,0,'CANCELLED',0,0,'2026-02-17 08:45:49.940437',NULL,'',49,NULL,'none'),(33,'2026-02-16 12:30:00.000000',0,0,'CANCELLED',0,0,'2026-02-17 17:07:35.352137',NULL,'',51,NULL,'none'),(34,'2026-02-16 12:30:00.000000',1,1,'CANCELLED',1,1,'2026-02-17 17:13:38.458048','2026-02-17 17:15:02.885362','',52,'wamid.HBgMOTE4OTI1NzY5Nzg3FQIAERgSQ0MwN0VDQ0Y0QUI2QTNDODI2AA==','SENT'),(36,'2026-03-04 12:30:00.000000',0,0,'CANCELLED',0,0,'2026-02-17 17:35:41.694843',NULL,'',55,NULL,'none'),(37,'2026-02-17 12:30:00.000000',0,0,'CANCELLED',0,0,'2026-02-17 17:40:54.527622',NULL,'',56,NULL,'none'),(38,'2026-02-17 12:30:00.000000',1,1,'SENT',1,1,'2026-02-18 05:46:06.220562','2026-02-18 07:08:09.441843','',57,'wamid.HBgMOTE5Nzg5MzAyMTYwFQIAERgSNjgzRUU5M0FDQUE3OEZDQ0MxAA==','SENT'),(39,'2026-02-17 12:30:00.000000',1,0,'PENDING',1,2,'2026-02-18 05:51:25.303619',NULL,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AUSp9n8hujh-4hdYR8LD9_h\'}',58,NULL,'FAILED'),(40,'2026-02-18 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-18 05:58:55.801313',NULL,'',59,NULL,'none'),(41,'2026-02-18 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-18 05:59:28.606167',NULL,'',60,NULL,'none'),(43,'2026-02-16 12:30:00.000000',0,0,'CANCELLED',0,0,'2026-02-19 07:11:39.465091',NULL,'',62,NULL,'none'),(44,'2026-02-18 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-19 08:22:31.808571',NULL,'',64,NULL,'none'),(45,'2026-02-13 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-19 14:20:10.043641',NULL,'',65,NULL,'none'),(46,'2026-02-19 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-20 05:19:51.199448',NULL,'',66,NULL,'none'),(47,'2026-02-19 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-20 05:21:24.337087',NULL,'',67,NULL,'none'),(48,'2026-02-19 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-20 05:21:33.171187',NULL,'',68,NULL,'none'),(49,'2026-02-20 12:30:00.000000',0,0,'CANCELLED',0,0,'2026-02-20 05:23:25.013320',NULL,'',69,NULL,'none'),(50,'2026-02-19 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-20 05:24:56.884892',NULL,'',70,NULL,'none'),(51,'2026-02-20 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-20 05:28:06.530224',NULL,'',71,NULL,'none'),(52,'2026-02-19 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-20 05:33:28.533002',NULL,'',72,NULL,'none'),(53,'2026-02-20 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-20 09:28:29.002735',NULL,'',73,NULL,'none'),(54,'2026-02-20 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-20 09:31:07.887326',NULL,'',74,NULL,'none'),(55,'2026-02-21 12:30:00.000000',0,0,'CANCELLED',0,0,'2026-02-23 05:47:43.818276',NULL,'',75,NULL,'none'),(56,'2026-02-22 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-23 05:55:16.355398',NULL,'',76,NULL,'none'),(57,'2026-02-22 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-23 06:13:29.181595',NULL,'',77,NULL,'none'),(58,'2026-02-23 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-24 05:27:48.321963',NULL,'',78,NULL,'none'),(59,'2026-02-25 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-24 05:28:20.039168',NULL,'',79,NULL,'none'),(60,'2026-02-26 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-24 05:37:34.392366',NULL,'',80,NULL,'none'),(61,'2026-03-01 12:30:00.000000',0,0,'CANCELLED',0,0,'2026-02-24 05:38:31.705746',NULL,'',81,NULL,'none'),(62,'2026-02-27 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-24 05:40:47.200977',NULL,'',82,NULL,'none'),(63,'2026-02-28 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-24 05:41:22.031294',NULL,'',83,NULL,'none'),(64,'2026-02-24 12:30:00.000000',0,0,'PENDING',0,0,'2026-02-25 06:54:41.632587',NULL,'',84,NULL,'none'),(65,'2026-02-25 12:30:00.000000',0,0,'CANCELLED',0,0,'2026-02-26 05:30:32.848268',NULL,'',85,NULL,'none'),(66,'2026-03-02 12:30:00.000000',0,0,'PENDING',0,0,'2026-03-02 05:24:32.279934',NULL,'',86,NULL,'none');
/*!40000 ALTER TABLE `registrations_reminder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_reminderlog`
--

DROP TABLE IF EXISTS `registrations_reminderlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_reminderlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `channel` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `success` tinyint(1) NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `reminder_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `registrations_remind_reminder_id_9e6cf751_fk_registrat` (`reminder_id`),
  CONSTRAINT `registrations_remind_reminder_id_9e6cf751_fk_registrat` FOREIGN KEY (`reminder_id`) REFERENCES `registrations_reminder` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_reminderlog`
--

LOCK TABLES `registrations_reminderlog` WRITE;
/*!40000 ALTER TABLE `registrations_reminderlog` DISABLE KEYS */;
INSERT INTO `registrations_reminderlog` VALUES (1,'2026-02-16 17:45:02.074164','EMAIL',1,'Email sent to yusufmalas@gmail.com',22),(2,'2026-02-16 17:45:02.610857','WHATSAPP',0,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AtrpLALkN9VttFzAfat6Uo_\'}',22),(3,'2026-02-16 17:45:04.406802','EMAIL',1,'Email sent to bhftech.info@gmail.com',24),(4,'2026-02-16 17:45:04.913182','WHATSAPP',0,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AmiX4qZWCmSCWiBaPaTKwmL\'}',24),(5,'2026-02-16 17:45:12.421928','EMAIL',1,'Email sent to mubarakgraphics@gmail.com',25),(6,'2026-02-16 17:45:12.929878','WHATSAPP',0,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'Aim9_gduHUzk00Zj07YoMua\'}',25),(7,'2026-02-17 05:45:02.198249','EMAIL',1,'Email sent to mustafaharar@gmail.com',26),(8,'2026-02-17 05:45:02.739751','WHATSAPP',0,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AqgvxvCQwrwk_ycK_lRKEED\'}',26),(11,'2026-02-17 05:45:06.852717','EMAIL',1,'Email sent to qhs52_shabbir@yahoo.in',28),(12,'2026-02-17 05:45:07.282216','WHATSAPP',0,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'A_zw42MwJTEr-s4IdKaKtbW\'}',28),(13,'2026-02-17 06:00:02.139293','EMAIL',1,'Email sent to test@example.com',29),(14,'2026-02-17 06:00:03.190721','WHATSAPP',0,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AfV5fdXpP6Ze20yC0RQRAJA\'}',29),(15,'2026-02-17 17:15:02.028306','EMAIL',1,'Email sent to mukbambot118@gmail.com',34),(16,'2026-02-17 17:15:02.896105','WHATSAPP',1,'WhatsApp sent via template to 8925769787 (ID: wamid.HBgMOTE4OTI1NzY5Nzg3FQIAERgSQ0MwN0VDQ0Y0QUI2QTNDODI2AA==)',34),(17,'2026-02-18 06:00:01.944311','EMAIL',1,'Email sent to ahmedmushtaq041@yahoo.com',38),(18,'2026-02-18 06:00:02.944167','WHATSAPP',1,'WhatsApp sent via template to 9789302160 (ID: wamid.HBgMOTE5Nzg5MzAyMTYwFQIAERgSNjgzRUU5M0FDQUE3OEZDQ0MxAA==)',38),(19,'2026-02-18 07:08:12.777867','EMAIL',1,'Email sent to ezzykhadir53@gmail.com',39),(20,'2026-02-18 07:08:13.205109','WHATSAPP',0,'WhatsApp reminder failed: Template delivery failed: {\'message\': \'(#132018) There’s an issue with the parameters in your template\', \'type\': \'OAuthException\', \'code\': 132018, \'error_data\': {\'messaging_product\': \'whatsapp\', \'details\': \'Param text cannot have new-line/tab characters or more than 4 consecutive spaces\'}, \'fbtrace_id\': \'AUSp9n8hujh-4hdYR8LD9_h\'}',39);
/*!40000 ALTER TABLE `registrations_reminderlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registrations_unlocklog`
--

DROP TABLE IF EXISTS `registrations_unlocklog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrations_unlocklog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `unlocked_at` datetime(6) NOT NULL,
  `reason` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `unlocked_by` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `duty_date` date NOT NULL,
  `namaaz_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `original_user_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `original_user_its` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `duty_assignment_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `registrations_unlock_duty_assignment_id_afbc2670_fk_registrat` (`duty_assignment_id`),
  CONSTRAINT `registrations_unlock_duty_assignment_id_afbc2670_fk_registrat` FOREIGN KEY (`duty_assignment_id`) REFERENCES `registrations_dutyassignment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registrations_unlocklog`
--

LOCK TABLES `registrations_unlocklog` WRITE;
/*!40000 ALTER TABLE `registrations_unlocklog` DISABLE KEYS */;
INSERT INTO `registrations_unlocklog` VALUES (1,'2026-02-17 05:44:42.632396','Verification Test Reason for Unassignment','test_admin','2026-02-20','FAJAR_AZAAN','Test User','99999999',44),(2,'2026-02-17 05:46:40.115042','phone not reachable','40414853','2026-02-17','MAGRIB_TAKBIRA','Ammar Hasan bhai Kapi','40910776',NULL),(3,'2026-02-17 05:49:59.855129','not reachable','40414853','2026-02-17','MAGRIB_TAKBIRA','Saifuddin','30705811',NULL),(4,'2026-02-17 05:51:56.831484','Unassigned via Admin Dashboard','test_admin','2026-02-20','FAJAR_AZAAN','Test User','99999999',44),(6,'2026-02-17 06:02:11.132635','Unassigned via Admin Dashboard','admin_fix','2026-02-25','MAGRIB_AZAAN','Fix Test','88888888',47),(7,'2026-02-17 06:04:50.697113','Unassigned via Admin Dashboard','60451866','2026-02-17','SANAH','Test User','99999999',45),(8,'2026-02-17 08:45:55.822879','Unassigned via Admin Dashboard','60451866','2026-02-24','ZOHAR_AZAAN','mukarram','60451866',49),(9,'2026-02-17 17:08:13.239803','Unassigned via Admin Dashboard','60451866','2026-02-17','TAJWEED','mukarram','60451866',51),(11,'2026-02-17 17:35:41.690266','REALLOCATION: Moved from 2026-03-01 to 2026-03-05 by 40414853','40414853','2026-03-01','FAJAR_AZAAN','Test Reallocator','11111111',48),(12,'2026-02-17 17:38:58.716451','Unassigned via Admin Dashboard','60451866','2026-03-05','FAJAR_AZAAN','Test Reallocator','11111111',55),(13,'2026-02-17 17:40:54.521766','REALLOCATION: Moved from 2026-02-17 to 2026-02-18 by 60451866','60451866','2026-02-17','DUA_E_JOSHAN','mukarram','60451866',52),(14,'2026-02-17 17:41:09.892721','Unassigned via Admin Dashboard','60451866','2026-02-18','DUA_E_JOSHAN','mukarram','60451866',56),(15,'2026-02-19 07:13:10.004846','Unassigned via Admin Dashboard','60451866','2026-02-17','ZOHAR_AZAAN','mukarram','60451866',62),(16,'2026-02-19 08:23:41.819472','Unassigned via Admin Dashboard','40414853','2026-02-17','FAJAR_AZAAN','Taha Aziz Kanorewala','60451742',39),(17,'2026-02-21 04:58:22.631370','Unassigned via Admin Dashboard','40414853','2026-02-21','MAGRIB_AZAAN','M saifuddin y lokhandwala','40410739',69),(18,'2026-02-23 05:54:48.227850','Unassigned via Admin Dashboard','40414853','2026-02-22','MAGRIB_AZAAN','Moiz shk. Shamoon bhai Mandleywala','40411468',75),(19,'2026-02-26 05:37:06.946039','Unassigned via Admin Dashboard','40414853','2026-02-26','MAGRIB_TAKBIRA','Mohammed Jangbar','30601063',85),(20,'2026-03-02 05:24:08.884253','Unassigned via Admin Dashboard','40414853','2026-03-02','MAGRIB_AZAAN','Ammar Hyderi','20313353',81);
/*!40000 ALTER TABLE `registrations_unlocklog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-04 20:41:56
