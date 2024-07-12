import re

#  User gives string and a dictionary is returned
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
        self.combiner = None

    # Literally us
    def keep_appearances(self, char: str):
        # Handles both lower and upper case
        if char.isalpha():
            index = ord(char.lower()) - ord(self.FIRST_CHARACTER)
        elif char.isdigit():
            index = self.NUMBER_OF_LETTERS + int(char)
        else:
            return
        self.first_alphanumeric_appearance[index] = True

    def map(self, chunk: str) -> dict:
        """
        Processes each chunk and emits key-value pairs.
        Returns:
        list: A list of key-value pairs.
        """
        words = self.WHITESPACE_RE.findall(chunk)
        for word in words:
            self.keep_appearances(word[0])
            self.intermediate.append((word.lower(), 1))
        # Create a string from the bool array of appearances
        appearances_str: str = ''.join(['1' if flag else '0' for flag in self.first_alphanumeric_appearance])
        self.combiner = Combiner(self.id, self.intermediate, appearances_str)
        return self.combiner.combine()

    def save_combiner_data(self) -> None:
        """
        Save combiner data to a temporary file in permanent storage
        """
        with open(self.combiner.filename, 'w') as file:
            # The first character appearance heatmap is stored for the 36 possible alphanumeric characters
            file.write(self.combiner.alphanumeric_appearances)
            file.write("\n")
            file.write(repr(self.combiner.combined))


class Combiner:
    def __init__(self, id: int, mapped_data: list[dict], alphanumeric_appearances: str):
        self.id = id
        self.mapped_data = mapped_data
        self.alphanumeric_appearances = alphanumeric_appearances
        self.filename = f"/mnt/longhorn/job_{job_id}/mapper_out/mapper_{self.id}.txt"
        # self.filename = f"testfile{self.id}.txt"
        self.combined = {}

    def combine(self) -> dict:
        """
        TODO test values Simplifies the Reducer's task by combining the results of the specific Map worker
        """
        for key, value in self.mapped_data:
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
            file.write(self.alphanumeric_appearances)
            file.write("\n")
            file.write(repr(self.combined))
