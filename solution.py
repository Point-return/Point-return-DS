import pandas as pd
from fuzzywuzzy import fuzz


def get_suitable_products(
        dealer_product: str, 
        manufactur_products: pd.Series,
        levenshtein_distance_max: int,
    ) -> list:
    '''
    A Model Explanation System
    
    return: Array of suitable manufactur products
    '''
    
    suitable_products = []
    for product in manufactur_products['name']:
        l_d = fuzz.token_sort_ratio(dealer_product, product)
        if (l_d >= levenshtein_distance_max):
            manufactur_product_id = manufactur_products[
                manufactur_products['name'] == product
            ]['id'].to_string(index=False)
            suitable_products.append({
                'id':  manufactur_product_id, 
                'product_name': product, 
                'levenshtein_distance': l_d 
            })
    return suitable_products


def get_solution(
        dealer_product: str,
        length: int = 10,
        levenshtein_distance_max: int = 50,
    ) -> list:

    manufactur_products = pd.read_csv('manufacturer_data.csv') 
    
    suitable_solution = get_suitable_products(
        dealer_product, 
        manufactur_products, 
        levenshtein_distance_max
    )
    solution = sorted(suitable_solution, key=lambda x: x['levenshtein_distance'], reverse=True)
    last_index = length - 1 if length < len(solution) else len(solution) - 1
    
    return solution[0: last_index]


if __name__ == '__main__':
    print(get_solution('Средство для удаления ленты  клейкой '))
