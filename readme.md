# APCEE* Platform

_\* APC Entitlement Explorer_

APCEE is a Streamlit app that will take a Google Sheet of information about Author Processing Charge (APC) waivers and discounts and present that to end users in an appealing way. You are free (and encouraged) to make a version of this platform for your institution.

The design philsophy for this platform is very much inspiried by Collection Builder, particularly [CB-Sheets](https://collectionbuilder.github.io/sheets/). You can run the whole thing without installing anythin on you local machine. Data goes in a Google Sheet, the app is deployed to Streamlit Cloud. Easy, peasy.


## APCEE in action

This video will explain how the platform works and the steps required to recreate it.


----

📀 VIDEO DEMO 📀

----



## Setting up your own

You'll need a couple of things to put together to recreate this:

- GitHub
- Google Sheets
- Command line access to run some python stuff
- Streamlit Cloud


### Github

GH Will allow you to host all of your app code so that it can be deployed to the Streamlit service.

- Fork the repository
- Modify `src/index.py` to change the few variables at the top of the file.

### Google Sheets

- Make a new sheet with two tabs:
	- ```journalInfo```
		- with columns ```Publisher, Journal_Title, ISSN```
	- ```publisherIno```
		- with columns ```Publisher, pubUrl, pubDiscount```

Fill in with appropriate data, the two pictures following will help with how the data is supposed to look


_journalInfo tab is the invidual journal details_

---
📸

----

_publisherInfo tab is where the publisher details go_

----
📸

----

**Publish to the web** each of the tabs as CSV files an make note of the URLs. The script in the next step will create an sqlite database by combining these two tabs together. Please note, column names need to be exactly as specified.


### Deploy to Streamlit Cloud

- Head to [Streamlit cloud]()
- New app
- Connect to Github
- find the url of your forked repository


## Tweak it more?

You can do everything you need to do run an instance of this without installing anything and just by visiting a few sites and setting up accounts. You can of course clone the repository, install steamlit and modfiy things even more.

### Setting it up locally
