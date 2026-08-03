from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}


def calculator(request, recipe_name):

    base_recipe = DATA.get(recipe_name, {})
    servings_str = request.GET.get('servings', '1')
    servings = int(servings_str)
    if servings < 1:
        servings = 1
    context_recipe = {}
    for ingredient, amount in base_recipe.items():
        # Округляем до двух знаков после запятой для красивого вывода
        scaled_amount = round(amount * servings, 2)
        context_recipe[ingredient] = scaled_amount

    context = {
        'recipe': context_recipe,
        'servings': servings
    }

    return render(request, 'calculator/index.html', context)
