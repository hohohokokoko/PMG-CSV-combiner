[![CSV combiner](https://github.com/hohohokokoko/PMG-CSV-combiner/actions/workflows/main.yml/badge.svg)](https://github.com/hohohokokoko/PMG-CSV-combiner/actions/workflows/main.yml)

# PMG-CSV-combiner

This project is a command line tool that takes multiple CSV files as arguments, generates a combined CSV file, and outputs the combined CSV file to ```STDOUT```.

The input CSV files should have the same columns, otherwise, an error message will be present. The combined CSV file contains the rows from each of the inputs along with an additional column that has the filename from which the row came (only the file's basename, not the entire path). ```filename``` is used as the header of the additional column. The script allows two or more file URLs as arguments.

## Language

Python 3.10

## Implementation

A ```CSVCombiner``` class is used to do the combination work. A ```main()``` function instantiates a ```CSVCombiner``` object, receives arguments from the command line, and invokes ```CSVCombiner.combine_csv()``` method.

```CSVCombiner``` first validates some special cases. Then it reads each file and does the combination. In fact, we do not need to parse CSV files, we just need to modify and append rows. So ```CSVCombiner``` reads, modifies (adds filename), and writes each row of each file. For efficiency and memory considerations, rows are operated in batches (multiple rows each time).

## Usage

Run the script

```
$ python csv_combiner.py <file_url_1> <file_url_2> [more file urls]
```

e.g.

```
$ python csv_combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv
```

or redirect ```STDOUT``` to a file

```
$ python csv_combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv > combined.csv
```

If files have different columns, the script will exit and prompt

```
Files have different column headers
```

For cases like too few arguments, file not existing, or empty file, the script will also give corresponding prompts.

## Test

Run the unit test script
```
$ python -m unittest test_csv_combiner.py
```
Several special cases are tested.

## CI/CD

GitHub Actions is used as the CI/CD tool. ```.github/workflows/main.yml``` defines the workflow of build. It runs scripts of ```install```, ```lint```, and ```test``` from ```Makefile``` upon each push. So this is the CI part. The CD part could be extended in this workflow for future use.

## Example Output

Given two input files named `clothing.csv` and `accessories.csv`.

|email_hash|category|
|----------|--------|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Shirts|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Pants|
|166ca9b3a59edaf774d107533fba2c70ed309516376ce2693e92c777dd971c4b|Cardigans|

|email_hash|category|
|----------|--------|
|176146e4ae48e70df2e628b45dccfd53405c73f951c003fb8c9c09b3207e7aab|Wallets|
|63d42170fa2d706101ab713de2313ad3f9a05aa0b1c875a56545cfd69f7101fe|Purses|

Your script would output

|email_hash|category|filename|
|----------|--------|--------|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Shirts|clothing.csv|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Pants|clothing.csv|
|166ca9b3a59edaf774d107533fba2c70ed309516376ce2693e92c777dd971c4b|Cardigans|clothing.csv|
|176146e4ae48e70df2e628b45dccfd53405c73f951c003fb8c9c09b3207e7aab|Wallets|accessories.csv|
|63d42170fa2d706101ab713de2313ad3f9a05aa0b1c875a56545cfd69f7101fe|Purses|accessories.csv|