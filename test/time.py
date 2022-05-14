from datetime import timedelta
import datetime
from random import uniform

timeout = timedelta(days=1)

now = datetime.datetime.now()

new_time = str(now+timeout)


print(new_time< str(datetime.datetime.now()))
print(datetime.datetime.now())
print(str(new_time))
a = 5
print(uniform(a-0.5,a+0.5))
