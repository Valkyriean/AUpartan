from datetime import timedelta
import datetime

timeout = timedelta(days=1)

now = datetime.datetime.now()

new_time = now+timeout


print(new_time< datetime.datetime.now())
print(datetime.datetime.now())
print(new_time)