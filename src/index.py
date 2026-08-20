import streamlit as st
import requests
import pandas as pd
import config



#### Functions need to manipulate data
@st.cache_data(ttl=3600,show_spinner="Please wait, downloading data...",show_time=True)
def get_data(JOURNAL_URL, PUB_URL):
    
    #This maps our verfied column in the data spreadsheet to some more interesting icons
    verify_map = {
        0 : "❓",
        1 : "✅",
        2 : "⛔",
    }

	#combined data
    journalDF = pd.read_csv(JOURNAL_URL)
    pub_DF = pd.read_csv(PUB_URL)
    combined_DF = pd.merge(journalDF,pub_DF, on="Publisher")

    pub_DF["Publisher Description"] = "**"+pub_DF["Publisher"] + "** [:link:](" + pub_DF["pubUrl"]+")"
    del pub_DF["pubUrl"]
    pub_DF.columns = ["Publisher","Discount","Publisher Description"]
    combined_DF.columns = ["Publisher","Title","ISSN","Verified","Publisher URL","Publisher Discount"]
    combined_DF.sort_values(by=['Title','Publisher'], inplace=True, key=lambda col: col.str.lower() )
    combined_DF.dropna(subset=["Title","ISSN"],inplace=True)
    combined_DF["Status"] = combined_DF["Verified"].map(verify_map)
    return combined_DF, pub_DF


def get_openalex_journal(issn,verified):

    detail_string = ""

    if len(issn) == 8:
        issn = issn[0:4]+"-"+issn[4:]

    try:
        j_item = requests.get("https://api.openalex.org/sources/issn:"+issn).json()
        #will need to fix if adding in a third
        if verified == 0:
	        if not j_item['is_oa']:
	            detail_string += " - Title is not considered _Open Access_ and  may be eligible for discount. :arrow_right: Please check _Publisher Discount_ for specifications and see [journal homepage]("+j_item['homepage_url']+") to ensure discount applies."
	        else: 
	            detail_string += " - Title is considered _Open Access_ or _Hybrid_ and may be eligible for disount. :arrow_right: Please check _Publisher Discount_ for specifications and see [journal homepage]("+j_item['homepage_url']+") to ensure discount applies."
        elif verified == 1:
        	detail_string += " Usual publisher discount applies"
        else:
        	detail_string += " Discount does not apply to this title"


        if j_item["apc_usd"]: 
            detail_string += "\n - Usual Article Processing Charge for this title is: **"+str(j_item["apc_usd"])+"** USD"

        detail_string += "\n - More analytics for this title from [OpenAlex]("+j_item['ids']['openalex']+")"
    except:
        detail_string = "**Could not retrieve extra journal information**"
    return detail_string


def log_apc_use(ISSN_ENTRY, PUBLISHER_ENTRY, L_URL,issn="",publisher=""):
	try:
	    form_data = {
	        ISSN_ENTRY: issn,
	        PUBLISHER_ENTRY: publisher,
	    }
	    result = requests.post(L_URL,data=form_data)
	    return result
	except:
		return False
####



#### Load data using cache function
combined_DF, pub_DF = get_data(config.JOURNAL_URL,config.PUB_URL)


#### Render Page
st.image(config.IMAGE_PATH,width=200)
st.write(config.PREAMBLE)
st.markdown(":red[Search and browse by title and publisher]:")

pubSelect = st.selectbox(label="Select a publisher to narrow", index=None, options=combined_DF["Publisher"].sort_values(ascending=True).unique())


if pubSelect:
	infoshow = combined_DF[combined_DF["Publisher"] == pubSelect]
	pub_details = pub_DF[pub_DF["Publisher"] == pubSelect]["Discount"].iloc[0]
	st.info(pub_details,title="Publisher Information",icon="📕")
	if config.LOGGING:
		log_apc_use(config.ISSN_ENTRY, config.PUBLISHER_ENTRY, config.L_URL,publisher=pubSelect)

	st.write("_Select a journal title from this publisher for more information_")
	st.write("_Click in box below, then Ctrl+F / ⌘+F to search_ ")
	event = st.dataframe(infoshow[["Title","ISSN","Status"]],on_select="rerun",selection_mode="single-row",hide_index=True)
	#st.dataframe(infoshow[["Title","ISSN"]],hide_index=True)
	st.write("Total titles for this publisher: ",len(infoshow))
else:
	infoshow = combined_DF
	st.write("_Click in box below, then Ctrl+F / ⌘+F to search_ ")
	event = st.dataframe(infoshow[["Title","ISSN","Publisher","Status"]],on_select="rerun",selection_mode="single-row",hide_index=True)
	st.write("Total titles for all publishers: ",len(infoshow))

if event.selection.rows:

	j_details = {

	"Title": infoshow.iloc[event.selection.rows[0]]["Title"],
	"Status": infoshow.iloc[event.selection.rows[0]]["Status"],
	"ISSN" : infoshow.iloc[event.selection.rows[0]]["ISSN"],
	"Publisher": infoshow.iloc[event.selection.rows[0]]["Publisher"],
	"Verified": infoshow.iloc[event.selection.rows[0]]["Verified"],
	"Publisher Discount": infoshow.iloc[event.selection.rows[0]]["Publisher Discount"]
	}


	if j_details["Verified"] == 0:
		st.warning("Discount / waiver unclear, plase verify!", icon="📕")
	elif j_details["Verified"] == 1:
		st.success("APC discount details found!",icon="📕")
	elif j_details["Verified"] == 2:
		st.error("Discount/waiver does not apply to this title!",icon="📕")
	
	j_details["Additional Information"] = get_openalex_journal(j_details["ISSN"],j_details["Verified"])
	del j_details["Verified"] #comment back out for diagnostic info

	if config.LOGGING:
		log_apc_use(config.ISSN_ENTRY, config.PUBLISHER_ENTRY, config.L_URL,issn=j_details["ISSN"])



	st.table(j_details)

#with pubTab:

with st.expander("Status Description"):
	st.markdown(config.STATUS_DESCRIPTION)
with st.expander("All Publisher Details"):
	st.markdown(config.PUBLISHER_LEADIN)
	st.table(pub_DF[["Publisher Description","Discount"]])
with st.expander("More information about APCs"):
	st.markdown(config.APC_LINK)

st.write(config.HELP_MESSAGE)






