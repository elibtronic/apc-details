import streamlit as st
import pandas as pd
import sqlite3
import requests
import json


def journal_details(issn):   
    detail_string = ""
    j_item = requests.get("https://api.openalex.org/sources/issn:"+issn).json()
    try:

        if not j_item['is_oa']:
            detail_string += " - Title is _closed_ and might be eligible for discount. Please see [journal homepage]("+j_item['homepage_url']+")"
        else: 
            detail_string += " - Could not determine if title is eligible for discount, or title might already be open access. Please see [journal homepage]("+j_item['homepage_url']+")"
        
        if j_item["apc_usd"]: 
            detail_string += "\n- Usual Author Processing Charge for this title is: **"+str(j_item["apc_usd"])+"** USD"

        detail_string += "\n- More analytics for this title from [OpenAlex]("+j_item['ids']['openalex']+")"
    except:
        detail_string = "**Could not retrieve extra journal information**"
    return detail_string



@st.cache_data(ttl=3600)
def get_publisher_info():
	conn = sqlite3.connect("apc-details.db")
	pub_info = pd.read_sql_query("SELECT * from publisherInfo",con=conn)
	conn.close()
	pub_info["Publisher"] = "**"+pub_info["Publisher"] + "** [:link:](" + pub_info["pubUrl"]+")"
	del(pub_info["pubUrl"])
	pub_info.columns = ["Publisher", "Discount Details"]
	return pub_info

@st.cache_data(ttl=3600)
def get_apc_info():
	conn = sqlite3.connect("apc-details.db")
	apc_info = pd.read_sql_query("SELECT * from apcDetails",con=conn)
	apc_info.sort_values(by=["Journal_Title"],inplace=True)
	conn.close()
	return apc_info


#st.image("brock_logo.png",width=200)
st.title("APC Discount and Waivers")
st.write("""Below are details about what Article Processing Charge (APC) discounts and waivers are available to members of the Brock community. 
	        More details can be found on the library site [:link:](https://brocku.ca/library/open-access/open-access-investments/)""")
st.write("**NB: Data is still being finalized and results are still incomplete.**")
st.write("""_Information Last Updated: May, 19, 2026_""")


journalTab, pubTab = st.tabs(['Journal','Publisher'])


with pubTab:
	st.write("The following is general information discounts and waivers by publisher.")
	pub_info = get_publisher_info()
	st.table(pub_info)

with journalTab:

	apc_info = get_apc_info()
	pubSelect = st.selectbox(label="Select a Publisher to Narrow", index=None, options=apc_info["Publisher"].sort_values(ascending=True).unique())

	if pubSelect:
		infoshow = apc_info[apc_info["Publisher"] == pubSelect]
		st.write("Details for: "+str(pubSelect))

		#pub_info["Publisher"] == pubSelect
		

		st.write("_Select Title for more information_")
		event = st.dataframe(infoshow[["Journal_Title"]],on_select="rerun",selection_mode="single-row")
		st.write("_Titles total for publisher: "+ str(len(infoshow))+"_")
	else:
		infoshow = apc_info
		event = st.dataframe(infoshow[["Journal_Title","Publisher","pubDiscount"]],on_select="rerun",selection_mode="single-row")
		st.write("_Titles total for all publishers: "+ str(len(infoshow))+"_")

	if event.selection.rows:		
		#st.dataframe(infoshow.iloc[event.selection.rows[0]])
		st.markdown("--------")
		st.markdown("")
		st.markdown(" **Journal Title:** "+infoshow.iloc[event.selection.rows[0]]['Journal_Title'])
		st.markdown("**Publisher:** "+infoshow.iloc[event.selection.rows[0]]['Publisher'])
		st.markdown("**Typical Publisher Discount:** "+infoshow.iloc[event.selection.rows[0]]['pubDiscount'])
		st.markdown("--------")
		st.markdown("**Extra Details:** ")
		st.markdown(journal_details(infoshow.iloc[event.selection.rows[0]]['ISSN']))




