import multiprocessing
import math


def worker(method, items, NUMBER_OF_CPU, iteration, args, queue):
    result = method(items, NUMBER_OF_CPU, iteration, *args)
    queue.put(result)


def multiprocess(items, method, *args):
    NUMBER_OF_CPU = multiprocessing.cpu_count() - 1

    # Calculate the length of each part
    part_length = math.ceil(len(items) / NUMBER_OF_CPU)
    divided_list = [
        items[i : i + part_length] for i in range(0, len(items), part_length)
    ]

    # Create a queue to store the results
    result_queue = multiprocessing.Queue()

    processes = []

    for i in range(NUMBER_OF_CPU):
        if i < len(divided_list):
            p = multiprocessing.Process(
                target=worker, args=(method, divided_list[i], NUMBER_OF_CPU,i , args, result_queue)
            )
            processes.append(p)
            p.start()

    # Collect the results from the queue
    results = []
    for _ in range(len(processes)):
        result = result_queue.get()
        results.append(result)

    # Wait for all processes to complete
    for p in processes:
        p.join()

    return results
