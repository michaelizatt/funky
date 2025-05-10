from streamlit.web import cli as stcli
from streamlit import runtime
from app import app
import sys

# https://stackoverflow.com/questions/62760929/how-can-i-run-a-streamlit-app-from-within-a-python-script
if __name__ == '__main__':
    if runtime.exists():
        app()   # TODO Send through parsed functions here
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())