import streamlit as st
import pandas as pd
import sqlite3


conn = sqlite3.connect("apc-details.db")
#journalDF = pd.read_sql_query("SELECT * from journalInfo",con=conn)
#publisherDF = pd.read_sql_query("SELECT * from publisherInfo",con=conn)
apc_info = pd.read_sql_query("SELECT * from apcDetails",con=conn)
conn.close()

#with st.sidebar:
	#st.write("Journal Information")
	#st.write("Publisher Information")


st.title("APC Discount and Waivers")
st.image("brock_logo.png",width=250)
st.write("Below are details about what APC discounts and waivers are available to members of the Brock community. More details can be found on the library [site](https://brocku.ca/library/open-access/open-access-investments/)")
st.write("_Information Last Updated: May, 19, 2026_")


st.sidebar.header('Publishers')
st.sidebar.header('Journals')



st.dataframe(apc_info)
