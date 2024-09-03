import os

from sqlalchemy import create_engine 

#----"os.path.abspath(__file__), basically gets the path of this exact file", "os.path.dirname() basically extracts the directory name from the path."
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f"sqlite:///{BASE_DIR}/db", echo=True)