import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)
def make_dataset(JOURNAL_URL, PUB_URL):
    journalDF = pd.read_csv(JOURNAL_URL)
    pubDF = pd.read_csv(PUB_URL)
    combinedDF = pd.merge(journalDF,pubDF, on="Publisher")
    return combinedDF


def journal_details(issn):   
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


