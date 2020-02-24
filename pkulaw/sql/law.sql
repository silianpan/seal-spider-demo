/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80013
 Source Host           : localhost:3306
 Source Schema         : pkulaw

 Target Server Type    : MySQL
 Target Server Version : 80013
 File Encoding         : 65001

 Date: 24/02/2020 09:31:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for law
-- ----------------------------
DROP TABLE IF EXISTS `law`;
CREATE TABLE `law` (
  `title` varchar(255) NOT NULL COMMENT '标题',
  `pub_dept` varchar(255) DEFAULT NULL COMMENT '发布部门',
  `pub_no` varchar(255) DEFAULT NULL COMMENT '发文字号',
  `pub_date` varchar(32) DEFAULT NULL COMMENT '发布日期',
  `law_type` varchar(128) DEFAULT NULL COMMENT '法规类别',
  `force_level` varchar(32) DEFAULT NULL COMMENT '效力级别',
  `time_valid` varchar(32) DEFAULT NULL COMMENT '时效性',
  `impl_date` varchar(32) DEFAULT NULL COMMENT '实施日期',
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '内容',
  `url` varchar(255) NOT NULL COMMENT 'url',
  `type` varchar(128) DEFAULT NULL COMMENT '类别',
  `deadline` varchar(32) DEFAULT NULL COMMENT '截止日期',
  `appr_dept` varchar(255) DEFAULT NULL COMMENT '批准部门',
  `appr_date` varchar(32) DEFAULT NULL COMMENT '批准日期',
  `pdf_url` varchar(255) DEFAULT NULL COMMENT '文件路径',
  `crt_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `upd_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `del_flag` bit(1) DEFAULT b'0' COMMENT '删除标志',
  PRIMARY KEY (`title`,`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='中央法规';

SET FOREIGN_KEY_CHECKS = 1;
