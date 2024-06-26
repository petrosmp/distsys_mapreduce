import re


class Mapper:
    def __init__(self, id: int):
        """
        Initializes the mapper with the given id.
        """
        # RE to keep only alphanumeric characters
        self.WHITESPACE_RE = re.compile(r'[\w\']+')
        self.NUMBER_OF_LETTERS = 26
        self.NUMBER_OF_DIGITS = 10
        self.FIRST_CHARACTER = 'a'
        self.intermediate = []
        self.id = id
        # Keep track of the appearance of the possible alphanumeric characters as first characters
        self.first_alphanumeric_appearance = [False] * (self.NUMBER_OF_LETTERS + self.NUMBER_OF_DIGITS)

    # Literally us
    def keep_appearances(self, char: str):
        # Handles both lower and upper case
        if char.isalpha():
            index = ord(char.lower()) - ord(self.FIRST_CHARACTER)
        elif char.isdigit():
            index = NUMBER_OF_LETTERS + int(char)
        else:
            return
        self.first_alphanumeric_appearance[index] = True

    def map(self, chunk: str) -> (list[dict], str):
        """
        Processes each chunk and emits key-value pairs.
        Returns:
        list: A list of key-value pairs.
        """
        words = self.WHITESPACE_RE.findall(chunk)
        for word in words:
            self.keep_appearances(word[0])
            self.intermediate.append((word, 1))
        # Create a string from the bool array of appearances
        appearances_str: str = ''.join(['1' if flag else '0' for flag in self.first_alphanumeric_appearance])
        return self.intermediate, appearances_str


class Combiner:
    def __init__(self, id: int, mapped_data: list[dict], alphanumeric_appearances: str):
        self.id = id
        self.mapped_data = mapped_data
        self.alphanumeric_appearances = alphanumeric_appearances
        self.filename = f"mapper_{self.id}.py"
        self.combined = {}

    def combine(self, mapped_data: list[dict]) -> dict:
        """
        TODO test values Simplifies the Reducer's task by combining the results of the specific Map worker
        """
        for key, value in mapped_data:
            # print(key, value)
            if key in self.combined:
                self.combined[key] += value
            else:
                self.combined[key] = value
        self.save_combiner_data()
        return self.combined

    def save_combiner_data(self) -> None:
        """
        Save combiner data to a temporary file in permanent storage
        """
        with open(self.filename, 'w') as file:
            # The first character appearance heatmap is stored for the 36 possible alphanumeric characters
            file.write(f"mapcombine_{self.id}_bools = " + "\"" + self.alphanumeric_appearances + "\"")
            file.write(f"\nmapcombine_{self.id}_output = ")
            file.write(repr(self.combined))

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


if __name__ == "__main__":
    text = ("we are avid we fans of PyPy and commensurately thankful for the great work by the PyPy team over "
            "the years. PyPy has enabled us to use Python for a larger part of our toolset than CPython alone "
            "would have supported, and its smooth integration with C/C++ through CFFI has helped us attain a "
            "better tradeoff between performance and programmer productivity in our projects")

    # mappers = [Mapper(i) for i in range(len(splits))]
    splitter = Splitter(text, 10)
    splits = splitter.split()

    # Apply map function to each split
    mappers: list[Mapper] = []
    mapped_data_list: list[dict] = []
    for i in splits:
        mapper = Mapper(i)
        mappers.append(mapper)
        mapped_data = mapper.map(splits[i])
        mapped_data_list.append(mapped_data)

    # combiners = [Combiner(i) for i in range(len(mappers))]
    combiners: list[Combiner] = []
    combined_data_list: list[dict] = []
    for i, mapped_data in enumerate(mapped_data_list):
        (m_data, alphanumeric_appearances) = mapped_data_list[i]
        print(m_data)
        combiner = Combiner(i, m_data, alphanumeric_appearances)
        combiners.append(combiner)
        combined_data = combiner.combine(m_data)
        print(combined_data)
        combined_data_list.append(combined_data)
