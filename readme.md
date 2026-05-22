# APCEE* Platform

_\* APC Entitlement Explorer_

APCEE is a Streamlit app that will take a Google Sheet of information about Author Processing Charge (APC) waivers and discounts and present that to end users in an appealing way. You are free (and encouraged) to make a version of this platform for your institution.


## APCEE in action

This video will explain how the platform works and the steps required to recreate it.


----

📀 VIDEO DEMO 📀

----



## How to Localize

You'll need a couple of things to put together to recreate this:

- GitHub
- Google Sheets
- Command line access to run some python stuff
- Streamlit Cloud


### Github

GH Will allow you to host all of your app code so that it can be deployed to the Streamlit service.

- Fork the repository
- Modify `src/index.py` to change the messages and logos etc.

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



### Command line

You'll need to install Python, so that you can install streamlit. Open a Command line in the same folder as the forked repository.

``` bash

pip install streamlit

```


### Build Database and configure

There is a script that will grab the contents of the two sheets and build them into a database that will be used by the app. You need to add in URLs to the two CSVs from the Google Sheets step.

edit the `build_database.py` file to add

```

journalUrL = 
pubUrl = 


```

then

``` bash

python build_database.py


```

You can now modfiy the app to change the logo, change the preamble, pull in a different logo etc.

To do this, modify `src/index.py`


### Deploy to Streamlit Cloud

- Head to [Streamlit cloud]()
- New app
- Connect to Github
- find the url of your forked repository


## Updating the app

There is considerably less work involved in updating the app once you have it working:


- Make changes to your spreadsheet
- Change the _'Last Updated'_ Date message on `src/index.py` 
- run the build database script again `python build_database.py`
- Push your GitHub repository with your updates, the app will reload
