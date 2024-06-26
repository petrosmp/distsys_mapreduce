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
        self.intermediate = []
        self.id = id
        # Keep track of the appearance of the possible alphanumeric characters as first characters
        self.first_alphanumeric_appearance = [False] * (self.NUMBER_OF_LETTERS + self.NUMBER_OF_DIGITS)

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
