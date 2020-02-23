-- MySQL dump 10.13  Distrib 5.7.20, for Win64 (x86_64)
--
-- Host: localhost    Database: renrendai
-- ------------------------------------------------------
-- Server version	5.7.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tbl_bmessage`
--

DROP TABLE IF EXISTS `tbl_bmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_bmessage` (
  `loan_id` int(11) NOT NULL COMMENT 'loanId',
  `nick_name` varchar(50) DEFAULT NULL COMMENT '昵称',
  `credit_rating` varchar(50) DEFAULT NULL COMMENT '信用评级',
  `name` varchar(20) DEFAULT NULL COMMENT '姓名',
  `identify` varchar(20) DEFAULT NULL COMMENT '身份证号',
  `age` varchar(5) DEFAULT NULL COMMENT '年龄',
  `degree` varchar(20) DEFAULT NULL COMMENT '学历',
  `marriage` varchar(20) DEFAULT NULL COMMENT '婚姻',
  `loan` varchar(20) DEFAULT NULL COMMENT '申请借款',
  `loc` varchar(20) DEFAULT NULL COMMENT '信用额度',
  `overdue` varchar(20) DEFAULT NULL COMMENT '逾期金额',
  `success` varchar(20) DEFAULT NULL COMMENT '成功借款',
  `total` varchar(20) DEFAULT NULL COMMENT '借款总额',
  `overdue_amount` varchar(20) DEFAULT NULL COMMENT '逾期次数',
  `pay_num` varchar(20) DEFAULT NULL COMMENT '还清笔数',
  `non_pay` varchar(20) DEFAULT NULL COMMENT '代还本息',
  `serious_overdue` varchar(20) DEFAULT NULL COMMENT '严重逾期',
  `income` varchar(30) DEFAULT NULL COMMENT '收入',
  `estate` varchar(20) DEFAULT NULL COMMENT '房产',
  `hose_loan` varchar(20) DEFAULT NULL COMMENT '房贷',
  `car` varchar(20) DEFAULT NULL COMMENT '车产',
  `car_loan` varchar(20) DEFAULT NULL COMMENT '车贷',
  `other` varchar(20) DEFAULT NULL COMMENT '其他',
  `industy` varchar(20) DEFAULT NULL COMMENT '公司行业',
  `scale` varchar(20) DEFAULT NULL COMMENT '公司规模',
  `career` varchar(20) DEFAULT NULL COMMENT '岗位职业',
  `city` varchar(30) DEFAULT NULL COMMENT '工作城市',
  `work_time` varchar(30) DEFAULT NULL COMMENT '工作时间',
  `value_date` varchar(30) DEFAULT NULL COMMENT '起息日',
  `err` varchar(20) DEFAULT NULL COMMENT '提前还款率',
  `risk_level` varchar(20) DEFAULT NULL COMMENT '风险等级',
  `repayment_mode` varchar(20) DEFAULT NULL COMMENT '还款方式',
  `repayment_source` varchar(20) DEFAULT NULL COMMENT '还款来源',
  `frd` varchar(20) DEFAULT NULL COMMENT '首还款日期',
  `sex` varchar(20) DEFAULT NULL COMMENT '性别',
  PRIMARY KEY (`loan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='基础信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_check_state`
--

DROP TABLE IF EXISTS `tbl_check_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_check_state` (
  `loan_id` int(11) NOT NULL,
  `project` varchar(20) DEFAULT NULL COMMENT '审核项目',
  `state` varchar(20) DEFAULT NULL COMMENT '状态',
  `pass_date` varchar(20) DEFAULT NULL COMMENT '通过日期',
  KEY `tbl_check_state_tbl_bmessage_loan_id_fk` (`loan_id`),
  CONSTRAINT `tbl_check_state_tbl_bmessage_loan_id_fk` FOREIGN KEY (`loan_id`) REFERENCES `tbl_bmessage` (`loan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='检查状态';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_repayment`
--

DROP TABLE IF EXISTS `tbl_repayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_repayment` (
  `loan_id` int(11) NOT NULL,
  `repayTime` varchar(32) DEFAULT NULL COMMENT '合约还款日期',
  `repayType` varchar(30) DEFAULT NULL COMMENT '状态',
  `unRepaidAmount` varchar(20) DEFAULT NULL COMMENT '应还本息',
  `repaidFee` varchar(20) DEFAULT NULL COMMENT '应付罚息',
  `actualRepayTime` varchar(32) DEFAULT NULL COMMENT '实际还款日期',
  KEY `tbl_repayment_tbl_bmessage_loan_id_fk` (`loan_id`),
  CONSTRAINT `tbl_repayment_tbl_bmessage_loan_id_fk` FOREIGN KEY (`loan_id`) REFERENCES `tbl_bmessage` (`loan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='还款表现';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-23 10:18:13
