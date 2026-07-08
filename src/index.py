import streamlit as st
import requests
import pandas as pd


### Fill in the values below to localize

#The sheet of publisher information that has been shared to CSV
PUB_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPFcOiXgZAo6XENgRXj3FoQ_BnbsYtAJq0QtlnhjGmpIkQjIp8eZNX6C66tcaooh1pfaUR8AULfSji/pub?gid=1143475194&single=true&output=csv"

#The sheet of journal information that has been shared to CSV
JOURNAL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPFcOiXgZAo6XENgRXj3FoQ_BnbsYtAJq0QtlnhjGmpIkQjIp8eZNX6C66tcaooh1pfaUR8AULfSji/pub?gid=0&single=true&output=csv"

#The form that is collecting the 'logged' ISSN and Publisher look-ups. Please check docs for more info
L_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe61TNpD96WMGonWeV-w0nkvQjGRCfKaB6qsFmzQQXhquFiiA/formResponse"
ISSN_ENTRY = "entry.192508866"
PUBLISHER_ENTRY = "entry.789120919"


### You can use Markdown in the following to localize to your place
PREAMBLE = """
# Article Processing Charge Agreements
Below are details about what Article Processing Charge (APC) discounts and waivers are available to members of the Brock community. More details can be found on the library site [:link:](https://brocku.ca/library/open-access/open-access-investments/).

:dart: _Title lists are built using  ULRICHs data [:link:](https://ulrichsweb.serialssolutions.com/login). Every effort has been made to ensure data is correct._

 :spiral_calendar: **Information Last Updated - July, 2, 2026.**

|Status|APC Discount/Waiver?|
|--|--|
|⛔| None available|
|❓| Please check|
|✅| Confirmed|




"""


APC_LINK  = """

Interested in learning more about APCs❓

Cantrell MH, Caldwell R, Mezick JA, Estill M, Collister LB (2026) “The system is obviously bonkers”: The APC Trap and the bind of scholarly publishing across four research intensive institutions in the U.S.. _PLOS ONE_ 21(7): e0351430. [https://doi.org/10.1371/journal.pone.0351430](https://doi.org/10.1371/journal.pone.0351430)


"""


HELP_MESSAGE = """


_Need more help:question: Contact Tim [:mailbox:](https://researchguides.library.brocku.ca/prf.php?id=2bbc13f2-7cd6-11ed-8528-0266e2e2286e)._

"""

### Other Configs
LOGGING = True #Switch to true to log lookups of publisher and issn to Google Sheet defined in L_URL
IMAGE_PATH = "images/logo.png" #Put your logo in the images folder, renamed to logo.png, defaults to 200 px wide


verify_map = {
	0 : "❓",
	1 : "✅",
	2 : "⛔",
}


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

combined_DF, pub_DF = get_data(JOURNAL_URL,PUB_URL)


#### Render Page
st.image(IMAGE_PATH,width=200)
st.write(PREAMBLE)


pubSelect = st.selectbox(label="Select a publisher to narrow", index=None, options=combined_DF["Publisher"].sort_values(ascending=True).unique())


if pubSelect:
	infoshow = combined_DF[combined_DF["Publisher"] == pubSelect]
	pub_details = pub_DF[pub_DF["Publisher"] == pubSelect]["Discount"].iloc[0]
	st.info(pub_details,title="Publisher Information",icon="📕")
	if LOGGING:
		log_apc_use(ISSN_ENTRY, PUBLISHER_ENTRY, L_URL,publisher=pubSelect)

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

	if LOGGING:
		log_apc_use(ISSN_ENTRY, PUBLISHER_ENTRY, L_URL,issn=j_details["ISSN"])



	st.table(j_details)

#with pubTab:

with st.expander("Publisher Details"):
	st.table(pub_DF[["Publisher Description","Discount"]])

with st.expander("'The system is obviously bonkers'"):
	st.markdown(APC_LINK)

st.write(HELP_MESSAGE)






