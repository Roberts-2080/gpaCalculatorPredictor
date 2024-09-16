-- 排名表

CREATE TABLE `score` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(500) COLLATE utf8mb4_bin NOT NULL,
  `avg_score` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `score_unique` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;