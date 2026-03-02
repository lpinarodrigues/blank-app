import subprocess
import sys

# Este arquivo serve apenas como ponte para o Streamlit Cloud
# Ele executa o seu arquivo principal 'main.py'
from main import *

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", "main.py"]
    sys.exit(stcli.main())
