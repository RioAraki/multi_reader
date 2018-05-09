# Put all steps in one file

# Step 1:  Search the book name on google
from googleapiclient.discovery import build

# google api: AIzaSyCh7vVI5NtzMrIpCMUJshx5Rd855U0hXe4
# cse id: 006143628057480232827:4svfte2xdd4

# return the first url from google search
def search_ask(name):
    # build a service object for interacting with api.
    service = build("customsearch", "v1", developerKey="AIzaSyCh7vVI5NtzMrIpCMUJshx5Rd855U0hXe4")
    res = service.cse().list(
        q=name,
        cx='006143628057480232827:4svfte2xdd4',
    ).execute()

    # If no results found
    if int(res['queries']['request'][0]['totalResults']) == 0:
        print ('No result found')
        return False

    return res['items'][0]['link']

# Step 2: scrape the site and fetch the contents
def


















if __name__ == '__main__':
    pass