import streamlit as st
import streamlit.components.v1 as components
import pydeck as pdk

import numpy as np
import pandas as pd 

#import seaborn as sns #seaborn til plots
#from matplotlib import pyplot as plt #plot control


#from jupyterthemes import jtplot
#jtplot.style(theme='monokai', context='notebook', ticks=True, grid=False)


st.set_page_config(page_title='Streamlit - Dashboard 🤯',
page_icon="🚀",
layout='wide'
)


# LOAD DATA ONCE
@st.experimental_singleton
def load_data():
    data = pd.read_csv('http://data.insideairbnb.com/denmark/hovedstaden/copenhagen/2022-06-24/visualisations/listings.csv')

    # also preprocess as we did in the notebook
    data = data[data.number_of_reviews > 0]
    data = data[data.room_type.isin(['Private room', 'Entire home/apt'])]
    data['price_z'] = (data['price'] - data['price'].mean())/data['price'].std(ddof=0)
    data['price_z'] = data['price_z'].abs()
    data = data[data.price_z < 3]
    data['log_price'] = np.log(data['price'])

    return data


palette=['#FF4C4B','#FF9361', '#159090']


# LOAD THE DATA NOW!
data = load_data()


# STREAMLIT APP LAYOUT
data = load_data()


st.title("AirBnb rentals in Copenhagen 🇩🇰")

price_selected = st.slider("Select price range", min_value = int(data.price.min()), max_value= int(data.price.max()), value = (300,3000), step=50)
data = data[(data.price > price_selected[0]) & (data.price < price_selected[1])]


st.markdown('---')

#filter for neighborhoods

neighbourhood_select = st.multiselect('Select neighbourhoods', data.neighbourhood.unique(), data.neighbourhood.unique())
data = data[data.neighbourhood.isin(neighbourhood_select)]

st.markdown('---')

layer = pdk.Layer(
        "ScatterplotLayer",
        data=data[['name','room_type','price', "longitude", "latitude"]].dropna(),
        pickable=True,
        opacity=0.7,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position=["longitude", "latitude"],
        get_radius=10*"log_price",
        get_color=[255, 140, 0],
        get_line_color=[0, 0, 0],
    )

# Set the viewport location
view_state = pdk.ViewState(latitude=data['latitude'].mean(), longitude=data['longitude'].mean(), zoom=12, pitch=50)

# Renders
r = pdk.Deck(layers=[layer], 
initial_view_state=view_state,
#map_style='mapbox://styles/mapbox/light-v9',
tooltip={"text": "{name}\n{room_type}\n{price}"}
)

st.pydeck_chart(r)