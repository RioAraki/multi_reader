import pprint # TODO: Understand what does pprint do
from googleapiclient.discovery import build

# google api: AIzaSyCh7vVI5NtzMrIpCMUJshx5Rd855U0hXe4
# cse id: 006143628057480232827:4svfte2xdd4

# return the first url from google search
def search():
    # build a service object for interacting with api.

    service = build("customsearch", "v1", developerKey="AIzaSyCh7vVI5NtzMrIpCMUJshx5Rd855U0hXe4")
    res = service.cse().list(
        q='哈利波特与魔法石',
        cx='006143628057480232827:4svfte2xdd4',
    ).execute()

    return res['items'][0]['link']

if __name__ == '__main__':
    print (search())