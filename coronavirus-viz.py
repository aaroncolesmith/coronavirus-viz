import pandas as pd
import numpy as np
import plotly_express as px
import streamlit as st

def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )

_max_width_()

st.title("Coronavirus Viz")
st.markdown("Feel free to explore the data. Click on an item in the legend to filter it out -- double-click an item to filter down to just that item.")

df=pd.read_csv('./covid_19_data.csv')

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '_').str.replace(')', '').str.replace('/','_')

df['observationdate'] = pd.to_datetime(df['observationdate'])

a = px.bar(df.groupby(['observationdate','country_region']).agg({'confirmed':sum}).reset_index(drop=False).sort_values(['confirmed'],ascending=False), x='observationdate',y='confirmed',color='country_region', title='Observations Over Time',width=1400, height=600)
st.plotly_chart(a)

b = px.bar(df.groupby(['observationdate','country_region']).agg({'deaths':sum}).reset_index(drop=False).sort_values(['deaths'],ascending=False), x='observationdate',y='deaths',color='country_region', title='Deaths Over Time',width=1400, height=600)
st.plotly_chart(b)
