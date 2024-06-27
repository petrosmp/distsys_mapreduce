import json
import os


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
        # Find all files corresponding to the pod ID
        files = [f for f in os.listdir("/mnt/longhorn/shuffler_out") if
                 f.startswith(f'shuffler_{self.reducer_id}_') and f.endswith('.json')]

        for filename in files:
            reduce_output_filename = f'/mnt/longhorn/reducer_out/reduced_{filename.split("_")[1]}_{filename.split("_")[2]}'
            self.reduce_file(filename, reduce_output_filename)


# Example usage
if __name__ == "__main__":
    pod_name = os.environ.get('POD_NAME')
    pod_index_store = pod_name.rsplit('-', 1)[-1]
    pod_index = int(pod_index_store)
    reducer_id = pod_index
    reducer = Reducer(str(reducer_id))
    reducer.run()
