from collections import defaultdict
import sys

class Splitter:
    def __init__(self, input_string: str, words_per_split: int):
        self.input_string = input_string
        self.words_per_split = words_per_split

    def split(self) -> dict:
        """
        Splits the input string into chunks with a specified number of words per chunk.

        Returns:
        dict: A dictionary where the keys are chunk indices and the values are the chunks of text.
        """
        words = self.input_string.split()
        total_words = len(words)
        split_count = 0
        splits = {}
        for i in range(0, total_words, self.words_per_split):
            split_count += 1
            chunk = " ".join(words[i:i + self.words_per_split])
            splits[split_count] = chunk
        self.write_files(splits)
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

    # number of words per chunk
    words_per_split = int(sys.argv[2])

    splitter = Splitter(text, words_per_split)
    splits = splitter.split()
    print(splits)
