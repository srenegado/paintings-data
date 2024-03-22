# test.py
#
# Data validation tests for dim_artist table
#
# Scott Renegado

import unittest
import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection


class TestDimArtist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Validating dim_artist table...")
        cls.engine = get_db_engine()
        cls.con = get_db_connection(engine=cls.engine)
        cls.df = pd.read_sql("SELECT * FROM dim_artist", con=cls.con)

    def test_schema(self):
        print("\nschema check")
        columns = self.df.columns.values.tolist()
        self.assertIn("dim_artist_skey", columns)
        self.assertIn("artist_id", columns)

    def test_primary_key_not_null(self):
        print("\nnull primary key count = 0")
        null_pk_counts = self.df[self.df["dim_artist_skey"].isnull()].shape[0]
        self.assertEqual(null_pk_counts, 0)

    def test_natural_key_not_null(self):
        print("\nnull natural key count = 0")
        null_pk_counts = self.df[self.df["artist_id"].isnull()].shape[0]
        self.assertEqual(null_pk_counts, 0)

    def test_primary_key_unique(self):
        print("\nduplicate primary key count = 0")
        duplicated_pk_counts = self.df[
            self.df.duplicated(subset=["dim_artist_skey"])
        ].shape[0]
        self.assertEqual(duplicated_pk_counts, 0)

    def test_no_duplicate_records(self):
        print("\nduplicate record count = 0")
        duplicated_record_counts = self.df[self.df.duplicated()].shape[0]
        self.assertEqual(duplicated_record_counts, 0)

    def test_names_not_missing(self):
        print("\nmissing names count = 0")
        null_names_counts = self.df[self.df["full_name"].isnull()].shape[0]
        self.assertEqual(null_names_counts, 0)

    @classmethod
    def tearDownClass(cls):
        print("\n")
        if cls.con:
            cls.con.close()


if __name__ == "__main__":
    unittest.main()
