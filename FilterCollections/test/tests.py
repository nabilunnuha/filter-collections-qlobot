import unittest
from ..utils import create_require, filter_duplicate
from ..logger import create_logger
from ..read_mongo_db_pdc import get_pdc_collection

class TestCollectionsModule(unittest.TestCase):
    def test_scraper_instance(self):
        coll = get_pdc_collection('test')
        self.assertIsInstance(coll, list)

    def test_create_logger(self):
        logger = create_logger(__name__)
        logger.debug('this logger level info')
        logger.info('this logger level info')
        logger.warning('this logger level warning')
        logger.error('this logger level error')
        logger.critical('this logger level critical')
        self.assertIsNotNone(logger)
        
    def test_create_require(self):
        req = create_require()
        self.assertIsNone(req)

    def test_filter_duplicate(self):
        [{'url':1},{'url':2},{'url':1},{'url':2},{'url':3},{'url':1}]
        result = filter_duplicate()
        self.assertEqual(len(result), 3)
        
if __name__ == '__main__':
    unittest.main()