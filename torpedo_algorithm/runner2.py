from combiner import Combiner
from mapper import Mapper
from splitter import Splitter



if __name__ == "__main__":
    text = ("we are avid we fans of PyPy and commensurately thankful for the great work by the PyPy team over "
            "the years. PyPy has enabled us to use Python for a larger part of our toolset than CPython alone "
            "would have supported, and its smooth integration with C/C++ through CFFI has helped us attain a "
            "better tradeoff between performance and programmer productivity in our projects")

    # mappers = [Mapper(i) for i in range(len(splits))]
    splitter = Splitter(text, 10)
    splits = splitter.split()
    print(splits)
    # # Apply map function to each split
    # mappers: list[Mapper] = []
    # mapped_data_list: list[dict] = []
    # for i in splits:
    #     mapper = Mapper(i)
    #     mappers.append(mapper)
    #     mapped_data = mapper.map(splits[i])
    #     mapped_data_list.append(mapped_data)
    #
    # # combiners = [Combiner(i) for i in range(len(mappers))]
    # combiners: list[Combiner] = []
    # combined_data_list: list[dict] = []
    # for i, mapped_data in enumerate(mapped_data_list):
    #     (m_data, alphanumeric_appearances) = mapped_data_list[i]
    #     print(m_data)
    #     combiner = Combiner(i, m_data, alphanumeric_appearances)
    #     combiners.append(combiner)
    #     combined_data = combiner.combine(m_data)
    #     print(combined_data)
    #     combined_data_list.append(combined_data)
    # def save_splits(filename) -> None:
    #     """
    #     Save combiner data to a temporary file in permanent storage
    #     """
    #     # for splits
    #     with open(filename, 'w') as file:
    #         file.write(repr(self.combined))
    #
