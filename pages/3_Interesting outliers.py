import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit.components.v1 as components
from scipy import stats
from scipy.optimize import curve_fit
from math import exp


st.title("Interesting outliers")

st.header('Fall of the left movement in Brasil')

st.subheader('Guevara')