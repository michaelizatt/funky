import contextlib
import io
import time
from threading import Thread

import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

dir_path = Path(__file__).parent

class ThreadWithReturnValue(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        super().__init__(group, target, name, args, kwargs)
        self._return = None

    def run(self):
        try:
            if self._target is not None:
                self._return = self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def join(self, *args):
        super().join(*args)
        return self._return

# Generator to stream stdout live
def live_stdout_stream(func):
    buffer = io.StringIO()

    # Redirect stdout dynamically
    with contextlib.redirect_stdout(buffer):
        thread = ThreadWithReturnValue(target=func)  # Run the function in a separate thread
        thread.start()

        pos = 0
        thread_active = True

        # While the function is running, stream output
        while thread_active:
            if pos != buffer.tell():
                buffer.seek(pos)
                output = buffer.read()  # Returns an empty string if no new data written
                pos = buffer.tell()

                if output:
                    # Sets new line as soft return (Markdown spec)
                    yield output.replace("\n", "  \n")

            # Allows while loop to run one more time if data was printed right before function finishes
            if not thread.is_alive():
                thread_active = False


            time.sleep(0.1)  # Delay to allow

        thread.join()  # Ensure function completes

# Function with print statements
def my_function(r: int = 25):
    for i in range(r):
        print(f"Processing {i+1} of {r}...")
        time.sleep(0.1)
    print("Process complete!")

def app():
    # Streamlit app
    st.title("Real-Time stdout streaming")

    # Container to store function std out
    st.header("Log:")
    stdout_container = st.container(height=400, border=True)

    # Stream function output in real time
    # TODO find a way to get return from function
    stdout_container.write_stream(live_stdout_stream(my_function))

    _return = pd.DataFrame(np.random.randn(5, 5),
                           columns = ["a", "b", "c", "d", "e"]
                           )

    if _return is not None:
        st.header("Return:")
        st.write(_return)


if __name__ == "__main__":
    print("This will only run when streamlit is imported (or just run __init__ for testing...)")
    my_function()