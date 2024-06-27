from collections import defaultdict
import sys
import re

alphanumeric_re: str = r'[^a-zA-Z0-9\s]'

class Splitter:
    def __init__(self, input_string: str, num_splits: int):
        self.input_string = re.sub(alphanumeric_re, '', input_string)
        self.num_splits = num_splits


    def split(self) -> dict:
        """
        Splits the input string into chunks with a specified number of words per chunk.

        Returns:
        dict: A dictionary where the keys are chunk indices and the values are the chunks of text.
        """
        words = self.input_string.split()
        total_words = len(words)
        words_per_split = total_words // self.num_splits
        splits = {}

        for i in range(self.num_splits):
            # Get index by index * words_per_split
            start_index = i * words_per_split
            # For the last split, include all remaining words
            if i == self.num_splits - 1:
                end_index = total_words
            else:
                end_index = start_index + words_per_split
            chunk = " ".join(words[start_index:end_index])
            splits[i + 1] = chunk
        return splits

    def write_files(self, splits: dict):
        for i, split in splits.items():
            with open(f"split_out/split{i}.txt", 'w') as file:
                file.write(split)

if __name__ == "__main__":
    # the text to split
    text = ""
    with open(sys.argv[1], 'r') as file:
        text = file.read()

    # Get number of splits as argument
    num_of_splits = int(sys.argv[2])

    splitter = Splitter(text, num_of_splits)
    splits = splitter.split()
    # print(splits)
