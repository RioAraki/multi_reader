from googleapiclient.discovery import build

# google api: AIzaSyCh7vVI5NtzMrIpCMUJshx5Rd855U0hXe4
# cse id: 006143628057480232827:4svfte2xdd4

# return the first url from google search
def search_ask():
    # build a service object for interacting with api.
    name = input("Enter the book name:")
    service = build("customsearch", "v1", developerKey="AIzaSyCh7vVI5NtzMrIpCMUJshx5Rd855U0hXe4")
    res = service.cse().list(
        q=name,
        cx='006143628057480232827:4svfte2xdd4',
    ).execute()

    for i in range(0,3):
        print ("{} -- Title:  {},  Link:  {}".format(i+1, res['items'][i]['title'], res['items'][i]['link']))
    print ("Here are the possible results we found, Type number 1/2/3 to choose the best fit one."
          "\nIf you don't see any correct title/ link, it means the book is not supported yet.\nFeel free to "
          "raise an issue and we would consider to add the site to our support list\n")
    num = int(input("Enter the number: "))

    while num < 1 or num > 3:
        print ("Invalid Number， please select again")
        num = int(input("Enter the number: "))
    return res['items'][num-1]['link']

def check_validity(link):
    pass


if __name__ == '__main__':
    print(search_ask())