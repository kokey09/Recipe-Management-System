
CREATE USER 'dashboard'@'localhost' IDENTIFIED BY 'dashboard';

GRANT ALL PRIVILEGES ON recipedb.* TO 'dashboard'@'localhost';

FLUSH PRIVILEGES;

CREATE DATABASE recipedb;

USE recipedb;


CREATE TABLE account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password VARCHAR(60),
    date_created TIMESTAMP,
    type VARCHAR(50),
    is_deleted TINYINT(1),
	status ENUM('unverified', 'verified') DEFAULT 'unverified'
);

CREATE TABLE recipes (
  recipe_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  instructions TEXT,
  image_url VARCHAR(512),
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at DATETIME DEFAULT NULL,
  deleted_by INT,
  recovered_at DATETIME DEFAULT NULL,
  recovered_by INT,
  account_id INT,
  status ENUM('pending', 'declined', 'approved') NOT NULL DEFAULT 'pending',
  status_changed_at DATETIME DEFAULT NULL,
  status_changed_by INT,
  FOREIGN KEY (`account_id`) REFERENCES `account`(`id`),
  FOREIGN KEY (`deleted_by`) REFERENCES `account`(`id`),
  FOREIGN KEY (`recovered_by`) REFERENCES `account`(`id`),
  FOREIGN KEY (`status_changed_by`) REFERENCES `account`(`id`)
);




CREATE TABLE ingredients (
    ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);



CREATE TABLE recipe_ingredients (
     recipe_id INT(11),
     ingredient_id INT(11),
     FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
     FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE reviews (
    review_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT(11),
    account_id INT(11),
    review_text TEXT,
    rating INT(5),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_url VARCHAR(512),
    FOREIGN KEY (account_id) REFERENCES account(id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);

CREATE TABLE favorites (
    favorite_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT(11),
    account_id INT(11),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted TINYINT(1),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (account_id) REFERENCES account(id)
);