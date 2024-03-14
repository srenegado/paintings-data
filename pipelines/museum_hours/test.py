# test.py
#
# Data validation tests for museum_hours table
#
# Scott Renegado

import unittest
import pandas as pd
from datetime import datetime

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection


class TestMuseumHours(unittest.TestCase):
    
    def setUp(self):
        self.engine = get_db_engine()
        self.con = get_db_connection(engine=self.engine)
        self.df = pd.read_sql('SELECT * FROM museum_hours', con=self.con)

    def test_schema(self):
        print("\nschema check")
        columns = self.df.columns.values.tolist()
        self.assertIn('museum_id', columns)
        self.assertIn('day', columns)
        
    def test_primary_key_not_null(self):
        print('\nnull primary key count = 0')
        null_pks = self.df[['museum_id', 'day']].isnull()
        null_pks_flattened = null_pks['museum_id'] | null_pks['day']
        null_pk_counts = self.df[null_pks_flattened].shape[0]
        self.assertEqual(null_pk_counts, 0)
        
    def test_primary_key_unique(self):
        print("\nduplicate primary key count = 0")
        duplicated_pk_counts = self.df[self.df.duplicated(subset=['museum_id', 'day'])].shape[0]
        self.assertEqual(duplicated_pk_counts, 0)
        
    def test_no_duplicate_records(self):
        print("\nduplicate record count = 0")
        duplicated_record_counts = self.df[self.df.duplicated()].shape[0]
        self.assertEqual(duplicated_record_counts, 0)

    def test_hours_not_missing(self):
        print("\nmissing hours count = 0")
        null_opening_hours_counts = self.df[self.df['open'].isnull()].shape[0]
        null_closing_hours_counts = self.df[self.df['close'].isnull()].shape[0]
        self.assertEqual(null_opening_hours_counts, 0)
        self.assertEqual(null_closing_hours_counts, 0)

    def test_hours_in_range(self):
        print("\nhours are in correct format")
        opening_hours = self.df['open']
        closing_hours = self.df['close']
        min_time = datetime.strptime('00:00:00', '%H:%M:%S').time()
        max_time = datetime.strptime('23:59:59', '%H:%M:%S').time()
        self.assertTrue(opening_hours.between(min_time, max_time).all())
        self.assertTrue(closing_hours.between(min_time, max_time).all())

    def tearDown(self):
        if self.con:
            self.con.close()

        
if __name__ == '__main__':
    unittest.main()