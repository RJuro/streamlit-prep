import streamlit as st
import streamlit.components.v1 as components
import pydeck as pdk

import numpy as np
import pandas as pd 

import seaborn as sns #seaborn til plots
from matplotlib import pyplot as plt #plot control


from jupyterthemes import jtplot
jtplot.style(theme='monokai', context='notebook', ticks=True, grid=False)


st.set_page_config(page_title='Streamlit - Dashboard 🤯',
page_icon="🚀",
layout='wide'
)