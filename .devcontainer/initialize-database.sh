#!/bin/sh
set -eu
sudo service mysql start
sudo mysql < database/initialization.sql
sudo mysql < database/account.sql
sudo mysql < database/recipes.sql
sudo mysql < database/ingredients.sql
sudo mysql < database/recipe_ingredients.sql
sudo mysql < database/reviews.sql
sudo mysql < database/favorites.sql