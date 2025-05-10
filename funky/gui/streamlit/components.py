import contextlib

import streamlit as st

def start_button():
    # Stack Overflow: https://stackoverflow.com/questions/77410751/writing-standard-output-on-streamlit-app-in-real-time
    button = st.button("Run")

def example_component():
    st.title()