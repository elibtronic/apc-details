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
Below are details about what Article Processing Charge (APC) discounts and waivers are available to members of the Brock community. More details can be found on the library site [:link:](https://brocku.ca/library/open-access/open-access-investments/). Title lists are built using  ULRICHs data [:link:](https://ulrichsweb.serialssolutions.com/login). Every effort has been made to ensure data is correct.

 :spiral_calendar: **Information Last Updated - July 13, 2026.**


"""


STATUS_DESCRIPTION = """

|Status|APC Discount/Waiver?|
|--|--|
|⛔| None available|
|❓| Please check|
|✅| Confirmed|


"""

PUBLISHER_LEADIN = """

Exact discount / waiver details are outlined for all publishers


"""


APC_LINK  = """

Interested in learning more about APCs❓

Cantrell MH, Caldwell R, Mezick JA, Estill M, Collister LB (2026) “The system is obviously bonkers”: The APC Trap and the bind of scholarly publishing across four research intensive institutions in the U.S.. _PLOS ONE_ 21(7): e0351430. [https://doi.org/10.1371/journal.pone.0351430](https://doi.org/10.1371/journal.pone.0351430)


"""


HELP_MESSAGE = """


_Need more help:question: Contact Tim [:mailbox:](https://researchguides.library.brocku.ca/prf.php?id=2bbc13f2-7cd6-11ed-8528-0266e2e2286e)._

"""

### Other Configs
LOGGING = False #Switch to true to log lookups of publisher and issn to Google Sheet defined in L_URL
IMAGE_PATH = "images/logo.png" #Put your logo in the images folder, renamed to logo.png, defaults to 200 px wide
