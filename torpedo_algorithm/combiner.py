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
