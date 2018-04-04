import time

cur_time = time.time()
cur_time = round((1000*cur_time-math.ceil(1000*cur_time)+1)/1000,2)
print(cur_time)