import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

# PS C:\Users\pablo\Desktop> cd .\WebApp\
# PS C:\Users\pablo\Desktop\WebApp> streamlit run .\myWebApp.py

#   You can now view your Streamlit app in your browser.  

#   Local URL: http://localhost:8501 
#   Network URL: http://192.168.1.35:8501

url = (
"C:/Users/pablo/Desktop/WebApp/debugged_singapore_airbnb.csv"
)
st.title('Airbnb prices in Singapore 🛏🌏')
st.subheader('AUTHOR: Pablo Benayas')
st.markdown('This application is a Streamlit dashboard that can be used '
'to analyze airbnb prices in Singapore')

data = pd.read_csv(url, parse_dates=['last_review']).iloc[:,1:]
data = data.loc[(data.price < 1050) & (data.price > 5),:]


# part I
st.header('Part I: Given a certain price range, where are airbnbs concentrated?')

select = st.selectbox('select option', ['low cost & medium price','high price'])
if select == 'high price':
    filter = data.loc[data.price > 200,:]
else:
    filter = data.loc[data.price <= 200,:]



# injured_people = st.slider('Select price range', 1, 6) 

select1 = st.slider('Select price (SGD)', float(filter.price.min()), float(filter.price.max()))
range = st.slider('Interval (previous price plus and minus selected value)', min_value=10, max_value=50, step=10)
st.map(filter.loc[(filter.price >= select1 - range) & (filter.price <= select1 + range),['latitude','longitude']].dropna(how='any')) 
# ‘any’ : If any NA values are present, drop that row or column.
 
 

st.subheader('Raw Data') 
st.markdown('(Prices sorted by ascending order)')
st.write(filter.loc[(filter.price >= select1 - range) & (filter.price <= select1 + range),
['price','host_name','neighbourhood','room_type']]\
    .sort_values(by='price', ascending=True))  


# part II
st.header('Part II: Given its room type, Where are the most expensive airbnb accomadations in Singapore?')
 

room_type_selected = st.selectbox('Select room type', data.room_type.unique()) 
# hour = st.sidebar.slider('Hour to look at', 0, 23) #same but with sidebar!! 
# separated by the difference of one
filtered_data = data.loc[data.room_type == room_type_selected,:]  

pct = round(len(data.loc[data.room_type==room_type_selected,:]) / len(data) * 100, 3) 
avg_price = round(filtered_data.price.median() ,3)

st.markdown('{}% of the airbnbs are of type "{}". The median price is {} SGD. (I choose the median here because mean values are highly affected by outliers in this dataset.)'\
    .format(pct, room_type_selected, avg_price))   


midpoint = (np.average(filtered_data.latitude), np.average(filtered_data.longitude))  



st.subheader('Map of "{}s". Color and size of every observation is based on its price.'\
    .format(room_type_selected)) 

st.write(pdk.Deck(
    map_style ='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude': midpoint[0],
        'longitude': midpoint[1],
        'zoom': 11,
        'pitch': 50,  # 3d parameter (either more vertical or horizontal degrees for visualization)
    },
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=filtered_data.loc[:,['price','longitude','latitude']],
            get_position=['longitude','latitude'], #(x,y) dont reverse order
            radius=100,
            extruded=True, # This is arg creates the 3d effect
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
        ), 
    ],
))



# # Part III: histogram

# st.subheader('Breakdown by number of available months where "{}" airbnbs can be booked in one year.'.format(room_type_selected))
# # filtered = data.loc[(data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < hour+1),:]
# i=0
# # bins = [i for i in range(0,366,30)] It works on jupyter, but somehow not here
# bins = [0,30,60,90,120,150,180,210,240,270,300,330,366]
# #  ['months: '+str(i) for i in range(1,13)]
# labels = ['m1 (less than one month available)','m2','m3','m4','m5','m6','m7','m8','m9','m10','m11','m12 = 1year']
# hist = pd.cut(filtered_data.availability_365 , bins=bins, labels=labels) 
#                                                   #we get the values with '[0]'

# hist_data = hist.value_counts()                                               

# fig = px.bar(hist_data, x=hist_data.index, y=hist_data, height=400)
# # reveal more information about a data point by moving their mouse cursor over 
# # the point and having a hover label appear.
# st.write(fig)