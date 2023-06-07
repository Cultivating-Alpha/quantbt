import multiprocessing
import math


def multiprocess(items, method):
    NUMBER_OF_CPU = multiprocessing.cpu_count()

    # Calculate the length of each part
    part_length = len(items) // NUMBER_OF_CPU
    part_length = math.ceil(len(items) / NUMBER_OF_CPU)
    print(part_length)

    divided_list = [
        items[i : i + part_length] for i in range(0, len(items), part_length)
    ]
    print(divided_list)

    processes = []

    for i in range(NUMBER_OF_CPU):
        if i < len(divided_list):
            p = multiprocessing.Process(target=method, args=(divided_list[i],))
            processes.append(p)
            p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()
