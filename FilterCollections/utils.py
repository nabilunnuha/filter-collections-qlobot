import os, json

def filter_duplicate(collection: list[dict]) -> list[dict]:
    unique_data = []
    seen_items = set()
    for d in collection:
        try:
            itemid = d.get('url')
            if itemid not in seen_items:
                unique_data.append(d)
                seen_items.add(itemid)
        except:
            pass
    return unique_data

def create_require() -> None:
    if not os.path.exists('file_csv'):
        os.makedirs('file_csv')
    if not os.path.exists('result'):
        os.makedirs('result')
    if not os.path.exists('config'):
        os.makedirs('config')
    if not os.path.exists('log'):
        os.makedirs('log')
    if not os.path.exists(r'config/config.json'):
        data = {
                    "min_harga":29000,
                    "max_harga":150000,
                    "min_sold":25,
                    "max_sold":999999999,
                    "min_rating":4.2,
                    "min_stock":75,
                    "acak_row":False,
                    "random_berat":False,
                    "min_rand":"300",
                    "max_rand":"900",
                    'limit':7000
                }
        with open(r'config/config.json', 'w') as f:
            json.dump(data, f)
    if not os.path.exists(r'config\judul_delete_keyword.txt'):
        with open(r'config\judul_delete_keyword.txt', 'w') as f:
            f.write('nota\nlive\ngun')
    if not os.path.exists(r'config\judul_lewati_keyword.txt'):
        with open(r'config\judul_lewati_keyword.txt', 'w') as f:
            f.write('nota\nlive\ngun')
            
def fix_url(url: str) -> str:
    result = url
    if url and 'https://cf.shopee.co.id' not in url:
        result = f'https://cf.shopee.co.id/file/{url}'
    return result