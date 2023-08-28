/*
 Navicat Premium Data Transfer

 Source Server         : LocalTestServer
 Source Server Type    : MySQL
 Source Server Version : 50740 (5.7.40-log)
 Source Host           : 10.1.0.110:3306
 Source Schema         : RDPS

 Target Server Type    : MySQL
 Target Server Version : 50740 (5.7.40-log)
 File Encoding         : 65001

 Date: 28/08/2023 03:22:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for rdps
-- ----------------------------
DROP TABLE IF EXISTS `rdps`;
CREATE TABLE `rdps`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lasttime` datetime NULL DEFAULT NULL,
  `activedays` int(255) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Event structure for Autodelete
-- ----------------------------
DROP EVENT IF EXISTS `Autodelete`;
delimiter ;;
CREATE EVENT `Autodelete`
ON SCHEDULE
EVERY '1' DAY STARTS '2023-08-28 01:13:15'
DO BEGIN
	DELETE FROM rdps
	WHERE	NOW() > STR_TO_DATE(lasttime,'%Y-%m-%d %H:%i:%s');
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table rdps
-- ----------------------------
DROP TRIGGER IF EXISTS `generate_token`;
delimiter ;;
CREATE TRIGGER `generate_token` BEFORE INSERT ON `rdps` FOR EACH ROW BEGIN
	SET NEW.token = UUID();
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
