import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import streamlit.components.v1 as components
import cv2

# @st.cache(persist=True)
# def load_data():


# @st.cache(persist=True)
# def train():

html = """
  <style>
  u{
  text-decoration-line: underline;
  text-decoration-style: double;
  }

  mark{
  font-weight: bold; 
  background-color: yellow;
  color: black;
  }

  font{
   color: grey;
  }

  embed:focus {
  outline: none;
}
  
}
    
  </style>
"""
st.markdown(html, unsafe_allow_html=True)
r1 = pd.read_csv("r1.csv")
crop_data = pd.read_csv("crop_data.csv")
st.title("Crop Advisory For Farmers")
st.sidebar.subheader("Select your State")
State_list = list(r1['state'].unique())
State = st.sidebar.selectbox("state: ", r1['state'].unique())
attributes = []

# rainfall prediction
st.subheader("Annual Rainfall prediction for your state for the year 2020: ")
x = pd.DataFrame(r1, columns=['le_state', 'le_year'])
y = pd.DataFrame(r1, columns=['rainfall_avg'])
lr = LinearRegression().fit(x, y)

if State:
    pred_data = [[State_list.index(State), 120]]
    # rainfall prediction
    pred = lr.predict(pred_data)
    strr_ = str(pred)
    strr_ = strr_.replace('[[', '')
    strr_ = strr_.replace(']]', '')

    st.write(" %s mm" % strr_)
    st.sidebar.subheader("Enter Crop Attributes: ")
    Season_list = list(crop_data['Season'].unique())
    Season = st.sidebar.selectbox("Enter Season: ", crop_data['Season'].unique())
    ph = st.sidebar.number_input("Enter PH content: ", 0.5, 8.5, 0.5)
    n = st.sidebar.number_input("Enter Nitrogen content: ", 2.0, 90.0, 2.0)
    p = st.sidebar.number_input("Enter Phosphorous content: ", 1.0, 50.0, 1.0)
    k = st.sidebar.number_input("Enter Potassium content: ", 0.5, 20.0, 0.5)
    temp = st.sidebar.number_input("Enter temperature: ", 2.0, 50.0, 2.0)
    st.subheader("Most profitable crop for your state is: ")

    x_ = crop_data[['Season_le', 'ph_avg', 'n', 'p', 'k', 'avg_temp', 'rainfall_avg']]
    y_ = crop_data.Crop
    clf = DecisionTreeClassifier().fit(x_, y_)
    i = Season_list.index(Season)
    predictors = [i, ph, n, p, k, temp, pred]
    str_ = str(clf.predict([predictors]))
    # st.write(str(clf.predict([predictors])))
    str_ = str_.replace('[\'', '')
    str_ = str_.replace('\']', '')

    st.write(str_)

    if st.button("SHOW INSIGHTS FOR THE CROP"):
        if str_ == "Arhar/Tur":
            st.image("data_insights/Arhar_Tur.png", width=800)
        st.image("data_insights/%s.png" % str_, width=800)
