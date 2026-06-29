import streamlit as st
import requests
import pandas as pd


### Google Sheets
PUB_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPFcOiXgZAo6XENgRXj3FoQ_BnbsYtAJq0QtlnhjGmpIkQjIp8eZNX6C66tcaooh1pfaUR8AULfSji/pub?gid=1143475194&single=true&output=csv"
JOURNAL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPFcOiXgZAo6XENgRXj3FoQ_BnbsYtAJq0QtlnhjGmpIkQjIp8eZNX6C66tcaooh1pfaUR8AULfSji/pub?gid=0&single=true&output=csv"
L_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe61TNpD96WMGonWeV-w0nkvQjGRCfKaB6qsFmzQQXhquFiiA/formResponse"

PREAMBLE = """
# Article Processing Charge Agreements
Below are details about what Article Processing Charge (APC) discounts and waivers are available to members of the Brock community. 
More details can be found on the library site [:link:](https://brocku.ca/library/open-access/open-access-investments/)

**NB: Data is still being finalized and results are still incomplete.**

_Information Last Updated: May, 19, 2026_
"""

logging = True

###



#### Functions need to manipulate data


@st.cache_data(ttl=3600,show_spinner="Please wait, downloading data...",show_time=True)
def get_data(JOURNAL_URL, PUB_URL):

	#combined data
    journalDF = pd.read_csv(JOURNAL_URL)
    pub_DF = pd.read_csv(PUB_URL)
    combined_DF = pd.merge(journalDF,pub_DF, on="Publisher")
    pub_DF["Publisher Description"] = "**"+pub_DF["Publisher"] + "** [:link:](" + pub_DF["pubUrl"]+")"
    del pub_DF["pubUrl"]
    pub_DF.columns = ["Publisher","Discount","Publisher Description"]
    combined_DF.columns = ["Publisher","Title","ISSN","Confidence","Publisher URL","Publisher Discount"]
    return combined_DF, pub_DF


def get_openalex_journal(issn,confidence):

    detail_string = ""

    if len(issn) == 8:
        issn = issn[0:4]+"-"+issn[4:]

    try:
        j_item = requests.get("https://api.openalex.org/sources/issn:"+issn).json()

        if confidence != 1:
	        if not j_item['is_oa']:
	            detail_string += " - Title is not considered _Open Access_ and  may be eligible for discount. :arrow_right: Please check _Publisher Discount_ for specifications and see [journal homepage]("+j_item['homepage_url']+") to ensure discount applies."
	        else: 
	            detail_string += " - Title is considered _Open Access_ or _Hybrid_ and may be eligible for disount. :arrow_right: Please check _Publisher Discount_ for specifications and see [journal homepage]("+j_item['homepage_url']+") to ensure discount applies."

        if j_item["apc_usd"]: 
            detail_string += "\n - Usual Article Processing Charge for this title is: **"+str(j_item["apc_usd"])+"** USD"

        detail_string += "\n - More analytics for this title from [OpenAlex]("+j_item['ids']['openalex']+")"
    except:
        detail_string = "**Could not retrieve extra journal information**"
    return detail_string


def log_apc_use(L_URL,issn="",publisher=""):
    form_data = {
        "entry.192508866": issn,
        "entry.789120919": publisher,
    }
    result = requests.post(L_URL,data=form_data)
    return result

####



#### Load data using cache function


combined_DF, pub_DF = get_data(JOURNAL_URL,PUB_URL)


#### Render Page
st.image("images/logo.png",width=200)
st.write(PREAMBLE)



journalTab, pubTab = st.tabs(['By Journal','Publisher'])


with pubTab:
	st.table(pub_DF[["Publisher Description","Discount"]])


with journalTab:
	pubSelect = st.selectbox(label="Select a publisher to narrow", index=None, options=combined_DF["Publisher"].sort_values(ascending=True).unique())

	if pubSelect:
		infoshow = combined_DF[combined_DF["Publisher"] == pubSelect]
		st.write("General publisher discount details:")
		pub_details = pub_DF[pub_DF["Publisher"] == pubSelect]["Discount"].iloc[0]
		st.write(" - "+pub_details)
		if logging:
			log_apc_use(L_URL,publisher=pubSelect)

		st.write("_Select a journal title for more information_")

		event = st.dataframe(infoshow[["Title","ISSN"]],on_select="rerun",selection_mode="single-row")
		#st.dataframe(infoshow[["Title","ISSN"]],hide_index=True)
		st.write("Total titles for this publisher: ",len(infoshow))
	else:
		infoshow = combined_DF
		st.write("_Journal Titles_")
		event = st.dataframe(infoshow[["Title","ISSN"]],on_select="rerun",selection_mode="single-row")
		st.write("Total titles for all publishers: ",len(infoshow))

	if event.selection.rows:

		j_details = {

		"Title": infoshow.iloc[event.selection.rows[0]]["Title"],
		"ISSN" : infoshow.iloc[event.selection.rows[0]]["ISSN"],
		"Publisher": infoshow.iloc[event.selection.rows[0]]["Publisher"],
		"Confidence": infoshow.iloc[event.selection.rows[0]]["Confidence"],
		"Publisher Discount": infoshow.iloc[event.selection.rows[0]]["Publisher Discount"]
		}

		j_details["Additional Information"] = get_openalex_journal(j_details["ISSN"],j_details["Confidence"])
		del j_details["Confidence"] #comment back out for diagnostic info

		if logging:
			log_apc_use(L_URL,issn=j_details["ISSN"])

		st.table(j_details)
		







