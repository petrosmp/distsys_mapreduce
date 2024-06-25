import re


class Mapper:
    def __init__(self):
        """
        Empty list for intermediate keys
        """
        self.intermediate = []
        self.WHITESPACE_RE = re.compile(r'[\w\']+')

    def map(self, chunk: str, case_sensitive: bool = True) -> list:
        """
        Processes each chunk and emits key-value pairs.

        Returns:
        list: A list of key-value pairs.
        """
        words = self.WHITESPACE_RE.findall(chunk)
        if case_sensitive:
            for word in words:
                self.intermediate.append((word, 1))
        else:
            for word in words:
                self.intermediate.append((word.lower(), 1))
        return self.intermediate
