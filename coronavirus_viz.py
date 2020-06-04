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

@st.cache
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

    return df_us

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

    return df_all

def daily_growth_all(df):
    a=px.bar(df.loc[df.Date > df.Date.max() - pd.to_timedelta(90, unit='d')].groupby(['Date']).agg({'Confirmed_Growth':'sum'}).reset_index(),
    x='Date',
    y='Confirmed_Growth',
    title='Daily Growth in COVID Cases')
    a.update_layout(showlegend=True)
    a.update_xaxes(title_text='Date')
    a.update_yaxes(title_text='# of COVID Cases')
    st.plotly_chart(a)


def daily_deaths_all(df):
    a=px.bar(df.loc[df.Date > df.Date.max() - pd.to_timedelta(90, unit='d')].groupby(['Date']).agg({'Deaths_Growth':'sum'}).reset_index(),
    x='Date',
    y='Deaths_Growth',
    title='Daily COVID Deaths')
    a.update_layout(showlegend=True)
    a.update_xaxes(title_text='Date')
    a.update_yaxes(title_text='# of COVID Deaths')
    st.plotly_chart(a)


def bar_graph_country(df):
    #df['Country_Region'] = df.Country_Region.str[:15]
    df['Country'] = df.Country_Region.str[:15]
    a=px.bar(df.loc[df.Date > df.Date.max() - pd.to_timedelta(90, unit='d')].groupby(['Date','Country']).agg({'Confirmed_Growth':'sum'}).reset_index().sort_values('Confirmed_Growth',ascending=False),x='Date',y='Confirmed_Growth',color='Country', title = 'Daily Growth in COVID Cases by Country')
    a.update_layout(showlegend=True)
    a.update_xaxes(title_text='Date')
    a.update_yaxes(title_text='# of COVID Cases')
    st.plotly_chart(a)


def bar_graph_country_deaths(df):
    df['Country'] = df.Country_Region.str[:15]
    a=px.bar(df.loc[df.Date > df.Date.max() - pd.to_timedelta(90, unit='d')].groupby(['Date','Country']).agg({'Deaths_Growth':'sum'}).reset_index().sort_values('Deaths_Growth',ascending=False),
    x='Date',
    y='Deaths_Growth',
    color='Country',
    title = 'Daily Growth in COVID Deaths by Country')
    a.update_layout(showlegend=True)
    a.update_xaxes(title_text='Date')
    a.update_yaxes(title_text='# of COVID Deaths')
    st.plotly_chart(a)


def rolling_avg(df):
    d=df.loc[df.Date > df.Date.max() - pd.to_timedelta(90, unit='d')].groupby(['Date']).agg({'Confirmed_Growth':'sum'}).reset_index()
    d['Rolling_Avg'] = d['Confirmed_Growth'].rolling(window=7).mean()
    d1 = d.melt(id_vars=['Date']+list(d.keys()[5:]), var_name='val')
    fig=px.line(d1, x='Date', y='value', color='val',title='Daily COVID Cases vs. 7 Day Rolling Average', width=800)
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='# of COVID Cases')
    fig.update_traces(mode='lines+markers',
                      marker=dict(size=6,
                                  line=dict(width=1,
                                            color='DarkSlateGrey')))
    st.plotly_chart(fig)

def rolling_avg_deaths(df):
    d=df.loc[(df.Date > df.Date.max() - pd.to_timedelta(90, unit='d'))].groupby(['Date']).agg({'Deaths_Growth':'sum'}).reset_index()
    d['Rolling_Avg'] = d['Deaths_Growth'].rolling(window=7).mean()
    d1 = d.melt(id_vars=['Date']+list(d.keys()[5:]), var_name='val')
    fig=px.line(d1, x='Date', y='value', color='val',title='Daily COVID Deaths vs. 7 Day Rolling Average')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='# of COVID Deaths')
    fig.update_traces(mode='lines+markers',
                      marker=dict(size=6,
                                  line=dict(width=1,
                                            color='DarkSlateGrey')))
    st.plotly_chart(fig)

def state_rolling_avg(df, state):
    d=df.loc[(df.Date > df.Date.max() - pd.to_timedelta(90, unit='d')) & (df.Province_State == state)].groupby(['Date']).agg({'Confirmed_Growth':'sum'}).reset_index()
    d['Rolling_Avg'] = d['Confirmed_Growth'].rolling(window=7).mean()
    d1 = d.melt(id_vars=['Date']+list(d.keys()[5:]), var_name='val')
    fig=px.line(d1, x='Date', y='value', color='val',title='Daily COVID Cases vs. 7 Day Rolling Average for '+state)
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='# of COVID Cases')
    fig.update_traces(mode='lines+markers',
                      marker=dict(size=6,
                                  line=dict(width=1,
                                            color='DarkSlateGrey')))
    st.plotly_chart(fig)

def mortality_rate(df):
    d=df.groupby(['Date']).agg({'Deaths':'sum','Confirmed':'sum'}).reset_index()
    d['Mortality_Rate'] = (d.Deaths / d.Confirmed)*100

    fig=px.scatter(d.tail(30),x='Date',y='Mortality_Rate',width=800,title='Mortality Rate Over Time (Last 30 Days)',text='Mortality_Rate')
    fig.update_traces(textposition='bottom center',
                      texttemplate = '%{text:.2f}',
                      textfont_size=10,
                      marker=dict(size=6,
                                  line=dict(width=1,
                                            color='DarkSlateGrey')))
    st.plotly_chart(fig)


def state_deaths_rolling_avg(df, state):

    d=df.loc[(df.Date > df.Date.max() - pd.to_timedelta(60, unit='d')) & (df.Province_State == state)].groupby(['Date']).agg({'Deaths_Growth':'sum'}).reset_index()
    d['Rolling_Avg'] = d['Deaths_Growth'].rolling(window=7).mean()
    d1 = d.melt(id_vars=['Date']+list(d.keys()[5:]), var_name='val')
    fig=px.line(d1, x='Date', y='value', color='val',title='Daily COVID Deaths vs. 7 Day Rolling Average for '+state)
    #fig.update_traces(mode='lines')
    fig.update_traces(mode='lines+markers',
                      marker=dict(size=6,
                                  line=dict(width=1,
                                            color='DarkSlateGrey')))
    st.plotly_chart(fig)

def growth_vs_death(df, dimension,title):
    g=df.groupby([dimension,'Date']).agg({'Confirmed_Growth':'sum','Deaths_Growth':'sum'}).reset_index()
    g[str(dimension)+'_viz'] = ''
    g.loc[g.Confirmed_Growth > g.Confirmed_Growth.mean()*2, str(dimension)+'_viz'] = g[dimension]
    g.loc[g.Deaths_Growth > g.Deaths_Growth.mean()*2, str(dimension)+'_viz'] = g[dimension]
    fig=px.scatter(g.loc[g.Date == g.Date.max()],
           x='Confirmed_Growth',
           y='Deaths_Growth',
           width=800,
            text=str(dimension)+'_viz',
            color=dimension,
           title=title)
    fig.update_traces(mode='markers+text',
                                     textposition="top center",
                      marker=dict(size=8,
                                  line=dict(width=1,
                                            color='DarkSlateGrey')))
    #fig.show()
    st.plotly_chart(fig)

def coronavirus_viz():
    main()

def main():
    st.title("Coronavirus-Viz")
    st.markdown("Feel free to explore the data. Click on an item in the legend to filter it out -- double-click an item to filter down to just that item. Or click and drag to filter the view so that you only see the range you are looking for.")
    st.write("If you have any feedback or questions, feel free to get at me on the [Twitter] (https://www.twitter.com/aaroncolesmith) machine")

    st.write('<img src="https://www.google-analytics.com/collect?v=1&tid=UA-18433914-1&cid=555&aip=1&t=event&ec=coronavirus_viz&ea=coronavirus_viz">',unsafe_allow_html=True)


    df_us = load_data_us()
    df_all = load_data_global()
    a=df_us['Province_State'].unique()
    a=np.insert(a,0,'')
    report_date = df_all.Date.dt.date.max()

    daily_growth_all(df_all)
    bar_graph_country(df_all)
    rolling_avg(df_all)
    daily_deaths_all(df_all)
    bar_graph_country_deaths(df_all)
    mortality_rate(df_all)
    rolling_avg_deaths(df_all)
    growth_vs_death(df_all,'Country','New COVID Cases & Deaths by Country for ' + str(report_date))
    growth_vs_death(df_us,'Province_State','New COVID Cases & Deaths by State for ' + str(report_date))


    option=st.selectbox('Select a State to view data', a)
    if len(option) > 0:
        st.write('<img src="https://www.google-analytics.com/collect?v=1&tid=UA-18433914-1&cid=555&aip=1&t=event&ec=coronavirus_viz&ea='+option+'">',unsafe_allow_html=True)
        state=option
        state_rolling_avg(df_us, state)
        state_deaths_rolling_avg(df_us, state)

if __name__ == "__main__":
    #execute
    main()
