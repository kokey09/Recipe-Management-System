/*
-- Query: SELECT * FROM recipedb.reviews
LIMIT 0, 1000

-- Date: 2023-12-18 03:30
*/
USE recipedb;

INSERT INTO `reviews` (`review_id`,`recipe_id`,`account_id`,`review_text`,`rating`,`date_created`,`image_url`) VALUES (1,4,2,'wow',4,'2023-12-18 03:27:10',NULL);
INSERT INTO `reviews` (`review_id`,`recipe_id`,`account_id`,`review_text`,`rating`,`date_created`,`image_url`) VALUES (2,6,2,'ahahahaha',4,'2023-12-18 03:27:25','static/reviews-img-table/5ca904b7fb71c25b3bdfa625390cb556.jpg');
