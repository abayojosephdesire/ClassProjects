"""
6.101 Lab 5:
Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def atomic_ingredient_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    atomic_recipes = {}  # Maps atomic food items to their costs
    for recipe in recipes:
        if recipe[0] == "atomic":
            atomic_recipes[recipe[1]] = recipe[2]

    return atomic_recipes


def compound_ingredient_possibilities(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    compound_recipes = {}  # Maps compound food items to their ingredients
    for recipe in recipes:
        if recipe[0] == "compound":
            compound_recipes.setdefault(recipe[1], []).append(recipe[2])

    return compound_recipes


def lowest_cost(recipes, food_item, restrictions=[]):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    compound_recipes = compound_ingredient_possibilities(recipes)
    atomic_recipes = atomic_ingredient_costs(recipes)

    # Recursive function that goes though all possible recipes
    def recipe_cost(recipe):
        if not recipe:  # Base case
            return 0

        # Restrictions -- Like dietary restrictions
        if recipe[0][0] in restrictions:
            return float("inf")
        # Recursive case -- recipe in atomic_recipes
        if recipe[0][0] in atomic_recipes:
            return atomic_recipes[recipe[0][0]] * recipe[0][1] + recipe_cost(recipe[1:])

        # Recursive case -- recipe in compound_recipes
        if recipe[0][0] in compound_recipes:
            return min(
                recipe_cost(item) for item in compound_recipes[recipe[0][0]]
            ) * recipe[0][1] + recipe_cost(recipe[1:])

        # If the recipe is not available, set ip to infinity
        # The min() will remove that infinity case, without affecting others
        return float("inf")

    if food_item not in restrictions:
        if food_item in compound_recipes:
            return min(
                (
                    recipe_cost(recipe)
                    for recipe in compound_recipes[food_item]
                    if recipe_cost(recipe) != float("inf")
                ),
                default=None,
            )
        elif food_item in atomic_recipes:
            return atomic_recipes[food_item]
    return None


def scaled_flat_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    scaled_ingredients = {}
    for ingredient, quantity in flat_recipe.items():
        scaled_ingredients[ingredient] = quantity * n

    return scaled_ingredients


def add_flat_recipes(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        add_flat_recipes([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    all_recipes = {}
    for recipe in flat_recipes:
        for ingredient, quantity in recipe.items():
            if ingredient in all_recipes:
                all_recipes[ingredient] += quantity
            else:
                all_recipes[ingredient] = quantity

    return all_recipes


def cheapest_flat_recipe(recipes, food_item, restrictions=[]):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    compound_recipes = compound_ingredient_possibilities(recipes)
    atomic_recipes = atomic_ingredient_costs(recipes)

    def find_cheapest_recipe(food):
        if food in restrictions:
            return {food: float("inf")}

        if food in atomic_recipes:  # Atomic recipes
            return {food: 1}

        if food in compound_recipes:  # Compound recipes
            # Possible combinations to make food
            food_ingredients = compound_recipes[food]
            cheapest_ingredients = {}
            # Example: [[(),()], [()], [(),()]]
            for ingredients in food_ingredients:
                resulting_ingredients = []
                # List of ingredients [(), (), ()]
                for food_item in ingredients:
                    resulting_ingredients.append(
                        scaled_flat_recipe(
                            find_cheapest_recipe(food_item[0]), food_item[1]
                        )
                    )
                added_recipes = add_flat_recipes(resulting_ingredients)

                # Update the recipe if the cost is less
                if not cheapest_ingredients:
                    cheapest_ingredients = added_recipes
                elif sum(
                    (
                        atomic_recipes[recipe_name] * recipe_quantity
                        if recipe_name in atomic_recipes
                        else float("inf")
                    )
                    for (recipe_name, recipe_quantity) in added_recipes.items()
                ) < sum(
                    (
                        atomic_recipes[recipe_name] * recipe_quantity
                        if recipe_name in atomic_recipes
                        else float("inf")
                    )
                    for (recipe_name, recipe_quantity) in cheapest_ingredients.items()
                ):
                    cheapest_ingredients = added_recipes

            return cheapest_ingredients if cheapest_ingredients else {}

        return {food: float("inf")}

    result = find_cheapest_recipe(food_item)
    if sum(result.values()) != float("inf") and result:
        return result


def combined_flat_recipes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes for a certain ingredient, compute and return a list of flat
    recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """

    def helper(recipes):  # Simply avoids mutations
        if not recipes:  # Base case
            return [{}]

        first_recipe, other_recipes = recipes[0], recipes[1:]
        combined_recipes = []
        for first_ingr in first_recipe:  # Recursive case
            for other_ingr in helper(other_recipes):
                combined_recipes.append(
                    {
                        key: first_ingr.get(key, 0) + other_ingr.get(key, 0)
                        for key in set(first_ingr) | set(other_ingr)
                    }
                )
        return combined_recipes

    return helper(flat_recipes)


def all_flat_recipes(recipes, food_item, restrictions=[]):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    compound_recipes = compound_ingredient_possibilities(recipes)
    atomic_recipes = atomic_ingredient_costs(recipes)

    def helper(food):
        if food in restrictions:  # Handles restrictions - Like dietary restrictions
            return [{food: float("inf")}]

        if food in atomic_recipes:  # Base case for atomic recipes
            return [{food: 1}]

        if food in compound_recipes:  # Recursion for compound recipes
            food_recipes = []
            for ingredients in compound_recipes[food]:
                resulting_ingredients = []
                for food_name, quantity in ingredients:
                    flat_recipes = helper(food_name)
                    scaled_recipes = [
                        scaled_flat_recipe(food, quantity) for food in flat_recipes
                    ]
                    resulting_ingredients.append(scaled_recipes)
                food_recipes += combined_flat_recipes(resulting_ingredients)

            return food_recipes

        return [{food: float("inf")}]

    result = helper(food_item)
    return [recipe for recipe in result if sum(recipe.values()) != float("inf")]


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    # you are free to add additional testing code here!

    # example_recipes = [
    #     (
    #         "compound",
    #         "chili",
    #         [
    #             ("beans", 3),
    #             ("cheese", 10),
    #             ("chili powder", 1),
    #             ("cornbread", 2),
    #             ("protein", 1),
    #         ],
    #     ),
    #     ("atomic", "beans", 5),
    #     (
    #         "compound",
    #         "cornbread",
    #         [("cornmeal", 3), ("milk", 1), ("butter", 5), \
    #           ("salt", 1), ("flour", 2)],
    #     ),
    #     ("atomic", "cornmeal", 7.5),
    #     (
    #         "compound",
    #         "burger",
    #         [("bread", 2), ("cheese", 1), ("lettuce", 1), \
    #           ("protein", 1), ("ketchup", 1)],
    #     ),
    #     (
    #         "compound",
    #         "burger",
    #         [
    #             ("bread", 2),
    #             ("cheese", 2),
    #             ("lettuce", 1),
    #             ("protein", 2),
    #         ],
    #     ),
    #     ("atomic", "lettuce", 2),
    #     ("compound", "butter", [("milk", 1), ("butter churn", 1)]),
    #     ("atomic", "butter churn", 50),
    #     ("compound", "milk", [("cow", 1), ("milking stool", 1)]),
    #     ("compound", "cheese", [("milk", 1), ("time", 1)]),
    #     ("compound", "cheese", [("cutting-edge laboratory", 11)]),
    #     ("atomic", "salt", 1),
    #     ("compound", "bread", [("yeast", 1), ("salt", 1), ("flour", 2)]),
    #     ("compound", "protein", [("cow", 1)]),
    #     ("atomic", "flour", 3),
    #     ("compound", "ketchup", [("tomato", 30), ("vinegar", 5)]),
    #     ("atomic", "chili powder", 1),
    #     (
    #         "compound",
    #         "ketchup",
    #         [("tomato", 30), ("vinegar", 3), ("salt", 1), \
    #           ("sugar", 2), ("cinnamon", 1)],
    #     ),  # the fancy ketchup
    #     ("atomic", "cow", 100),
    #     ("atomic", "milking stool", 5),
    #     ("atomic", "cutting-edge laboratory", 1000),
    #     ("atomic", "yeast", 2),
    #     ("atomic", "time", 10000),
    #     ("atomic", "vinegar", 20),
    #     ("atomic", "sugar", 1),
    #     ("atomic", "cinnamon", 7),
    #     ("atomic", "tomato", 13),
    # ]

    # print(cheapest_flat_recipe(example_recipes, "burger", ("vinegar", "milk")))

    # print(combined_flat_recipes(
    #     [
    #         [{'peanut butter': 1}, {'almond butter': 1}],
    #         [{'jelly': 2}],
    #         [{'heyy': 1}, {'water': 1}],
    #     ],
    # ))

    # print(combined_flat_recipes(
    #     [
    #         [{"a": 1}],
    #         [{"a": 1, "b": 2}]
    #     ]
    # ))

    # print(all_flat_recipes(example_recipes, "protein"))
