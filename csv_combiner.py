"""
This module is used to combine multiple CSV files run as a command line tool.

Classes:
    CSVCombiner: Validate and combine multiple CSV files given their urls

Functions:
    main: Receive command line arguments, instantiate a CSVCombiner, and run the combine function
"""
import sys
import os
from itertools import islice


class CSVCombiner:
    """Validate and combine multiple CSV files"""
    def __init__(self, args):
        """Initialize a CSVCombiner object with a list of file urls"""
        self.urls = args
        self.basenames = []


    def validate_args(self):
        """Validate the number of files"""
        if len(self.urls) <= 1:
            sys.exit("Please specify at least two files.")


    def validate_files(self):
        """Validate files exist and not empty"""
        # iterate through all urls
        for url in self.urls:
            if not os.path.exists(url):
                sys.exit("File does not exist: " + url)
            if os.path.getsize(url) == 0:
                sys.exit("File is empty: " + url)


    def validate_columns(self):
        """Validate all files have the same column headers"""
        column_headers = ""
        # iterate through all urls and read files
        for i, url in enumerate(self.urls):
            first_line = ""
            with open(url, 'r', encoding='utf-8') as f:
                # only read the first line of each file which is the column headers
                first_line = f.readline().strip('\n')

            if i == 0:
                column_headers = first_line
            else:
                # for subsequent files, column headers should be the same as previous ones
                if first_line != column_headers:
                    sys.exit("Files have different column headers")


    def get_basename(self):
        """Get basenames of all files"""
        # iterate through all urls
        for url in self.urls:
            # store each file's basename
            self.basenames.append(os.path.basename(url))


    def read_write_util(self, batch_size, f, i):
        """
        Read, modify, and write a file in batches of lines

        Parameters:
            batch_size: Number of lines to operate in a batch
            f: File handle of the current file
            i: Index of the current file
        """
        while True:
            # each time, read the file in a batch of lines, for efficiency and memory considerations
            line_batch = list(islice(f, batch_size))
            if not line_batch:
                break

            batch_result = ""
            # iterate through all lines in a batch and form a big string
            for line in line_batch:
                # append basename to each line and append the line to the big string
                batch_result += line.strip('\n') + ',\"' + self.basenames[i] + '\"\n'

            # each time, write the result of the current batch to STDOUT
            # for efficiency and memory considerations
            sys.stdout.write(batch_result)


    def combine_csv(self):
        """Combine all files"""
        self.validate_args()
        self.validate_files()
        self.validate_columns()
        self.get_basename()

        batch_size = 100

        # iterate through all urls and read files
        for i, url in enumerate(self.urls):
            if i == 0:
                with open(url, 'r', encoding='utf-8') as f:
                    # for the first file, keep its first line as the combined file's column headers
                    first_line = f.readline().strip('\n') + ',\"filename\"\n'
                    # write to STDOUT
                    sys.stdout.write(first_line)

                    # read, modify, and write subsequent lines of the file in batches of lines
                    self.read_write_util(batch_size, f, i)
            else:
                with open(url, 'r', encoding='utf-8') as f:
                    # for the subsequent files, skip the first line
                    next(f)

                    # read, modify, and write subsequent lines of the file in batches of lines
                    self.read_write_util(batch_size, f, i)


def main():
    """Receive command line arguments and use CSVCombiner to combine files"""
    combiner = CSVCombiner(sys.argv[1:])
    combiner.combine_csv()


if __name__ == '__main__':
    main()
