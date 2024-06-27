import ast
import json
import os

NUMBER_OF_LETTERS: int = 26
NUMBER_OF_DIGITS: int = 10
FIRST_CHARACTER: str = 'a'


def create_bitmask(group: str) -> str:
    """ Create group bitmask, that has 1 in the position of each alphanumeric of the group """
    bitmask = ['0'] * 36
    for char in group:
        if char.isalpha():
            index = ord(char.lower()) - ord('a')
        elif char.isdigit():
            index = ord(char) - ord('0') + NUMBER_OF_LETTERS
        else:
            continue
        bitmask[index] = '1'
    return ''.join(bitmask)


def is_file_relevant(bools: str, group_bitmask: str) -> bool:
    """ A relevant file contains the alphanumerics of the given group bitmask """
    for i in range(len(bools)):
        if bools[i] == '1' and group_bitmask[i] == '1':
            return True
    return False


def get_bool_from_index(index: int) -> bool:
    if index == -1:
        return False
    if bools[index] == '1':
        return True
    if bools[index] == '0':
        return False


def get_index_from_letter(char: str) -> int:
    """ Get the bool array index of the first char of the word """
    if char.isalpha():
        index = ord(char.lower()) - ord(FIRST_CHARACTER)
    elif char.isdigit():
        index = NUMBER_OF_LETTERS + int(char)
    else:
        index = -1
    return index

def list_map_files(directory):
    """
    List all .txt files in the directory that start with 'mapper_'.
    """
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.startswith('mapper_') and f.endswith('.txt')]

class Shuffler:
    def __init__(self, num_of_reducers: int):
        self.num_of_reducers: int = num_of_reducers
        self.groups: list = self.divide_alphabet(self.num_of_reducers)
        self.reducer_data: dict
        self.relevant_dicts: list[dict]

    def print_groups(self):
        print(self.groups)
    def shuffle(self) -> None:
        pass

    def filter_relevant_files(self) -> None:
        """
        Filter files based on the alphanumeric appearances in bools
        """
        # Find all files that contain words starting from letters in the group,
        # collect their data and send to reduce
        for index, group in enumerate(self.groups):
            # Create letter group bit code, will probably be consecutive bits
            group_bitmask = create_bitmask(group)
            # TODO implement directory
            files = list_map_files("/mnt/longhorn/mapper_out/")
            relevant_dicts = []
            for filename in files:
                with open(filename, 'r') as f:
                    lines = f.readlines()
                    file_bools = lines[0].strip()

                    # Check if the file is relevant based on the bools string
                    if is_file_relevant(file_bools, group_bitmask):
                        # read the second line as dictionary
                        dictionary = ast.literal_eval(lines[1].strip())
                        filtered_dict = {k: v for k, v in dictionary.items() if ((k[0] in group) or (k[0] in group.lower()))}
                        #self.process_dictionary(filtered_dict)
                        relevant_dicts.append(filtered_dict)
            # Write the relevant_dicts to a file with the group index in the filename
            output_file = f'/mnt/longhorn/shuffler_out/shuffler_{index}_{group}.json'
            with open(output_file, 'w') as f:
                json.dump(relevant_dicts, f)

    # TODO move to master
    def divide_alphabet(self, n: int) -> list:
        " Divide the alphabet in num of shufflers group"
        ALPHABET: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        base_size: int = NUMBER_OF_LETTERS // n
        extra_groups: int = NUMBER_OF_LETTERS % n
        groups: list = []
        start: int = 0
        for i in range(n):
            end = start + base_size + (1 if i < extra_groups else 0)
            groups.append(ALPHABET[start:end])
            start = end
        return groups


if __name__ == '__main__':
    # pod_name = os.environ.get('POD_NAME')
    # pod_index_store = pod_name.rsplit('-', 1)[-1]
    # pod_index = int(pod_index_store)
    num_reducers = int(os.environ.get('NUM_REDUCERS'))
    shuffler = Shuffler(num_reducers-1)
    shuffler.print_groups()
    shuffler.filter_relevant_files()
