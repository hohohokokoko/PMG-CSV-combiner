"""This module is used to test CSVCombiner using unittest"""
import unittest
from io import StringIO
from unittest.mock import patch
from csv_combiner import CSVCombiner


class TestCSVCombiner(unittest.TestCase):
    """This class inherits unittest.TestCase and is used to test CSVCombiner"""
    def test_no_file(self):
        """Test CSVCombiner.validate_args() when there is no file given"""
        args = []

        combiner = CSVCombiner(args)
        with self.assertRaises(SystemExit) as cm:
            combiner.validate_args()

        self.assertEqual(cm.exception.code, "Please specify at least two files.")


    def test_one_file(self):
        """Test CSVCombiner.validate_args() when there is only one file given"""
        args = ["./fixtures/clothing.csv"]

        combiner = CSVCombiner(args)
        with self.assertRaises(SystemExit) as cm:
            combiner.validate_args()

        self.assertEqual(cm.exception.code, "Please specify at least two files.")


    def test_file_not_exist(self):
        """Test CSVCombiner.validate_files() when the file does not exist"""
        args = ["./fixtures/clothing.csv", "./fixtures/fake.csv"]

        combiner = CSVCombiner(args)
        with self.assertRaises(SystemExit) as cm:
            combiner.validate_files()

        self.assertEqual(cm.exception.code, "File does not exist: " + args[1])


    def test_file_empty(self):
        """Test CSVCombiner.validate_files() when the file is empty"""
        args = ["./fixtures/clothing.csv", "./customized_fixtures/empty.csv"]

        combiner = CSVCombiner(args)
        with self.assertRaises(SystemExit) as cm:
            combiner.validate_files()

        self.assertEqual(cm.exception.code, "File is empty: " + args[1])


    def test_different_columns(self):
        """Test CSVCombiner.validate_columns() when columns are different"""
        args = ["./fixtures/clothing.csv", "./customized_fixtures/accessories_change.csv"]

        combiner = CSVCombiner(args)
        with self.assertRaises(SystemExit) as cm:
            combiner.validate_columns()

        self.assertEqual(cm.exception.code, "Files have different column headers")


    def test_get_basename(self):
        """Test CSVCombiner.get_basename()"""
        args = ["./fixtures/clothing.csv", "./fixtures/accessories.csv"]
        target_basename = ["clothing.csv", "accessories.csv"]

        combiner = CSVCombiner(args)
        combiner.get_basename()

        self.assertEqual(combiner.basenames, target_basename)


    def test_two_files(self):
        """Test CSVCombiner.combine_csv() when combinig two files"""
        args = ["./fixtures/accessories.csv", "./fixtures/clothing.csv"]
        f = open("./target_fixtures/combined_acc_clothing.csv", 'r')
        target = f.read()
        f.close()

        combiner = CSVCombiner(args)
        with patch('sys.stdout', new=StringIO()) as output:
            combiner.combine_csv()
            self.assertEqual(output.getvalue(), target)


    def test_three_files(self):
        """Test CSVCombiner.combine_csv() when combinig three files"""
        args = ["./fixtures/accessories.csv", "./fixtures/clothing.csv", "./fixtures/household_cleaners.csv"]
        f = open("./target_fixtures/combined_acc_clothing_cleaner.csv", 'r')
        target = f.read()
        f.close()

        combiner = CSVCombiner(args)
        with patch('sys.stdout', new=StringIO()) as output:
            combiner.combine_csv()
            self.assertEqual(output.getvalue(), target)
