# test.py
#
# Data validation tests for product table
#
# Scott Renegado

import unittest
import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection


class TestProduct(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.engine = get_db_engine()
        cls.con = get_db_connection(engine=cls.engine)
        cls.df = pd.read_sql('SELECT * FROM product', con=cls.con)

    def test_schema(self):
        print("\nschema check")
        columns = self.df.columns.values.tolist()
        self.assertIn('work_id', columns)
        self.assertIn('canvas_id', columns)
        
    def test_primary_key_not_null(self):
        print('\nnull primary key count = 0')
        null_pks = self.df[['work_id', 'canvas_id']].isnull()
        null_pks_flattened = null_pks['work_id'] | null_pks['canvas_id']
        null_pk_counts = self.df[null_pks_flattened].shape[0]
        self.assertEqual(null_pk_counts, 0)
        
    def test_primary_key_unique(self):
        print("\nduplicate primary key count = 0")
        duplicated_pk_counts = self.df[self.df.duplicated(subset=['work_id', 'canvas_id'])].shape[0]
        self.assertEqual(duplicated_pk_counts, 0)
        
    def test_no_duplicate_records(self):
        print("\nduplicate record count = 0")
        duplicated_record_counts = self.df[self.df.duplicated()].shape[0]
        self.assertEqual(duplicated_record_counts, 0)

    def test_sale_price_not_missing(self):
        print("\nmissing sale price count = 0")
        null_sale_price_counts = self.df[self.df['sale_price'].isnull()].shape[0]
        self.assertEqual(null_sale_price_counts, 0)

    def test_regular_price_not_missing(self):
        print("\nmissing regular price count = 0")
        null_regular_price_counts = self.df[self.df['regular_price'].isnull()].shape[0]
        self.assertEqual(null_regular_price_counts, 0)

    def test_nonzero_sale_price(self):
        print("\nmin(sale_price) > 0")
        min_sale_price = min(self.df['sale_price'])
        self.assertGreater(min_sale_price, 0)

    def test_nonzero_regular_price(self):
        print("\nmin(regular_price) > 0")
        min_regular_price = min(self.df['regular_price'])
        self.assertGreater(min_regular_price, 0)

    @classmethod
    def tearDownClass(cls):
        if cls.con:
            cls.con.close()

        
if __name__ == '__main__':
    unittest.main()