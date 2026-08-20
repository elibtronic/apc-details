import streamlit as st
import pandas as pd


### Google Sheets

PUB_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPFcOiXgZAo6XENgRXj3FoQ_BnbsYtAJq0QtlnhjGmpIkQjIp8eZNX6C66tcaooh1pfaUR8AULfSji/pub?gid=1143475194&single=true&output=csv"
JOURNAL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPFcOiXgZAo6XENgRXj3FoQ_BnbsYtAJq0QtlnhjGmpIkQjIp8eZNX6C66tcaooh1pfaUR8AULfSji/pub?gid=0&single=true&output=csv"

###



#### Functions need to manipulate data


@st.cache_data(ttl=3600)
def get_data(JOURNAL_URL, PUB_URL):

	#combined data
    journalDF = pd.read_csv(JOURNAL_URL)
    pub_DF = pd.read_csv(PUB_URL)
    combined_DF = pd.merge(journalDF,pub_DF, on="Publisher")
    pub_DF["Publisher"] = "**"+pub_DF["Publisher"] + "** [:link:](" + pub_DF["pubUrl"]+")"
    pub_DF.columns = ["Publisher","URL","Discount"]


    return combined_DF, pub_DF


def get_openalex_journal(issn):   
    detail_string = ""
    try:
        j_item = requests.get("https://api.openalex.org/sources/issn:"+issn).json()
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


####


#### Render Page

combined_DF, pub_DF = get_data(JOURNAL_URL,PUB_URL)
st.image("brock_logo.png",width=200)
st.title("APC Discount and Waivers")
st.write("""Below are details about what Article Processing Charge (APC) discounts and waivers are available to members of the Brock community. 
	        More details can be found on the library site [:link:](https://brocku.ca/library/open-access/open-access-investments/)""")
st.write("**NB: Data is still being finalized and results are still incomplete.**")
st.write("""_Information Last Updated: May, 19, 2026_""")



journalTab, pubTab = st.tabs(['Journal','Publisher'])


with pubTab:
	st.table(pub_DF)


with journalTab:
	st.write("Journal")


