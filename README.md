## Grade Calculator
The grade calculator/predictor provides students with a tool to calculate their overall GPA/predict how many grades they need to get in a specified assignment/exam. Students are enrolled in several classes, so it can get difficult for them to calculate their GPA without any tools. This is where the grade calculator excels! The tool is user-friendly and all students can see their ranks among the whole dataset & share their ranks in social media!


### To start development:
#### 1. Install npm and node.js.
#### 2. Run `npm install` in the project's 'client' dir.
#### 3. Run `npm run dev` in the project's 'client' dir. The project will be deployed to: `localhost:5173` by default.
#### 4. Install the Mysql.server (my version is 5.7).
#### 5. Need to add any databases & tables you needed, here I used commands as below:
```bash
mysql -u root -p (the defaulted super administrator is 'root')


CREATE DATABASE `gpa` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;


-- gpa.course definition

CREATE TABLE `course` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `pass_line` int NOT NULL,
  `semester_id` bigint NOT NULL COMMENT '学期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_unique` (`title`,`semester_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


-- gpa.course_module definition

CREATE TABLE `course_module` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `grade_percentage` int DEFAULT NULL COMMENT '成绩占比',
  `test_score` int DEFAULT NULL COMMENT '测试满分',
  `current_score` int DEFAULT NULL COMMENT '已得分数',
  `course_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_module_unique` (`title`,`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


-- gpa.score definition

CREATE TABLE `score` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(500) COLLATE utf8mb4_bin NOT NULL,
  `avg_score` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `score_unique` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


-- gpa.semester definition

CREATE TABLE `semester` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `semester_unique` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


INSERT INTO semester
(id, title)
VALUES(1, 'the first semester');


INSERT INTO semester
(id, title)
VALUES(2, 'the second semester');
```
#### 6. Open another development tool's window for backend's python, you can choose python above 3.9's versions as the interpreter(only choose the 'server' dir as the root working dir for new window)
#### 7. In client's working dir, run 'pip install requirements.txt', then revise the 'db_config' & 'db_util' according to your settings; If you used above commands, only need to change the Mysql login password.
#### 8. Then run the 'app.py'.