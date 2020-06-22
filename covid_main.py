import pandas as pd
import numpy as np
import plotly_express as px
import streamlit as st
from covid_functions import load_data_us, load_data_global, bar_graph, bar_graph_dimension, rolling_avg

def main_dash(df):
    #Bar Graph - confirmed cases over time
    metric = 'Confirmed_Growth'
    bar_graph(df,90,metric,800,'Daily Growth in COVID Cases')
    bar_graph_dimension(df,90,metric,'Country',800,'Daily Growth in COVID Cases by Country')
    rolling_avg(df,90,metric,800,'7 Day Rolling Avg of COVID Cases')


def main():
    df_us = load_data_us()
    df_all = load_data_global()
    report_date = df_all.Date.dt.date.max()


    radio_selection = st.sidebar.radio('Select a page:',['Main Dashboard','Breakdown by US State','Breakdown by US County'])

    if radio_selection == 'Main Dashboard':
        st.write('Main')
        st.write(str(df_us.index.size))
        main_dash(df_all)
        # dashboard(df_all, report_date)
    if radio_selection == 'Breakdown by US State':
        st.write('US State')
        # state_dashboard(df_us, report_date)
    if radio_selection == 'Breakdown by US County':
        st.write('County')
        # county_dashboard(df_us, report_date)

if __name__ == "__main__":
    #execute
    main()
