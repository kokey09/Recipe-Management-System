# Recipe Management System

## Usage
### Codespaces
1. `python app.py`

### Local
1. `pip install -r requirements.txt`
2. `mysql < database_query.sql && mysql < database/account.sql && mysql < database/recipes.sql && mysql < database/ingredients.sql && mysql < database/recipe_ingredients.sql`
3. `python app.py`

## Flowchart
### Implemented
```mermaid
flowchart TD
  subgraph Admin[Admin]
    StartAdmin([Start]) --> GoToWebsiteAdmin[Go to website]
    GoToWebsiteAdmin --> Login[Login]
    Login --> AddRecipe[Add recipe]
    Login --> EditRecipe[Edit recipe]
      EditRecipe --> UpdateRecipe[Update recipe]
      EditRecipe --> DeleteRecipe[Delete recipe]
  end
  subgraph EndUser[End user]
    StartEndUser([Start]) --> GoToWebsiteEndUser[Go to website]
    GoToWebsiteEndUser --> SearchRecipes{Search recipes}
    SearchRecipes --> |Recipe exists| DisplayRecipe[Display recipe]
    DisplayRecipe --> SearchRecipes
    SearchRecipes --> |Recipe does not exist| RecipeNotFound[Recipe not found]
    RecipeNotFound -->SearchRecipes
  end
```

### Proposed
```mermaid
flowchart TD
  subgraph Admin[Admin]
    StartAdmin([Start]) --> GoToWebsiteAdmin[Go to website]
    GoToWebsiteAdmin --> LoginToDashboard[Login to Dashboard]
    LoginToDashboard --> AddRecipe[Add recipe]
    LoginToDashboard --> EditRecipe[Edit recipe]
      EditRecipe --> UpdateRecipe[Update recipe]
      EditRecipe --> DeleteRecipe[Delete recipe]
    LoginToDashboard --> ListOfRequestedRecipes[List of requested recipes]
      ListOfRequestedRecipes --> AddRecipe
  end
  subgraph EndUser[End user]
    StartEndUser([Start]) --> GoToWebsiteEndUser[Go to website]
    GoToWebsiteEndUser --> SearchRecipes{Search recipes}
    SearchRecipes --> |Recipe exists| DisplayRecipe[Display recipe]
      DisplayRecipe --> RateRecipe{Rate recipe?}
        RateRecipe --> |Yes| InputRating[/Input rating/]
          InputRating --> SearchRecipes
        RateRecipe --> |No| SearchRecipes
    SearchRecipes --> |Recipe does not exist| RecipeNotFound[Recipe not found]
      RecipeNotFound --> RequestRecipe{Request recipe?}
        RequestRecipe --> |Yes| ListOfRequestedRecipes
        RequestRecipe --> |No| SearchRecipes
  end
```