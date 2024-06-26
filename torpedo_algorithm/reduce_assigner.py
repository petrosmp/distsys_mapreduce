import importlib.util
class ReduceTaskAssigner:
    def __init__(self, key: str):
        # The word this reducer will handle
        self.key = key
        self.NUMBER_OF_LETTERS = 26
        self.NUMBER_OF_DIGITS = 10
        self.FIRST_CHARACTER = 'a'

    def filter_relevant_files(self, bools: str) -> None:
        """
        Filter files based on the alphanumeric appearances in bools
        """
        #for word, count in combined_data.items():
        # Change to i
        files = list_map_files(self.directory)
        for filename in files:
            module_name = filename[:-3] # removers file extension
            file_path = os.path.join(self.directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            bools_variable = f"{module_name}_bools"
            output_variable = f"{module_name}_output"
            if hasattr(module, bools_variable) and hasattr(module, output_variable):
                bools = getattr(module, bools_variable)
                combined_data = getattr(module, output_variable)
                self.filter_and_combine(combined_data, bools)


            index = getIndexFromLetter(word[0])
            if index < 0 or index > 36:  # Ignore characters outside 'a-z' and '0-9'
                continue
            if getBoolFromInbdex(self, index):
                # this is the reduce task
                if word in self.combined_data:
                    self.reduce_data[word] += count
                else:
                    self.reduce_data[word] = count

    def getIndexFromLetter(self, char: str) -> int:
        # Transform to lowercase
        #return ord(word[0].lower()) - ord('a')
        if char.isalpha():
            index = ord(char.lower()) - ord(FIRST_CHARACTER)
        elif char.isdigit():
            index = NUMBER_OF_LETTERS + int(char)
        else:
            index = -1
        return index

    def getBoolFromInbdex(self, index: int) -> bool:
        if index == -1:
            return False
        if bools[index] == '1':
            return True
        if bools[index] == '0':
            return False
