import streamlit as st
import pandas as pd
import plotly_express as px

df = pd.read_csv('vehicles_us.csv')
#seperates manufacturer from overall model field
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])
#creates column of the year of the posting
df['year'] = pd.DatetimeIndex(df['date_posted']).year
#calculates the age of the vehicle at time of posting
df['age'] = df['year'] - df['model_year']

#creates text header above the dataframe
st.header('Data viewer')
#displays dataframe using streamlit
st.dataframe(df)

st.header ('Fuel Type by Year')
st.write(px.histogram(df, x='fuel',
                      color = 'year',
                      color_discrete_sequence = ['navy', 'darkorange']
                      ))
st.header('Compare Price distribution between Vehicle Contions')
condition_list = sorted(df['condition'].unique())
condition_1 = st.selectbox('Select Condition 1',
                           condition_list, index=condition_list.index('like new'))

condition_2 = st.selectbox('Select Condition 2',
                           condition_list, index=condition_list.index('excellent'))
mask_filter = (df['condition'] == condition_1) | df['condition'] == condition_2
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize Histogram', value=True)
if normalize:
    histnorm = 'percent'

else:
    histnorm= None

st.write(px.histogram(df_filtered,
                      x='price',
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))
