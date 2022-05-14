from datetime import timedelta
import datetime
from random import uniform

timeout = timedelta(days=1)

now = datetime.datetime.now()

new_time = now+timeout


print(new_time< datetime.datetime.now())
print(datetime.datetime.now())
print(new_time)
a = 5
print(uniform(a-0.5,a+0.5))
