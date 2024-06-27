import json
import os


directory = "/mnt/longhorn/shuffler_out"
directory_out = "/mnt/longhorn/reducer_out"

class Reducer:
    def __init__(self, reducer_id: str):
        self.reducer_id = reducer_id
        self.reduce_output_filename = f"reduced_out_{self.reducer_id}"
        self.reduced: dict = {}

    def reduce_file(self, input_filename: str, reduce_output_filename: str):
        # Read the JSON file containing the list of dictionaries
        with open(input_filename, 'r') as f:
            list_of_dicts = json.load(f)
        # Aggregate the counts for each key
        for dictionary in list_of_dicts:
            for key, value in dictionary.items():
                if key in self.reduced:
                    self.reduced[key] += value
                else:
                    self.reduced[key] = value
        # Write the final reduce
        with open(reduce_output_filename, 'w') as f:
            json.dump(self.reduced, f)

    def run(self):
        file_to_open = f"shuffler_{self.reducer_id}.json"
        filename = os.path.join(directory, file_to_open)
        reduce_output_file_to_open = f'reduced__{self.reducer_id}.json'
        reduce_output_filename = os.path.join(directory_out, reduce_output_file_to_open)
        self.reduce_file(filename, reduce_output_filename)


# Example usage
if __name__ == "__main__":
    pod_name = os.environ.get('POD_NAME')
    pod_index_store = pod_name.rsplit('-', 1)[-1]
    pod_index = int(pod_index_store)
    reducer_id = pod_index
    reducer = Reducer(str(reducer_id))
    reducer.run()
