import sys
import os
from itertools import islice


class CSVCombiner:
    def __init__(self, args):
        """Initialize a CSV combiner"""
        self.__urls = args
        self.__basenames = []


    def validate_args(self):
        """Validate the number of arguments"""
        if len(self.__urls) <= 1:
            sys.exit("Please specify at least two files.")


    def validate_files(self):
        """Validate files"""
        for url in self.__urls:
            if not os.path.exists(url):
                sys.exit("File does not exist: " + url)
            if os.path.getsize(url) == 0:
                sys.exit("File is empty: " + url)


    def validate_columns(self):
        """Validate whether all files have the same column names"""
        column_names = ""
        for i, url in enumerate(self.__urls):
            first_line = ""
            with open(url, 'r') as f:
                first_line = f.readline().strip('\n')
            if (i == 0):
                column_names = first_line
            else:
                if first_line != column_names:
                    sys.exit("Files have different column names")


    def get_basename(self):
            """Get basenames of all files"""
            for url in self.__urls:
                self.__basenames.append(os.path.basename(url))


    def combine_csv(self):
        """Combine all files"""
        self.validate_args()
        self.validate_files()
        self.validate_columns()
        self.get_basename()

        batch_size = 10

        for i, url in enumerate(self.__urls):
            if i == 0:
                with open(url, 'r') as f:
                    first_line = f.readline().strip('\n') + ',\"filename\"'
                    print(first_line)
                    while True:
                        line_batch = list(islice(f, batch_size))
                        if not line_batch:
                            break
                        batch_result = ""
                        for line in line_batch:
                            batch_result += line.strip('\n') + ',\"' + self.__basenames[i] + '\"\n'
                        sys.stdout.write(batch_result)
            else:
                with open(url, 'r') as f:
                    next(f)
                    while True:
                        line_batch = list(islice(f, batch_size))
                        if not line_batch:
                            break
                        batch_result = ""
                        for line in line_batch:
                            batch_result += line.strip('\n') + ',\"' + self.__basenames[i] + '\"\n'
                        sys.stdout.write(batch_result)


def main():
    combiner = CSVCombiner(sys.argv[1:])
    combiner.combine_csv()


if __name__ == '__main__':
    main()
