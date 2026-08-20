import streamlit as st
import pandas as pd
import numpy as np



st.title("APC Discount and Waivers")
st.image("brock_logo.png",width=250)
st.write("Below are details about what APC discounts and waivers are available to members of the Brock community. More details can be found on the library [site](https://brocku.ca/library/open-access/open-access-investments/)")
st.write("_Information Last Updated: May, 19, 2026_")


pub_data = pd.read_csv("publisher_data.csv")
del pub_data["publisherID"]


publisher = st.selectbox(
	'Select Publisher',
	options=pub_data['publisher'].unique()

	)


flitered_pub_data = pub_data[pub_data['publisher'] == publisher]

pubName = flitered_pub_data["publisher"].values[0]
pubURL = flitered_pub_data["pubUrl"].values[0]

st.write("["+pubName+"]("+pubURL+")")
st.write("**Discount Details**")
st.write(flitered_pub_data["pubDiscount"].values[0])

st.table(pub_data)