import os
from classes.map import Mapper

job_id = os.environ.get('JOB_ID')

# Give chunk and id
if __name__ == "__main__":
    pod_index = int(os.environ.get('JOB_COMPLETION_INDEX'))

    input_filename = f'/mnt/longhorn/job_{job_id}/split_out/split{pod_index}.txt'

    #file to map given by coordinator
    with open(input_filename, 'r') as in_file:
        split = in_file.read()
    mapped_data_list: list[dict] = []
    mapper = Mapper(pod_index)
    mapped_data = mapper.map(split)
    mapper.save_combiner_data()

# import os
# from classes.map import Mapper
#
# # Simulating job_id for local testing
# job_id = "test_job_001"
#
# def create_test_file(filename, content):
#     """Create a test file with given content."""
#     os.makedirs(os.path.dirname(filename), exist_ok=True)
#     with open(filename, 'w') as f:
#         f.write(content)
#
# def read_combiner_output(filename):
#     """Read and return the content of the combiner output file."""
#     with open(filename, 'r') as f:
#         return f.read()
#
# if __name__ == "__main__":
#     # Simulate pod_index
#     pod_index = 0
#
#     # Create a test input file
#     input_filename = f'test_data/job_{job_id}/split_out/split{pod_index}.txt'
#     test_content = """
#     Hello world! This is a test file.
#     It contains some words to map and count.
#     Hello again, world!
#     """
#     create_test_file(input_filename, test_content)
#
#     # Create mapper instance
#     mapper = Mapper(pod_index)
#
#     # Read the test file
#     with open(input_filename, 'r') as in_file:
#         split = in_file.read()
#
#     # Map the content
#     mapped_data = mapper.map(split)
#
#     # Print mapped data
#     print("Mapped data:")
#     print(mapped_data)
#
#     print("\nTest completed successfully!")