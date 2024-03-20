# test.py
#
# Data validation tests for dim_concept table
#
# Scott Renegado

import unittest
import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection


class TestDimConcept(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Validating dim_concept table...")
        cls.engine = get_db_engine()
        cls.con = get_db_connection(engine=cls.engine)
        cls.df = pd.read_sql('SELECT * FROM dim_concept', con=cls.con)

    def test_schema(self):
        print("\nschema check")
        columns = self.df.columns.values.tolist()
        self.assertIn('dim_concept_skey', columns)
        self.assertIn('work_id', columns)
        
    def test_primary_key_not_null(self):
        print('\nnull primary key count = 0')
        null_pk_counts = self.df[self.df['dim_concept_skey'].isnull()].shape[0]
        self.assertEqual(null_pk_counts, 0)

    def test_natural_key_not_null(self):
        print('\nnull natural key count = 0')
        null_pk_counts = self.df[self.df['work_id'].isnull()].shape[0]
        self.assertEqual(null_pk_counts, 0)
        
    def test_primary_key_unique(self):
        print("\nduplicate primary key count = 0")
        duplicated_pk_counts = self.df[self.df.duplicated(subset=['dim_concept_skey'])].shape[0]
        self.assertEqual(duplicated_pk_counts, 0)
        
    def test_no_duplicate_records(self):
        print("\nduplicate record count = 0")
        duplicated_record_counts = self.df[self.df.duplicated()].shape[0]
        self.assertEqual(duplicated_record_counts, 0)

    def test_subject_logic(self):
        print("\ncheck join logic (subject)")
        expected = pd.read_sql(
            """
            SELECT
                CASE WHEN work_subject.subject IS NULL THEN 'Not Provided' 
                    ELSE work_subject.subject 
                END as subject
            FROM work
            LEFT JOIN work_subject ON work.id = work_subject.work_id
            """, con=self.con)
        actual = pd.DataFrame(self.df['subject'])
        self.assertTrue(actual.equals(expected))

    @classmethod
    def tearDownClass(cls):
        print('\n')
        if cls.con:
            cls.con.close()

        
if __name__ == '__main__':
    unittest.main()