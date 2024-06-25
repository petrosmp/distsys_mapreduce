from collections import defaultdict
class Combiner:
    def __init__(self):
        self.combined = defaultdict(int)

    def combine(self, mapped_data: dict) -> dict:
        """
        Combines the mapped data to reduce the amount of data transfer to the reducer.

        Returns:
        dict: A dictionary with combined counts of words.
        """
        for key, value in mapped_data:
            self.combined[key] += value
        return dict(self.combined)
