import re


class Mapper:
    def __init__(self, id :int):
        """
        Initializes the mapper with the given id.
        """
        # RE to keep only alphanumeric characters
        self.WHITESPACE_RE = re.compile(r'[\w\']+')
        self.NUMBER_OF_LETTERS = 26
        self.NUMBER_OF_DIGITS = 10
        self.intermediate = []
        self.id = id
        self.filename = f"mapper_{self.id}.py"
        # Keep track of the appearance of the possible alphanumeric characters as first characters
        self.first_alphanumeric_appearance = [False] * (NUMBER_OF_LETTERS + NUMBER_OF_DIGITS)

    # Literally us
    def keep_appearances(self, char: str):
        # Handles both lower and upper case
        if char.isalpha():
            index = ord(char.lower()) - ord('a')
        elif char.isdigit():
            index = 26 + int(char)
        else:
            return
        self.first_alphanumeric_appearance[index] = True

    def map(self, chunk: str) -> list:
        """
        Processes each chunk and emits key-value pairs.
        Returns:
        list: A list of key-value pairs.
        """
        words = self.WHITESPACE_RE.findall(chunk)
        for word in words:
            self.keep_appearances(word[0])
            self.intermediate.append((word, 1))
        return self.intermediate

    def save_mapper_data(group_id: int) -> None:
        """
        Save mapper data to a temporary file in permanent storage
        """
        with open(self.filename, 'w') as file:
            # The character appearance heatmap is stored for the 36 possible
            file.write(f"{''.join(['1' if flag else '0' for flag in self.first_char_bool_array])}\n")
            file.write(f"group_id = {group_id}\n")
            file.write(f"mapper_{self.id}_output = ")
            file.write(self.intermediate)
