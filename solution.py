import pandas as pd
from fuzzywuzzy import fuzz

def get_not_continuous_words(data: pd.DataFrame) -> str: 
    """Separate the combined words in a column 'name'.
    
    Args:
        data: list of produscts produced and distributed by the manufacturer.

    Returns:
        not continuous words in the names of the manufacturer's products.
    """
    list_product_word = [
        'PROSEPT', 
        'концентрат', 
        'Crystal', 
        'готовый', 
        'Duty', 
        'Multipower', 
        'MULTIPOWER', 
        'White', 
        'Belizna',
        'Cooky', 
        'Diona', 
        'готовое', 
        'ULTRA', 
        'Antifoam', 
        'Bath', 
        'Universal', 
        'Carpet', 
        'концентрированное', 
        'Flox', 
        'эффектом', 
        'splash', 
        'epoxy', 
        'Candy', 
        'Optic', 
        'Clean', 
        'шампунь', 
        'штуки', 
        'Super', 
        'Plastix', 
        'Proplast', 
        'Ириса', 
        'FLOX'
    ]

    result = data['name']
    if (pd.isna(result)):
        return '-'
    else:
        for word in list_product_word:
            tmp_str = result.split(str(word))
            if len(tmp_str) > 1:
                result = tmp_str[0] + ' ' + word + ' ' + tmp_str[1]

        return result

def get_not_continuous_words_when_entering(row: str)  -> str:
    """Separates merged words when entering a dealer product.
    
    Args:
        row: product sold by dealer.

    Returns:
        there are no merged words when entering a dealer product.
    """
    list_product_dealer = [
        'антижук', 
        'PROSEPT', 
        'universal', 
        'ULTRA', 
        'grill', 
        'удаления',
        'floor', 
        'remover', 
        'средство', 
        'стекол', 
        'зеркал', 
        'пластика',
        'акриловых', 
        'bath', 
        'acryl', 
        'profi', 
        'Eco', 
        'multipower', 
        'xm11',
        'graffiti', 
        'плесени', 
        'грибка', 
        'gel', 
        'снятия', 
        'shine', 
        'грунтовка',
        '20л',
        '10л', 
        '2л', 
        'hand', 
        'cristal', 
        'против', 
        'лак', 
        'полуматовый',
        'глянцевый', 
        'невымываемый', 
        'машины', 
        'splash', 
        'орех', 
        'сlean', 
        'acid',
        'polish', 
        'удаления', 
        'hard', 
        'посуды', 
        'полов', 
        'комнат',  
        'spray',
        'посудомоечной', 
        'lime', 
        'rinser', 
        'sport', 
        'спортивной', 
        'черных',
        'black', 
        'сауны', 
        'бани', 
        'труб', 
        'засоров', 
        'extra', 
        'после',
        'очистки', 
        'ухода', 
        'мебелью', 
        'зеленый', 
        'красный',
        'fungi', 
        'Crystal', 
        'концентрат',
        'Cooky'
    ]
    result = row
    for word in list_product_dealer:
        tmp_str = result.split(str(word))
        if len(tmp_str) > 1:
            result = tmp_str[0] + ' ' + word + ' ' + tmp_str[1]
    return result

def get_suitable_products(
        dealer_product: str, 
        manufacturer_products: pd.Series,
        levenshtein_distance_max: int,
    ) -> list:
    """Create a model explanation system.

    Args:
        dealer_product: product sold by dealer.
        manufacturer_products: list of the manufacturer products.
        levenshtein_distance_max: difference between the names of two products.
        
    Returns: 
        Array of suitable manufactur products.
    """
    suitable_products = []
    for i in range(len(manufacturer_products)):
        product = manufacturer_products['name_split'][i]
        l_d = fuzz.token_sort_ratio(
            get_not_continuous_words_when_entering(dealer_product),
            product,
        )
        if l_d >= levenshtein_distance_max:
            manufacturer_products_id = manufacturer_products[
                manufacturer_products['name_split'] == product
            ]['id'].to_string(index=False)
            suitable_products.append(
                {
                    'id': manufacturer_products.loc[i]['id'],
                    'product_name': manufacturer_products['name'][i],
                    'levenshtein_distance': l_d,
                },
            )
    return suitable_products
    

def get_solution(
        dealer_product: str,
        length: int = 10,
        levenshtein_distance_max: int = 50,
    ) -> list:
    """Sorting recommended manufacturer products in descending order of Levenshtein distance.
    
    Args:
        dealer_product: product sold by dealer,
        length: length of the list of recommended products,
        levenshtein_distance_max: difference between the names of two products.

    Returns:
        array of matching products in descending order of Levenshtein distance.
    """
    manufacturer_products = pd.read_csv('manufacturer_data.csv')
    manufacturer_products['name_split'] = manufacturer_products.apply(get_not_continuous_words, axis=1) 
    suitable_solution = get_suitable_products(
        get_not_continuous_words_when_entering(dealer_product), 
        manufacturer_products, 
        levenshtein_distance_max
    )
    solution = sorted(
        suitable_solution, 
        key=lambda x: x['levenshtein_distance'], 
        reverse=True
    )
    last_index = length if length < len(solution) else len(solution)
    return solution[0: last_index]


if __name__ == '__main__':
    print(get_solution('Спрей для столешниц и раковин из искусственного камня и гранитаCooky Spray готовый состав / 0,5 л'))
