/*
-- Query: SELECT * FROM recipedb.account
LIMIT 0, 1000

-- Date: 2023-12-18 03:28
*/
USE recipedb;

INSERT INTO `account` (`id`,`username`,`email`,`password`,`date_created`,`type`,`is_deleted`,`status`) VALUES (1,'admin','admin@gmail.com','$2b$12$Nsyi97BcA9ZnwNHC91CY8ulRq7CdRJjS4P69jZMg7mE648Ntj.B96','2023-12-17 18:29:37','admin',0,'verified');
INSERT INTO `account` (`id`,`username`,`email`,`password`,`date_created`,`type`,`is_deleted`,`status`) VALUES (2,'khim','khimrata11@gmail.com','$2b$12$1uiw0uEP9CbDZ.3zg/scsO3ZWdrYsj52JYP2xAHIb3LKKWV.nMd9i','2023-12-17 18:38:00','normal',0,'verified');
INSERT INTO `account` (`id`,`username`,`email`,`password`,`date_created`,`type`,`is_deleted`,`status`) VALUES (3,'cerbenus','cerbenus09@gmail.com','$2b$12$Jfyeu8OsewZ4l77kv9urGufdWBxzGURlTOSuUTl0xNdBsxIa.7Ml6','2023-12-17 18:38:33','admin',0,'verified');
