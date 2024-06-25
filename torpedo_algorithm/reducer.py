from collections import defaultdict


class Reducer:
    def __init__(self):
        self.reduced = defaultdict(int)

    def reduce(self, combined_data_list: list) -> dict:
        """
        Reduces the combined data to get the final word counts.

        Args:
        combined_data_list (list): A list of dictionaries with combined word counts.

        Returns:
        dict: A dictionary with the final word counts.
        """
        for combined_data in combined_data_list:
            for key, value in combined_data.items():
                self.reduced[key] += value
        return dict(self.reduced)