# test.py
#
# Data validation tests for work table
#
# Scott Renegado

import unittest
import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection


class TestWork(unittest.TestCase):
    
    def setUp(self):
        self.engine = get_db_engine()
        self.con = get_db_connection(engine=self.engine)
        self.df = pd.read_sql('SELECT * FROM work', con=self.con)

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

    def test_artist_id_references_artist(self):
        print("\nvalues in artist_id exist in artist (id)")
        artist_ids = pd.read_sql('SELECT id from artist',con=self.con)
        invalid_artist_id_counts = self.df[~self.df['artist_id'].isin(artist_ids['id'])].shape[0]
        self.assertEqual(invalid_artist_id_counts, 0)

    def test_museum_id_references_museum(self):
        print("\nvalues in museum_id exist in museum (id)")
        museum_ids = pd.read_sql('SELECT id from museum',con=self.con)
        invalid_museum_id_counts = self.df[~self.df['museum_id'].isin(museum_ids['id'])].shape[0]
        self.assertEqual(invalid_museum_id_counts, 0)
        
    def tearDown(self):
        if self.con:
            self.con.close()

        
if __name__ == '__main__':
    unittest.main()