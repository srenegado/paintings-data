# test.py
#
# Data validation tests for fact_artwork table
#
# Scott Renegado

import unittest
import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection


class TestFactArtwork(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Validating fact_artwork table...")
        cls.engine = get_db_engine()
        cls.con = get_db_connection(engine=cls.engine)
        cls.df = pd.read_sql('SELECT * FROM fact_artwork', con=cls.con)

    def test_schema(self):
        print("\nschema check")
        columns = self.df.columns.values.tolist()
        self.assertIn('dim_concept_skey', columns)
        self.assertIn('dim_canvas_skey', columns)
        
    def test_primary_key_not_null(self):
        print('\nnull primary key count = 0')
        null_pks = self.df[['dim_concept_skey', 'dim_canvas_skey']].isnull()
        null_pks_flattened = null_pks['dim_concept_skey'] | null_pks['dim_canvas_skey']
        null_pk_counts = self.df[null_pks_flattened].shape[0]
        self.assertEqual(null_pk_counts, 0)
        
    def test_primary_key_unique(self):
        print("\nduplicate primary key count = 0")
        duplicated_pk_counts = self.df[self.df.duplicated(subset=['dim_concept_skey', 'dim_canvas_skey'])].shape[0]
        self.assertEqual(duplicated_pk_counts, 0)
        
    def test_no_duplicate_records(self):
        print("\nduplicate record count = 0")
        duplicated_record_counts = self.df[self.df.duplicated()].shape[0]
        self.assertEqual(duplicated_record_counts, 0)

    def test_no_missing_foreign_keys(self):
        print("\nmissing foreign keys = 0")
        null_dim_artist_skeys = self.df[self.df['dim_artist_skey'].isnull()].shape[0]
        null_dim_museum_skeys = self.df[self.df['dim_museum_skey'].isnull()].shape[0]
        self.assertEqual(null_dim_artist_skeys, 0)
        self.assertEqual(null_dim_museum_skeys, 0)

    def test_dim_artist_skey_logic(self):
        print("\ncheck join logic (dim_artist_skey)")
        expected = pd.read_sql(
            """
            SELECT dim_artist_skey
            FROM dim_concept
            LEFT JOIN product ON product.work_id = dim_concept.work_id -- necessary LEFT JOIN
            LEFT JOIN dim_canvas ON product.canvas_id = dim_canvas.canvas_id -- necessary LEFT JOIN
            LEFT JOIN work on dim_concept.work_id = work.id
            LEFT JOIN dim_artist on work.artist_id = dim_artist.artist_id
            ORDER BY dim_concept_skey, dim_canvas_skey
        """, con=self.con)
        actual = pd.DataFrame(self.df['dim_artist_skey'])
        self.assertTrue(actual.equals(expected))

    def test_dim_museum_skey_logic(self):
        print("\ncheck join logic (dim_museum_skey)")
        expected = pd.read_sql(
            """
            SELECT dim_museum_skey
            FROM dim_concept
            LEFT JOIN product ON product.work_id = dim_concept.work_id -- necessary LEFT JOIN
            LEFT JOIN dim_canvas ON product.canvas_id = dim_canvas.canvas_id -- necessary LEFT JOIN
            LEFT JOIN work on dim_concept.work_id = work.id
            LEFT JOIN dim_museum on work.museum_id = dim_museum.museum_id
            ORDER BY dim_concept_skey, dim_canvas_skey
        """, con=self.con)
        actual = pd.DataFrame(self.df['dim_museum_skey'])
        self.assertTrue(actual.equals(expected))

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
        print("\n")
        if cls.con:
            cls.con.close()

        
if __name__ == '__main__':
    unittest.main()