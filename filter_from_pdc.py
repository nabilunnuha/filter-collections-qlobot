import pandas as pd
import json
import random
import time
from FilterCollections.filter_product import merge_product_variant
from FilterCollections.utils import create_require, filter_duplicate
from FilterCollections.logger import create_logger
from FilterCollections.read_mongo_db_pdc import filter_collection_from_pdc

def main():
    create_require()
    log = create_logger()
    try:
        output_path = './result'
        
        with open('./config/config.json', 'r') as f:
            data = json.load(f)
            
        limit = int(data['limit'])
        acak_row = bool(data['acak_row'])
            
        with open('./config/judul_lewati_keyword.txt', 'r', encoding='utf-8') as f:
            judul_lewati_keyword = [line.strip() for line in f.readlines()]

        with open('./config/judul_delete_keyword.txt', 'r', encoding='utf-8') as f:
            judul_delete_keyword = [line.strip() for line in f.readlines()]

        products, variants = filter_collection_from_pdc(data, judul_lewati_keyword, judul_delete_keyword)
        products = filter_duplicate(products)
        
        result_merge = merge_product_variant(products, variants)
        
        if acak_row:
            random.shuffle(result_merge)
            
        for i in range(0, len(result_merge), limit):
            random_number = random.randint(10000, 99999)
            try:
                produk_to_csv = result_merge[i:i+limit]
                final_produk = pd.DataFrame(produk_to_csv)
                final_produk.to_csv(f"{output_path}/products-{random_number}.csv", index=False, encoding='utf-8')
                log.info(f'products-{random_number}.csv')
            except Exception as e:
                log.error(f'To Csv Error: {e}')
    except Exception as e:
        log.error(e)
        time.sleep(5)

if __name__ == '__main__':
    main()