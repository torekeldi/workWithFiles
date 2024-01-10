import os
import chardet


def get_list_by_file(file_name: str) -> list:
    """

    returns a list from a given file

    """
    file_path = os.path.join(os.getcwd(), file_name)
    rawdata = open(file_name, 'rb').read()
    file_enc = chardet.detect(rawdata)['encoding']
    with open(file_path, encoding=file_enc) as f:
        result = [x.strip('\n') for x in f.readlines() if x.strip('\n') != '']
    return result


def get_cook_book(cook_list: list) -> dict:
    """

    returns a dict from a given list

    dict structure goes by like this: {dish_str: ingredient_list}

    ingredient_list structure goes by like this: {'ingredient_name': str, 'quantity': int, 'measure': str}

    """
    cook_dict = {}
    dish = [x for x in cook_list if x.find('|') == -1 and not x.isdigit()]
    ing_quantity = [int(x) for x in cook_list if x.isdigit()]
    ing = [x for x in cook_list if x.find('|') != -1]
    start = 0
    for d, q in zip(dish, ing_quantity):
        ing_list = ing[start:start + q]
        cook_value = []
        for ing_str in ing_list:
            cut_list = ing_str.split(' | ')
            cook_value.append({'ingredient_name': cut_list[0], 'quantity': cut_list[1], 'measure': cut_list[2]})
        cook_dict[d] = cook_value
        start += q
    return cook_dict


def get_shop_list_by_dishes(dishes: list, person_count: int) -> dict:
    """

    returns a dict from a given dishes list and person count

    dict structure goes by like this: {ingredient_str: quantity_dict}

    quantity_dict structure goes by like this: {'measure': str, 'quantity': int}

    """
    cook_book = get_cook_book(get_list_by_file('recipes.txt'))
    ing_dict = {}
    for dish in dishes:
        if dish in cook_book:
            for ing in cook_book[dish]:
                if ing_dict.get(ing['ingredient_name']):
                    quantity_value = ing_dict.get(ing['ingredient_name'])['quantity']
                    dict_value = {'measure': ing['measure'],
                                  'quantity': quantity_value + int(ing['quantity']) * person_count}
                    ing_dict[ing['ingredient_name']] = dict_value
                else:
                    dict_value = {'measure': ing['measure'], 'quantity': int(ing['quantity']) * person_count}
                    ing_dict[ing['ingredient_name']] = dict_value
    return ing_dict


b = get_shop_list_by_dishes(['Омлет', 'Фахитос'], 1)
print(b)
