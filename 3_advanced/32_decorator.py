# ADVANCED ***************************************************************************
# content = decorator
#
# date    = 2024-11-21
# email   = Stephane Barbin
#************************************************************************************


"""
0. CONNECT the decorator "print_process" with all sleeping functions.
   Print START and END before and after.

   START *******
   main_function
   END *********


1. Print the processing time of all sleeping functions.
END - 00:00:00


2. PRINT the name of the sleeping function in the decorator.
   How can you get the information inside it?

START - long_sleeping

"""


import time

# DECORATOR
def print_process(func):
    def wrapper(*args, **kwargs):
        print(f"START - {func.__name__}")

        start_time = time.time()
        
        result = func(*args, **kwargs)

        elapsed_time = time.time() - start_time
        
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        
        print(f"END - {time_str}")
        return result
    return wrapper

# FUNC
@print_process
def short_sleeping(name):
    time.sleep(0.1)
    print(name)

@print_process
def mid_sleeping():
    time.sleep(2)

@print_process
def long_sleeping():
    time.sleep(4)



short_sleeping("so sleepy")
mid_sleeping()
long_sleeping()