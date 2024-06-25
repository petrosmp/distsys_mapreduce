import re


class Mapper:
    def __init__(self, id :int):
        """
        Empty list for intermediate keys
        """
        self.intermediate = []
        self.WHITESPACE_RE = re.compile(r'[\w\']+')
        self.id = id
        self.filename = f"mapper_{self.id}"

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

    def save_mapper_data(group_id: int, mapper_output_data: list) -> None:
        """
        Save mapper data to a temporary file
        """
        with open(self.filename, 'w') as file:
            file.write(f"group_id = {group_id}\n")
            file.write(f"mapper_{self.id}_output = ")
            file.write(repr(mapper_output_data))
