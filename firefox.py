#!/usr/bin/python

from winappdbg import Debug, EventHandler, System, Process
import sys

# breakout function
def PR_Write(event, memory_address, arg1, arg2, arg3):
    print(process.read(arg2, 1024)) # first KB of the argument (prints the memory pointer)

# this class specifies the module and function to intercept
class MyEventHandler(EventHandler):
    def load_dll(self, event):
        module = event.get_module()
        if module.match_name("nss3.dll"): # DLL file
            # getting the PID
            pid = event.get_pid()
            # function name
            address = module.resolve("PR_Write")
            # here we resolve the memory address - a breakpoint function is called PR_Write
            event.debug.hook_function(pid, address, preCB=PR_Write, postCB=None, paramCount=3, signature=None)

# debugger object with inheritance
debug = Debug(MyEventHandler())

try:
    # search for the firefox.exe process
    for (process, name) in debug.system.find_processes_by_filename("firefox.exe"):
        print(process.get_pid(), name) # retrieve the PID
    # attach it to the debugger
    debug.attach(process.get_pid())
    debug.loop()
except Exception as e:
    pass
finally:
    # stop debugging
    debug.stop()

# PR_Write Function (writes a buffer of data to a file or socket) the paramCount comes from the function definition (check docs)
# fs -> a pointer to the PRFileDesc
# bug -> a pointer to the buffer holding the data to be written -> this is the memory pointer
# amount -> the amount of data in bytes to be written from the buffer
