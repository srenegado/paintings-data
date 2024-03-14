# test.py
#
# Data validation tests for canvas table
#
# Scott Renegado

import unittest
import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection


class TestCanvas(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.engine = get_db_engine()
        cls.con = get_db_connection(engine=cls.engine)
        cls.df = pd.read_sql('SELECT * FROM canvas', con=cls.con)

    def test_schema(self):
        print("\nschema check")
        columns = self.df.columns.values.tolist()
        self.assertIn('id', columns)
        
    def test_primary_key_not_null(self):
        print('\nnull primary key count = 0')
        null_pk_counts = self.df[self.df['id'].isnull()].shape[0]
        self.assertEqual(null_pk_counts, 0)
        
    def test_primary_key_unique(self):
        print("\nduplicate primary key count = 0")
        duplicated_pk_counts = self.df[self.df.duplicated(subset=['id'])].shape[0]
        self.assertEqual(duplicated_pk_counts, 0)
        
    def test_no_duplicate_records(self):
        print("\nduplicate record count = 0")
        duplicated_record_counts = self.df[self.df.duplicated()].shape[0]
        self.assertEqual(duplicated_record_counts, 0)

    def test_label_not_missing(self):
        print("\nmissing label count = 0")
        null_label_count = self.df[self.df['label'].isnull()].shape[0]
        self.assertEqual(null_label_count, 0)
        
    @classmethod
    def tearDownClass(cls):
        if cls.con:
            cls.con.close()

        
if __name__ == '__main__':
    unittest.main()