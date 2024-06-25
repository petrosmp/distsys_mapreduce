text = ("we are avid fans of PyPy and commensurately thankful for the great work by the PyPy team over "
        "the years. PyPy has enabled us to use Python for a larger part of our toolset than CPython alone "
        "would have supported, and its smooth integration with C/C++ through CFFI has helped us attain a "
        "better tradeoff between performance and programmer productivity in our projects")

from combiner import Combiner
from mapper import Mapper
from splitter import Splitter
from reducer import Reducer


def save_mapper_data(id: int, group_id: int, mapper_output_data: list, filename: str) -> None:
    """
    Save mapper data to a temporary file
    """
    with open(filename, 'w') as file:
        file.write(f"group_id = {group_id}\n")
        file.write(f"mapper_{id}_output = ")
        file.write(repr(mapper_output_data))


def distribute_combined_data(combined_data_list: list, num_reducers: int) -> list:
    """ GPTahh method"""
    distributed = [[] for _ in range(num_reducers)]
    for i, combined_data in enumerate(combined_data_list):
        distributed[i % num_reducers].append(combined_data)
    return distributed


if __name__ == "__main__":
    words_per_split = 5
    splitter = Splitter(text, words_per_split)
    # Split the input string
    splits = splitter.split()
    print(splits)
    # Initialize Mapper instances
    mappers = [Mapper() for _ in range(len(splits))]

    # Apply map function to each split
    mapped_data_list = []
    for i in splits:
        mapper = Mapper()
        mappers.append(mapper)
        # print(splits[i])
        mapped_data = mapper.map(splits[i])
        print(f'Mapper {i} output: {mapped_data}')
        mapped_data_list.append(mapped_data)

    # for i, data in mapped_data.items():
    #     print(f'Mapper {i} output: {data}')
    # Combine data
    combiners = [Combiner() for _ in range(len(mappers))]
    combined_data_list = []
    for i, mapped_data in enumerate(mapped_data_list):
        combiner = Combiner()
        combiners.append(combiner)
        combined_data = combiner.combine(mapped_data)
        print(f'Combiner {i} output: {combined_data}')
        combined_data_list.append(combined_data)

    # reducer = Reducer()
    # final_counts = reducer.reduce(combined_data_list)
    # print("1 reducer result.", final_counts)

    # Distribute combined data to reducers
    num_reducers = 6
    distributed_data = distribute_combined_data(combined_data_list, num_reducers)

    # Reduce distributed data
    reducers = [Reducer() for _ in range(num_reducers)]
    reduced_data_list = []
    for i, combined_data_chunk in enumerate(distributed_data):
        reducer = reducers[i]
        reduced_data = reducer.reduce(combined_data_chunk)
        print(f'Reducer {i} output: {reduced_data}')
        reduced_data_list.append(reduced_data)

    # Sequentially combine the reduced data from all reducers
    final_reducer = Reducer()
    final_counts = final_reducer.reduce(reduced_data_list)

    print("Final word counts:", final_counts)

