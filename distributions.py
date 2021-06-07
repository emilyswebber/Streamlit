import math
import streamlit as st 
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from numpy.random import seed
import pandas as pd
import pygsheets
import seaborn as sns
from matplotlib.pyplot import figure
import plotly.graph_objects as go
from math import sqrt
from scipy.stats import norm

st.set_page_config(initial_sidebar_state='auto')

seed(100)
st.sidebar.markdown("**Indicate the Capacity.**")

capacity = st.sidebar.number_input('', 0, 1000000, 3500)

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.markdown("**Indicate count in each category.**")


count1 = st.sidebar.number_input('How many in Category 1?', 0, 1000000, 1000)
count2 = st.sidebar.number_input('How many in Category 2?', 0, 1000000, 1000)
count3 = st.sidebar.number_input('How many in Category 3?',  0, 1000000, 1000)

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.markdown("**Indicate avg days for each category.**")

mean1 = st.sidebar.number_input('Average Days Category 1', 0, 1000000, 25)
mean2 = st.sidebar.number_input('Average Days Category 2',  0, 1000000, 32)
mean3 = st.sidebar.number_input('Average Days Category 3',  0, 1000000, 51)

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.markdown("**Indicate stdev days for each category.**")

sd1 = st.sidebar.number_input('Standard Dev. Days Category 1', 0, 1000000, 5)
sd2 = st.sidebar.number_input('Standard Dev. Days Category 2', 0, 1000000, 7)
sd3 = st.sidebar.number_input('Standard Dev. Days Category 3', 0, 1000000, 10)

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.markdown("**Indicate how many days out you want to simulate.**")
max_d = st.sidebar.number_input('', 0, 365, 100)



#count1 = 1000
#count2 = 1000
#count3 = 1000

#mean1 = 25
#mean2 = 32
#mean3 = 51

#sd1 = 5
#sd2 = 7
#sd3 = 10

#capacity = 150

cat_1 = np.random.normal(mean1, sd1, count1)
cat_2 = np.random.normal(mean2, sd2, count2)
cat_3 = np.random.normal(mean3, sd3, count3)


cat_1b = pd.DataFrame(cat_1, columns=['Days']) 
cat_2b = pd.DataFrame(cat_2, columns=['Days']) 
cat_3b = pd.DataFrame(cat_3, columns=['Days']) 

cat_1b['Days'] = cat_1b['Days'].round(0)
c1_counts = cat_1b['Days'].value_counts()
c1_counts2 = c1_counts.to_frame()
c1_counts2 = c1_counts2.sort_index()
c1_counts2['Cumulative_C1'] = c1_counts2['Days'].cumsum()
c1_counts2['xaxis'] = c1_counts2.index
c1 = c1_counts2[['xaxis', 'Days']]

cat_2b['Days'] = cat_2b['Days'].round(0)
c2_counts = cat_2b['Days'].value_counts()
c2_counts2 = c2_counts.to_frame()
c2_counts2 = c2_counts2.sort_index()
c2_counts2['Cumulative_C2'] = c2_counts2['Days'].cumsum()
c2_counts2['xaxis'] = c2_counts2.index
c2 = c2_counts2[['xaxis', 'Days']]

cat_3b['Days'] = cat_3b['Days'].round(0)
c3_counts = cat_3b['Days'].value_counts()
c3_counts2 = c3_counts.to_frame()
c3_counts2 = c3_counts2.sort_index()
c3_counts2['Cumulative_C3'] = c3_counts2['Days'].cumsum()
c3_counts2['xaxis'] = c3_counts2.index
c3 = c3_counts2[['xaxis', 'Days']]


df = pd.DataFrame({ 'A' : range(1, max_d + 1 ,1)})


df_2 = df.merge(
    c1, 
    left_on = 'A', 
    right_on = 'xaxis',
    how = 'left')

df_2['Cumulative_C1'] = df_2['Days'].fillna(0)
df_2['Cumulative_C1b'] = df_2['Cumulative_C1'].cumsum()
df_2['Cat_1_Counts'] = count1 - df_2['Cumulative_C1b']

df_2 = df_2[['A', 'Cat_1_Counts']]


df_3 = df_2.merge(
    c2, 
    left_on = 'A', 
    right_on = 'xaxis',
    how = 'left')

df_3['Cumulative_C2'] = df_3['Days'].fillna(0)
df_3['Cumulative_C2b'] = df_3['Cumulative_C2'].cumsum()
df_3['Cat_2_Counts'] = count2 - df_3['Cumulative_C2b']

df_3 = df_3[['A', 'Cat_1_Counts', 'Cat_2_Counts']]


df_4 = df_3.merge(
    c3, 
    left_on = 'A', 
    right_on = 'xaxis',
    how = 'left')

df_4['Cumulative_C3'] = df_4['Days'].fillna(0)
df_4['Cumulative_C3b'] = df_4['Cumulative_C3'].cumsum()
df_4['Cat_3_Counts'] = count3 - df_4['Cumulative_C3b']

df_4 = df_4[['A', 'Cat_1_Counts', 'Cat_2_Counts', 'Cat_3_Counts']]

df_4.head(50)


plt.rcParams["figure.figsize"] = (20,10)
plt.rcParams.update({'font.size': 22})


"""
## "What-If"  Simulator   


"""

fig1 = plt.figure()

plt.rcParams["figure.figsize"] = (20,10)
plt.rcParams.update({'font.size': 22})

x = df_4['A']

plt.bar(x, df_4['Cat_1_Counts'], color='#39B54E')
plt.bar(x, df_4['Cat_2_Counts'], bottom= df_4['Cat_1_Counts'], color='#2D8FE2')
plt.bar(x, df_4['Cat_3_Counts'],bottom= df_4['Cat_1_Counts'] + df_4['Cat_2_Counts'],  color='#662D91')
plt.xlabel('Days')
plt.ylabel('UC Count')
plt.legend(prop ={'size': 20})
plt.axhline(y=capacity, color='r', linestyle='-')



st.pyplot(fig1)