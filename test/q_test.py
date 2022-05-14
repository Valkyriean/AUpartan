import queue

# a = queue.Queue()
# a.put(0)
# a.put(1)

# print(list(a.queue))


queueing_task = queue.Queue()
queueing_task.put({"name":"123"})
# (due date, task, worker IP)
working_task = [(0,{"name":"234"},0)]
finished_task = ["456"]

def check_global(task_name):
    if check_finished(task_name):
        return True
    for t in list(queueing_task.queue):
        if t.get("name",None) == task_name:
            return True
    for t in working_task:
        if t[1].get("name",None) == task_name:
            return True
    return False

def check_finished(task_name):
    return task_name in finished_task

print(check_global("124"))