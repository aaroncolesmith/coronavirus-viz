import pandas as pd
import numpy as np
import plotly_express as px
import streamlit as st

@st.cache(suppress_st_warning=True)
def load_data_us():
    try:
        df = pd.read_csv('./data/time_series_covid19_confirmed_US.csv')
    except:
        try:
            df = pd.read_csv('./coronavirus_viz/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
        except:
            df = pd.read_csv('./coviz/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
    df = df.drop(df.columns[0:5], axis=1)
    df=df.set_index(['Admin2','Province_State','Country_Region','Combined_Key','Lat','Long_']).stack().reset_index()
    df.columns=['Admin2','Province_State','Country_Region','Combined_Key','Lat','Long_','Date','Confirmed']

    df['Date']=pd.to_datetime(df.Date)
    tmp = df.groupby(['Combined_Key']).agg({'Confirmed':'sum'}).reset_index().sort_values('Confirmed',ascending=False).head(30)
    l = tmp.Combined_Key.unique()
    df.loc[df.Combined_Key.isin(l),'top_city'] = df.Combined_Key
    df['top_city']=df.top_city.fillna('Other')
    df['Confirmed_Growth'] = df['Confirmed']-df['Confirmed'].shift(1)
    df.loc[df.Combined_Key != df.Combined_Key.shift(1),'Confirmed_Growth'] = 0
    df['Confirmed_Growth_Pct'] = (df['Confirmed']-df['Confirmed'].shift(1))/df['Confirmed'].shift(1)
    df.loc[df.Combined_Key != df.Combined_Key.shift(1),'Confirmed_Growth_Pct'] = 0
    df['Confirmed_Growth_Pct'] = df.Confirmed_Growth_Pct.fillna(0)

    try:
        deaths_us = pd.read_csv('./data/time_series_covid19_deaths_US.csv')
    except:
        try:
            deaths_us = pd.read_csv('./coronavirus_viz/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
        except:
            deaths_us = pd.read_csv('./coviz/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

    deaths_us = deaths_us.drop(deaths_us.columns[0:5], axis=1)
    deaths_us=deaths_us.set_index(['Admin2','Province_State','Country_Region','Combined_Key','Lat','Long_']).stack().reset_index()
    deaths_us.columns=['Admin2','Province_State','Country_Region','Combined_Key','Lat','Long_','Date','Deaths']
    us_population = deaths_us.loc[deaths_us.Date == 'Population']
    deaths_us = deaths_us.loc[deaths_us.Date != 'Population']

    deaths_us['Date']=pd.to_datetime(deaths_us.Date)
    tmp = deaths_us.groupby(['Combined_Key']).agg({'Deaths':'sum'}).reset_index().sort_values('Deaths',ascending=False).head(30)
    l = tmp.Combined_Key.unique()
    deaths_us.loc[deaths_us.Combined_Key.isin(l),'top_city'] = deaths_us.Combined_Key
    deaths_us['top_city']=deaths_us.top_city.fillna('Other')
    deaths_us['Deaths_Growth'] = deaths_us['Deaths']-deaths_us['Deaths'].shift(1)
    deaths_us.loc[deaths_us.Combined_Key != deaths_us.Combined_Key.shift(1),'Deaths_Growth'] = 0
    deaths_us['Deaths_Growth_Pct'] = (deaths_us['Deaths']-deaths_us['Deaths'].shift(1))/deaths_us['Deaths'].shift(1)
    deaths_us.loc[deaths_us.Combined_Key != deaths_us.Combined_Key.shift(1),'Deaths_Growth_Pct'] = 0
    deaths_us['Deaths_Growth_Pct'] = deaths_us.Deaths_Growth_Pct.fillna(0)


    df_us = pd.merge(df, deaths_us, left_on=['Combined_Key','Date'],right_on=['Combined_Key','Date'])
    df_us = df_us[['Admin2_x','Province_State_x','Country_Region_x','Combined_Key','top_city_x','Lat_x','Long__x','Date','Confirmed','Confirmed_Growth','Confirmed_Growth_Pct','Deaths','Deaths_Growth','Deaths_Growth_Pct']]
    df_us.columns = ['Admin','Province_State','Country_Region','Combined_Key','Top_City','Lat','Long','Date','Confirmed','Confirmed_Growth','Confirmed_Growth_Pct','Deaths','Deaths_Growth','Deaths_Growth_Pct']
    df_us['State'] = df.Province_State.str[:15]

    return df_us

@st.cache(suppress_st_warning=True)
def load_data_global():
    try:
        confirmed_all = pd.read_csv('./data/time_series_covid19_confirmed_global.csv')
    except:
        try:
            confirmed_all = pd.read_csv('./coronavirus_viz/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
        except:
            confirmed_all = pd.read_csv('./coviz/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    confirmed_all=confirmed_all.set_index(['Province/State','Country/Region','Lat','Long']).stack().reset_index()
    confirmed_all['Combined_Key'] = confirmed_all['Province/State'].fillna('None') + ', ' + confirmed_all['Country/Region']
    confirmed_all.columns=['Province/State','Country/Region','Lat','Long','Date','Confirmed','Combined_Key']
    confirmed_all = confirmed_all[['Province/State','Country/Region','Combined_Key','Lat','Long','Date','Confirmed']]

    confirmed_all['Date']=pd.to_datetime(confirmed_all.Date)

    tmp = confirmed_all.groupby(['Combined_Key']).agg({'Confirmed':'sum'}).reset_index().sort_values('Confirmed',ascending=False).head(30)
    l = tmp.Combined_Key.unique()
    confirmed_all.loc[confirmed_all.Combined_Key.isin(l),'top_city'] = confirmed_all.Combined_Key
    confirmed_all['top_city']=confirmed_all.top_city.fillna('Other')

    confirmed_all['Confirmed_Growth'] = confirmed_all['Confirmed']-confirmed_all['Confirmed'].shift(1)
    confirmed_all.loc[confirmed_all.Combined_Key != confirmed_all.Combined_Key.shift(1),'Confirmed_Growth'] = 0
    confirmed_all['Confirmed_Growth_Pct'] = (confirmed_all['Confirmed']-confirmed_all['Confirmed'].shift(1))/confirmed_all['Confirmed'].shift(1)
    confirmed_all.loc[confirmed_all.Combined_Key != confirmed_all.Combined_Key.shift(1),'Confirmed_Growth_Pct'] = 0
    confirmed_all['Confirmed_Growth_Pct']=confirmed_all['Confirmed_Growth_Pct'].fillna(0)

    try:
        deaths_all = pd.read_csv('./data/time_series_covid19_deaths_global.csv')
    except:
        try:
            deaths_all = pd.read_csv('./coronavirus_viz/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
        except:
            deaths_all = pd.read_csv('./coviz/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    deaths_all=deaths_all.set_index(['Province/State','Country/Region','Lat','Long']).stack().reset_index()
    deaths_all['Combined_Key'] = deaths_all['Province/State'].fillna('None') + ', ' + deaths_all['Country/Region']
    deaths_all.columns=['Province/State','Country/Region','Lat','Long','Date','Deaths','Combined_Key']
    deaths_all = deaths_all[['Province/State','Country/Region','Combined_Key','Lat','Long','Date','Deaths']]

    deaths_all['Date']=pd.to_datetime(deaths_all.Date)
    tmp = deaths_all.groupby(['Combined_Key']).agg({'Deaths':'sum'}).reset_index().sort_values('Deaths',ascending=False).head(30)
    l = tmp.Combined_Key.unique()
    deaths_all.loc[deaths_all.Combined_Key.isin(l),'top_city'] = deaths_all.Combined_Key
    deaths_all['top_city']=deaths_all.top_city.fillna('Other')
    deaths_all['Deaths_Growth'] = deaths_all['Deaths']-deaths_all['Deaths'].shift(1)
    deaths_all.loc[deaths_all.Combined_Key != deaths_all.Combined_Key.shift(1),'Deaths_Growth'] = 0
    deaths_all['Deaths_Growth_Pct'] = (deaths_all['Deaths']-deaths_all['Deaths'].shift(1))/deaths_all['Deaths'].shift(1)
    deaths_all.loc[deaths_all.Combined_Key != deaths_all.Combined_Key.shift(1),'Deaths_Growth_Pct'] = 0
    deaths_all['Deaths_Growth_Pct'] = deaths_all.Deaths_Growth_Pct.fillna(0)

    df_all = pd.merge(confirmed_all, deaths_all, left_on=['Combined_Key','Date'],right_on=['Combined_Key','Date'])
    df_all = df_all[['Province/State_x','Country/Region_x','Combined_Key','top_city_x','Lat_x','Long_x','Date','Confirmed','Confirmed_Growth','Confirmed_Growth_Pct','Deaths','Deaths_Growth','Deaths_Growth_Pct']]
    df_all.columns = ['Province_State','Country_Region','Combined_Key','Top_City','Lat','Long','Date','Confirmed','Confirmed_Growth','Confirmed_Growth_Pct','Deaths','Deaths_Growth','Deaths_Growth_Pct']
    df_all['Country'] = df_all.Country_Region.str[:15]

    return df_all


def bar_graph(df, days_back, metric ,width=800, title=''):
    fig = px.bar(df.loc[df.Date > df.Date.max() - pd.to_timedelta(days_back, unit='d')].groupby(['Date']).agg({metric:'sum'}).reset_index(),
    x='Date',
    y=metric,
    title=title,
    width=width)
    # fig.show()
    st.plotly_chart(fig)

def bar_graph_dimension(df, days_back, metric, dimension, width=800, title=''):
    fig = px.bar(df.loc[df.Date > df.Date.max() - pd.to_timedelta(days_back, unit='d')].groupby(['Date',dimension]).agg({metric:'sum'}).reset_index().sort_values(dimension,ascending=False),
    x='Date',
    y=metric,
    color=dimension,
    title=title,
    width=width)
    # fig.show()
    st.plotly_chart(fig)

def rolling_avg(df, days_back, metric, width=800, title=''):
    d=df.loc[(df.Date > df.Date.max() - pd.to_timedelta(days_back, unit='d'))].groupby(['Date']).agg({metric:'sum'}).reset_index()
    d['Rolling_Avg'] = d[metric].rolling(window=7).mean()
    d1 = d.melt(id_vars=['Date']+list(d.keys()[5:]), var_name='val')
    fig=px.line(d1, x='Date', y='value', color='val',width=width,title=title)
    fig.update_traces(mode='lines+markers',
                      marker=dict(size=6,
                                  line=dict(width=1,
                                            color='DarkSlateGrey')))
    # fig.show()
    st.plotly_chart(fig)