from json import load
from xmlrpc.client import Boolean
import streamlit as st
import pandas as pd
import numpy as np
import time 
import matplotlib.pyplot as plt
from multiapp import MultiApp
from Apps import asg1, asg2, asg3, asg5, asg6, asg7, asg8


#variables
disrad = False

st.title("Data Analysis Tool")

file = st.file_uploader("Enter Dataset first to Proceed", type=['csv','txt'], accept_multiple_files=False, disabled=False)
# data = pd.read_csv(file)

def load_file():
    df = pd.read_csv(file)
    # st.header("Dataset Table")
    # st.dataframe(df, width=1000, height=500)
    return df
if file:
    data = load_file()  
    
    app = MultiApp()
    
    app.add_app("Assignment 1", asg1.app)
    app.add_app("Assignment 2", asg2.app)
    app.add_app("Assignment 3", asg3.app)
    app.add_app("Assignment 5", asg5.app)
    app.add_app("Assignment 6", asg6.app)
    app.add_app("Assignment 7", asg7.app)
    app.add_app("Assignment 8", asg8.app)
   
    # The main app
    app.run(data)

