/*
 Navicat Premium Data Transfer

 Source Server         : 113.62.127.198
 Source Server Type    : MySQL
 Source Server Version : 80016
 Source Host           : 113.62.127.198:3306
 Source Schema         : spider

 Target Server Type    : MySQL
 Target Server Version : 80016
 File Encoding         : 65001

 Date: 03/08/2019 16:51:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for news_qq
-- ----------------------------
DROP TABLE IF EXISTS `news_qq`;
CREATE TABLE `news_qq` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `title` varchar(1024) DEFAULT NULL COMMENT '新闻标题',
  `content` text COMMENT '新闻内容',
  `url` varchar(1024) DEFAULT NULL COMMENT '新闻URL',
  `pub_time` varchar(255) DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
