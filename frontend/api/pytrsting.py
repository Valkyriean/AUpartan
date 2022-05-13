import queue
queueing_task = queue.Queue()
queueing_task.put(1)
queueing_task.put(2)
queueing_task.put(3)
print(list(queueing_task))