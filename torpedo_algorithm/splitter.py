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

    def split_input(input_file, lines_per_split):
        try:
            with open(input_file, 'r') as file:
                lines = file.readlines()
                total_lines = len(lines)
                split_count = 0
                for i in range(0, total_lines, lines_per_split):
                    split_count += 1
                    output_file = f'{input_file}_split_{split_count}.txt'
                    with open(output_file, 'w') as split_file:
                        split_file.writelines(lines[i:i + lines_per_split])
            print(f'Successfully split {input_file} into {split_count} parts.')
        except Exception as e:
            print(f'Error while splitting file: {e}')

    def write_files(self, splits: dict):
        for i, split in enumerate(splits):  # Using enumerate to get index i
            with open(f"/mnt/longhorn/split_out/split{i}.txt", 'w') as file:
                file.write(splits[split])

if __name__ == "__main__":

    #the text to split
    text = ""
    with open(sys.argv[1], 'r') as file:
        text = file.read()

    #num of chucnks to split to
    split_num = int(sys.argv[2])

    # mappers = [Mapper(i) for i in range(len(splits))]
    splitter = Splitter(text, split_num)
    splits = splitter.split()
    print(splits)
 