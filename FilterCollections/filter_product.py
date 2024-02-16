import csv
import os
import random
from tqdm import tqdm

def get_product_all(data: dict, judul_lewati_keyword: list[str], judul_delete_keyword: list[str], file_path: str = './file_csv') -> tuple[list, list]:
    log = create_logger()
    min_harga = int(data['min_harga'])
    max_harga = int(data['max_harga'])
    min_sold = int(data['min_sold'])
    max_sold = int(data['max_sold'])
    min_rating = float(data['min_rating'])
    if min_rating > 5:
        min_rating = float(5)
    min_stock = int(data['min_stock'])
    random_berat = bool(data['random_berat'])
    min_rand = int(data['min_rand'])
    max_rand = int(data['max_rand'])
    try:
        df_mrg = []
        var_mrg = []
        dir_list = os.listdir(file_path)
        for i in range(len(dir_list)):
            produk = dir_list[i]
            if 'variant' in produk:
                with open(f'{file_path}/{produk}','r',encoding='utf-8') as f:
                    csv_reader = csv.DictReader(f, delimiter=',')
                    for row in tqdm(csv_reader, desc=produk, ncols=100):
                        url = row['url']
                        v_stock = int(row['v_stock'])
                        v_price = int(row['v_price'])
                        v_image = row['v_image']
                        v1_name = row['v1_name']
                        v1_value = row['v1_value']
                        v2_name = row['v2_name']
                        v2_value = row['v2_value']
                        var_data = {
                            'url': url,
                            'v_stock': v_stock,
                            'v_price': v_price,
                            'v_image': v_image,
                            'v1_name': v1_name,
                            'v1_value': v1_value,
                            'v2_name': v2_name,
                            'v2_value': v2_value,
                        }
                        var_mrg.append(var_data)
            else:
                with open(f'{file_path}/{produk}', 'r', encoding='utf-8') as f:
                    csv_reader = csv.DictReader(f, delimiter=',')
                    for row in tqdm(csv_reader, desc=produk, ncols=100):
                        url = row['url']
                        name = row['name']
                        price = int(row['price'])
                        thumbnail_1 = row['thumbnail_1']
                        thumbnail_2 = row['thumbnail_2']
                        thumbnail_3 = row['thumbnail_3']
                        thumbnail_4 = row['thumbnail_4']
                        thumbnail_5 = row['thumbnail_5']
                        thumbnail_6 = row['thumbnail_6']
                        thumbnail_7 = row['thumbnail_7']
                        thumbnail_8 = row['thumbnail_8']
                        thumbnail_9 = row['thumbnail_9']
                        thumbnail_10 = row['thumbnail_10']
                        video = row['video']
                        description = row['description']
                        description_html = row['description_html']
                        weight = int(row['weight'])
                        if random_berat:
                            if int(weight) < 10:
                                weight = random.randint(min_rand, max_rand)
                                row['weight'] = weight
                        condition = row['condition']
                        min_order = int(row['min_order'])
                        category_1 = row['category_1']
                        category_2 = row['category_2']
                        category_3 = row['category_3']
                        category_4 = row['category_4']
                        category_5 = row['category_5']

                        sold = int(row['sold'])
                        views = int(row['views'])
                        rating = float(row['rating'])
                        rating_by = int(row['rating_by'])
                        stock = int(row['stock'])
                        size_image = row['size_image']
                        if int(price) <= min_harga or int(price) >= max_harga:
                            continue
                        if int(sold) <= int(min_sold) or int(sold) >= int(max_sold):
                            continue
                        if float(rating) <= min_rating:
                            continue
                        if int(stock) <= min_stock:
                            continue

                        if any(word.lower().strip() in name.lower() for word in judul_lewati_keyword):
                            continue

                        description = description.strip()
                        row['description'] = description
                        name = ' '.join([n for n in name.split(' ') if all(judul_key.lower() not in n.lower() for judul_key in judul_delete_keyword) and n])
                        row['name'] = name
                        df_mrg.append(row)
                        
        return df_mrg, var_mrg
    
    except Exception as e:
        log.error(e)
        return [], []
   
def merge_product_variant(products: list[dict], variants: list[dict]) -> list[dict]:
    result_merge = []
    for product in tqdm(products, desc='Combining Variations', ncols=100):
        url = product['url']
        if 'v_name1' not in product:
            data_variant = [var for var in variants if var['url'] == url]
            product['v_name1'] = data_variant[0]['v1_name'] if len(data_variant) >= 1 else ''
            product['v_name2'] = data_variant[0]['v2_name'] if len(data_variant) >= 1 else ''
            for i in range(1, 101):
                index = i - 1
                product[f'v{i}_value1'] = data_variant[index]['v1_value'] if len(data_variant) >= i else ''
                product[f'v{i}_value2'] = data_variant[index]['v2_value'] if len(data_variant) >= i else ''
                product[f'v{i}_price'] = data_variant[index]['v_price'] if len(data_variant) >= i else ''
                product[f'v{i}_stock'] = data_variant[index]['v_stock'] if len(data_variant) >= i else ''
                product[f'v{i}_image'] = data_variant[index]['v_image'] if len(data_variant) >= i else ''
        result_merge.append(product)
    return result_merge
        
from .logger import create_logger