
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data #It helps streamlit in memorizing the data as it used again and again
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path = '../Day 10/data/data/mpg.csv') #It will read the original file again and again consuming more time
mpg_df = deepcopy(mpg_df_raw) #Work on the copy

st.title("Introduction to streamlit")
st.header("MPG Data Exploration")

#st.table(mpg_df)

if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(mpg_df)

#left_column, right_column = st.columns([1,2])
    
left_column, middle_column, right_column = st.columns([3,1,1])

years = ["All"]+sorted(pd.unique(mpg_df['year']))
year = left_column.selectbox("Choose a Year", years)

#st.write(year)

show_means = middle_column.radio(
    label='Show Class Means', options=['Yes', 'No'])

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)

#st.write(show_means)
if year == 'All':
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df['year'] == year]

st.write(reduced_df)

means = reduced_df.groupby('class').mean(numeric_only = True)
st.write(means)

m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)
ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

if show_means == "Yes":
    ax.scatter(means['displ'], means['hwy'], alpha=0.7,
               color="red", label="displ versus hwy mean values for 7 different classes")
ax.legend()
st.pyplot(m_fig)

p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity = 0.5,
                   range_x = [1,8], range_y=[10,50],
                   width=750, height=600, labels ={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                   title="Engine Size vs. Highway Fuel Mileage")
p_fig.update_layout(title_font_size=22)

#p_fig

if show_means == "Yes":
    p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'],
                               mode="markers"))
    p_fig.update_layout(showlegend=False)

st.plotly_chart(p_fig)

url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)
# "This works too:", url

# Sample Streamlit Map
st.subheader("Streamlit Map")
ds_geo = px.data.carshare()

st.dataframe(ds_geo.head())

ds_geo['lat'] = ds_geo['centroid_lat']
ds_geo['lon'] = ds_geo['centroid_lon']

#st.dataframe(ds_geo.head())

st.map(ds_geo)