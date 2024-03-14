# test.py
#
# Data validation tests for fact_museum_hours table
#
# Scott Renegado

import unittest
import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection


class TestFactMuseumHours(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.engine = get_db_engine()
        cls.con = get_db_connection(engine=cls.engine)
        cls.df = pd.read_sql('SELECT * FROM fact_museum_hours', con=cls.con)

    def test_schema(self):
        print("\nschema check")
        columns = self.df.columns.values.tolist()
        self.assertIn('dim_museum_skey', columns)
        self.assertIn('day', columns)
        
    def test_primary_key_not_null(self):
        print('\nnull primary key count = 0')
        null_pks = self.df[['dim_museum_skey', 'day']].isnull()
        null_pks_flattened = null_pks['dim_museum_skey'] | null_pks['day']
        null_pk_counts = self.df[null_pks_flattened].shape[0]
        self.assertEqual(null_pk_counts, 0)
        
    def test_primary_key_unique(self):
        print("\nduplicate primary key count = 0")
        duplicated_pk_counts = self.df[self.df.duplicated(subset=['dim_museum_skey', 'day'])].shape[0]
        self.assertEqual(duplicated_pk_counts, 0)
        
    def test_no_duplicate_records(self):
        print("\nduplicate record count = 0")
        duplicated_record_counts = self.df[self.df.duplicated()].shape[0]
        self.assertEqual(duplicated_record_counts, 0)

    def test_hours_not_missing(self):
        print("\nmissing hours count = 0")
        null_opening_hours_counts = self.df[self.df['opening_hours'].isnull()].shape[0]
        null_closing_hours_counts = self.df[self.df['closing_hours'].isnull()].shape[0]
        self.assertEqual(null_opening_hours_counts, 0)
        self.assertEqual(null_closing_hours_counts, 0)

    def test_no_missing_foreign_keys(self):
        print("\nmissing foreign keys = 0")
        null_dim_museum_skeys = self.df[self.df['dim_museum_skey'].isnull()].shape[0]
        self.assertEqual(null_dim_museum_skeys, 0)
        
    @classmethod
    def tearDownClass(cls):
        if cls.con:
            cls.con.close()

        
if __name__ == '__main__':
    unittest.main()