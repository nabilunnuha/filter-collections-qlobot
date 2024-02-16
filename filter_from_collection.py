import json
import pandas as pd
import time
import random
from FilterCollections.filter_product import get_product_all, merge_product_variant
from FilterCollections.utils import create_require, filter_duplicate
from FilterCollections.logger import create_logger
    
def main():
    create_require()
    log = create_logger()
    try:
        output_path = './result'
        
        with open(r'config/config.json', 'r+') as f:
            data = json.load(f)

        with open(r'config/judul_lewati_keyword.txt', 'r+', encoding='utf-8') as f:
            judul_lewati_keyword = [line.strip().lower() for line in f.readlines() if len(line) > 2]
            judul_lewati_keyword = list(set(judul_lewati_keyword))

        with open(r'config/judul_delete_keyword.txt', 'r+', encoding='utf-8') as f:
            judul_delete_keyword = [line.strip().lower() for line in f.readlines() if len(line) > 2]
            judul_delete_keyword = list(set(judul_delete_keyword))
        
        limit = int(data['limit'])
        acak_row = bool(data['acak_row'])
        
        products, variants = get_product_all(data,judul_lewati_keyword,judul_delete_keyword)
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
    finally:
        time.sleep(5)
    
if __name__ == '__main__':
    main()