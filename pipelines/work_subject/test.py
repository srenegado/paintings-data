# test.py
#
# Data validation tests for work table
#
# Scott Renegado

import unittest
import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection


class TestWorkSubject(unittest.TestCase):
    
    def setUp(self):
        self.engine = get_db_engine()
        self.con = get_db_connection(engine=self.engine)
        self.df = pd.read_sql('SELECT * FROM work_subject', con=self.con)

    def test_schema(self):
        print("\nschema check")
        columns = self.df.columns.values.tolist()
        self.assertIn('work_id', columns)
        self.assertIn('subject', columns)
        
    def test_primary_key_not_null(self):
        print('\nnull primary key count = 0')
        null_pks = self.df[['work_id', 'subject']].isnull()
        null_pks_flattened = null_pks['work_id'] | null_pks['subject']
        null_pk_counts = self.df[null_pks_flattened].shape[0]
        self.assertEqual(null_pk_counts, 0)
        
    def test_primary_key_unique(self):
        print("\nduplicate primary key count = 0")
        duplicated_pk_counts = self.df[self.df.duplicated(subset=['work_id', 'subject'])].shape[0]
        self.assertEqual(duplicated_pk_counts, 0)
        
    def test_no_duplicate_records(self):
        print("\nduplicate record count = 0")
        duplicated_record_counts = self.df[self.df.duplicated()].shape[0]
        self.assertEqual(duplicated_record_counts, 0)

    def test_work_id_references_work(self):
        print("\nvalues in work_id exist in work (id)")
        work_ids = pd.read_sql('SELECT id from work',con=self.con)
        invalid_work_id_counts = self.df[~self.df['work_id'].isin(work_ids['id'])].shape[0]
        self.assertEqual(invalid_work_id_counts, 0)

    def tearDown(self):
        if self.con:
            self.con.close()

        
if __name__ == '__main__':
    unittest.main()