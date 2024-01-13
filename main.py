def get_file_enc(file_name):
    import chardet
    file_path = get_file_path(file_name)
    rawdata = open(file_path, 'rb').read()
    file_enc = chardet.detect(rawdata)['encoding']
    return file_enc


def get_file_path(file_name):
    import os
    file_path = os.path.join(os.getcwd(), file_name)
    return file_path


def get_list_by_file(file_name: str) -> list:
    file_path = get_file_path(file_name)
    file_enc = get_file_enc(file_path)
    with open(file_path, encoding=file_enc) as f:
        result = [x.strip('\n') for x in f.readlines() if x.strip('\n') != '']
    return result


def get_cook_book(cook_list: list) -> dict:
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


shop_list = get_shop_list_by_dishes(['Омлет', 'Фахитос'], 2)
print(shop_list)


def get_merged_text(*files: str):
    file_dict = {}
    for file in files:
        file_dict[file] = len(get_list_by_file(file))
    sorted_file = sorted(file_dict.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_file}
    for i, (k, v) in enumerate(sorted_dict.items()):
        file_enc = get_file_enc(k)
        file_list = [k, str(v)]
        file_list.extend(get_list_by_file(k))
        lined_list = [x+'\n' for x in file_list]
        if i == 0:
            with open('merged_file.txt', 'w', encoding=file_enc) as f:
                f.writelines(lined_list)
        else:
            with open('merged_file.txt', 'a', encoding=file_enc) as f:
                f.writelines(lined_list)
    file_path = get_file_path('merged_file.txt')
    return file_path


merged_text = get_merged_text('1.txt', '2.txt', '3.txt')
print(merged_text)
