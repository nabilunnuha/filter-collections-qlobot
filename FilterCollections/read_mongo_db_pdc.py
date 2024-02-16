from pymongo import MongoClient
from tqdm import tqdm
import math

def get_pdc_collection(namespace_collection: str) -> list[dict]:
    log = create_logger()
    try:
        client = MongoClient('localhost', 27017)
        db_name = 'kampretcode2'
        db = client[db_name]
        cursor = db['item'].find()

        data: list[dict] = [document for document in cursor]
        filter_data = [prdct for prdct in data if str(prdct['marketplace']) == 'shopee' and str(prdct['namespace']).strip() == namespace_collection.strip()]
        return filter_data
    except Exception as e:
        log.error(e)
        return []
    
def filter_collection_from_pdc(data: dict, judul_lewati_keyword: list[str], judul_delete_keyword: list[str]) -> tuple[list,list]:
    log = create_logger()
    try:
        name_space = str(input('namespace collection: '))
        data_product = get_pdc_collection(name_space)
        min_harga = int(data['min_harga'])
        max_harga = int(data['max_harga'])
        min_sold = int(data['min_sold'])
        max_sold = int(data['max_sold'])
        min_rating = float(data['min_rating'])
        if min_rating > 5:
            min_rating = float(5)
        min_stock = int(data['min_stock'])

        data_produk = []
        data_produk_variant = []
        for data in tqdm(data_product, desc="Filtering", ncols=100):
            try:
                link_img = "https://cf.shopee.co.id/file/"
                to_items = data
                images = data
                productitem = to_items['public_source']['productitem']
                url = data['url']
                name: str = to_items['name']
                price = to_items['price']
                thumbnail_1 = to_items['image']
                thumbnail_2 = images['images'][1] if len(images['images']) >= 2 else ""
                thumbnail_3 = images['images'][2] if len(images['images']) >= 3 else ""
                thumbnail_4 = images['images'][3] if len(images['images']) >= 4 else ""
                thumbnail_5 = images['images'][4] if len(images['images']) >= 5 else ""
                thumbnail_6 = images['images'][5] if len(images['images']) >= 6 else ""
                thumbnail_7 = images['images'][6] if len(images['images']) >= 7 else ""
                thumbnail_8 = images['images'][7] if len(images['images']) >= 8 else ""
                thumbnail_9 = images['images'][8] if len(images['images']) >= 9 else ""
                thumbnail_10 = images['images'][9] if len(images['images']) >= 10 else ""
                video = ''
                description: str = to_items['desc']
                description_html = ''
                weight = 0
                if 'condition' in productitem:
                    condition = 'Baru' if productitem['condition'] == 1 else 'Bekas'
                else:
                    condition = 'Baru'
                min_order = 1
                category_1 = productitem['categories'][0]['displayname'] if len(productitem['categories']) >= 1 else ""
                category_2 = productitem['categories'][1]['displayname'] if len(productitem['categories']) >= 2 else ""
                category_3 = productitem['categories'][2]['displayname'] if len(productitem['categories']) >= 3 else ""
                category_4 = productitem['categories'][3]['displayname'] if len(productitem['categories']) >= 4 else ""
                category_5 = productitem['categories'][4]['displayname'] if len(productitem['categories']) >= 5 else ""
                sold = to_items['sold']
                views = 0
                rating = productitem['itemrating']['ratingstar']
                if productitem['itemrating']['ratingcount']:
                    rating_by = sum(productitem['itemrating']['ratingcount'])
                else:
                    rating_by = 0
                stock = to_items['stock']
                size_image = ''
                if int(price) < min_harga or int(price) > max_harga:
                    # log.info(f'{price = }')
                    continue
                if int(sold) < int(min_sold) or int(sold) >=int(max_sold):
                    # log.info(f'{price = }')
                    continue
                if float(rating) < min_rating:
                    # log.info(f'{rating = }')
                    continue
                if int(stock) < min_stock:
                    # log.info(f'{stock = }')
                    continue

                if any(word.lower().strip() in name.lower() for word in judul_lewati_keyword):
                    # log.info(f'{name = }')
                    continue

                description = description.strip()
                name = ' '.join([n for n in name.split(' ') if all(judul_key.lower() not in n.lower() for judul_key in judul_delete_keyword) and n])

                new_data = {'url': url,
                            'name': name,
                            'price': price,
                            'thumbnail_1': fix_url(thumbnail_1),
                            'thumbnail_2': fix_url(thumbnail_2),
                            'thumbnail_3': fix_url(thumbnail_3),
                            'thumbnail_4': fix_url(thumbnail_4),
                            'thumbnail_5': fix_url(thumbnail_5),
                            'thumbnail_6': fix_url(thumbnail_6),
                            'thumbnail_7': fix_url(thumbnail_7),
                            'thumbnail_8': fix_url(thumbnail_8),
                            'thumbnail_9': fix_url(thumbnail_9),
                            'thumbnail_10': fix_url(thumbnail_10),
                            'video': video,
                            'description': description,
                            'description_html': description_html,
                            'weight': weight,
                            'condition': condition,
                            'min_order': min_order,
                            'category_1': category_1,
                            'category_2': category_2,
                            'category_3': category_3,
                            'category_4': category_4,
                            'category_5': category_5,
                            'sold': sold,
                            'views': views,
                            'rating': rating,
                            'rating_by': rating_by,
                            'stock': stock,
                            'size_image': size_image}
                
                data_produk.append(new_data)

                models = productitem['models']
                tier_variations = productitem['tiervariations']
                for model in models:
                    if len(tier_variations) >= 1:
                        v_stock = model['stock']
                        v_price = math.ceil(int(str(model['price'])[:-5]) / 100) * 100
                        tier_index = model['extinfo']['tierindex']
                        v_image = ''
                        v2_name = ''
                        v2_value = ''
                        if len(tier_variations) >= 2:
                            v1_name = tier_variations[0]['name']
                            v2_name = tier_variations[1]['name'] if len(tier_variations) >= 2 else ""
                            if tier_variations[0]['images']:
                                v_image = link_img+tier_variations[0]['images'][tier_index[0]]
                            if len(tier_variations[0]['options']) >= 1:
                                v1_value = tier_variations[0]['options'][tier_index[0]]
                            if v2_name and len(tier_variations[1]['options']) >= 1:
                                v2_value = tier_variations[1]['options'][tier_index[1]]
                        elif len(tier_variations) < 2:
                            v1_name = tier_variations[0]['name']
                            if tier_variations[0]['images']:
                                v_image = link_img+tier_variations[0]['images'][tier_index[0]]
                            if len(tier_variations[0]['options']) >= 1:
                                v1_value = tier_variations[0]['options'][tier_index[0]]
                    v_new_data = {
                        'url': url,
                        'v_stock': v_stock,
                        'v_price': v_price,
                        'v_image': v_image,
                        'v1_name': v1_name,
                        'v1_value': v1_value,
                        'v2_name': v2_name,
                        'v2_value': v2_value,
                    }
                    data_produk_variant.append(v_new_data)
            except Exception as e:
                log.error(f'{__name__}: {e}')
        return data_produk, data_produk_variant
    except Exception as e:
        log.error(f'{__name__}: {e}')
        return [], []
    
from .logger import create_logger
from .utils import fix_url