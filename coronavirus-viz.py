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

st.title("Coronavirus-Viz")
st.markdown("Feel free to explore the data. Click on an item in the legend to filter it out -- double-click an item to filter down to just that item. Or click and drag to filter the view so that you only see the range you are looking for.")
st.write("If you have any feedback or questions, feel free to get at me on the [Twitter] (https://www.twitter.com/aaroncolesmith) machine")


df=pd.read_csv('./covid_19_data.csv')

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '_').str.replace(')', '').str.replace('/','_')

df['observationdate'] = pd.to_datetime(df['observationdate'])

a = px.bar(df.groupby(['observationdate','country_region']).agg({'confirmed':sum}).reset_index(drop=False).sort_values(['confirmed'],ascending=False), x='observationdate',y='confirmed',color='country_region', title='Observations Over Time',width=1400, height=600).for_each_trace(lambda t: t.update(name=t.name.replace("country_region=","")))
st.plotly_chart(a)

b = px.bar(df.groupby(['observationdate','country_region']).agg({'deaths':sum}).reset_index(drop=False).sort_values(['deaths'],ascending=False), x='observationdate',y='deaths',color='country_region', title='Deaths Over Time',width=1400, height=600).for_each_trace(lambda t: t.update(name=t.name.replace("country_region=","")))
st.plotly_chart(b)

c = px.scatter(df.groupby(['country_region']).agg({'confirmed':max, 'deaths':max}).reset_index(),x='confirmed',y='deaths',color='country_region', title='Confirmed Cases vs. Deaths by Country',width=1400, height=600).for_each_trace(lambda t: t.update(name=t.name.replace("country_region=","")))
c.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))


st.plotly_chart(c)


dfg=df.groupby(['observationdate','country_region']).agg({'confirmed':sum}).reset_index(drop=False)

dfg.loc[dfg.confirmed >= 100, 'over_100'] = 1
dfg.loc[dfg.confirmed < 100, 'over_100'] = 0

g=pd.concat([dfg.loc[dfg.country_region == 'Mainland China'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'US'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'South Korea'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'Japan'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'Italy'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'Iran'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'Singapore'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'France'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'Japan'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'Germany'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'Spain'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'Hong Kong'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index(),
         dfg.loc[dfg.country_region == 'UK'].groupby(['observationdate','country_region','confirmed']).sum().cumsum().reset_index()
           .reset_index()], sort=False)



t=px.line(g.loc[g.over_100 > 0],x='over_100',y='confirmed',color='country_region', title='Confirmed Cases Since the 100th Observation',width=1400, height=600)
t.update_xaxes(title='Days Since 100th Observation')
t.update_yaxes(title='Confirmed Cases')
t.update_traces(mode='lines+markers')
st.plotly_chart(t)
