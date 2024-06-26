class Reducer:
    def __init__(self, key: str):
        # The word this reducer will handle
        self.key = key


    def reduce(self, combined_data_list: list) -> dict:
        """
        Reduces the combined data to get the final word counts.

        Returns:
        dict: A dictionary with the final word counts.
        """
        for combined_data in combined_data_list:
            for key, value in combined_data.items():
                self.reduced[key] += value
        return dict(self.reduced)

    def filter_relevant_files(self, bools: str) -> None:
        """
        Filter files based on the alphanumeric appearances in bools
        """
        for word, count in combined_data.items():
            index = ord(word[0].lower()) - ord('a')
            if index < 0 or index >= 36:  # Ignore characters outside 'a-z' and '0-9'
                continue
            if index >= 26:  # Adjust index for digits
                index -= (ord('a') - ord('0') - 26)
            if bools[index] == '1':
                if word in self.combined_data:
                    self.combined_data[word] += count
                else:
                    self.combined_data[word] = count

