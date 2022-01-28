import authenticate
import json


def number_borrowers(loanid):
    # this list is only for testing my function with different guid
    loanid = ['2d6acb8c-0396-4696-abab-b50c548314de', 'f522d624-db0f-47be-ab02-7e7c0220ef61',
              'f522d624-db0f-47be-ab02-7e7c0220ef61', "f522d624-db0f-47be-ab02-7e7c0220ef61",
              "f522d624-db0f-47be-ab02-7e7c0220ef61", '0d0fa588-ca95-4920-8aac-0c446ea4a7cd',
              'cafffcae - 8531 - 41a8 - bbd0 - cc03e3a66818']
    loanid =loanid[1]
    url = "https://api.elliemae.com/encompass/v1/loans/" + loanid + "/applications"
    auth = authenticate.Authenticate()

    response = auth.session.get(url)
    a = json.loads(response.text)[0]
    # print(a)
    # for r in a:
    #     print(r)
    count=0
    for r in a:

        d=a[r]
        if type(d) is dict:
            print(r)
            if "isBorrower" in d:
                if d["isBorrower"]== True:
                    count+=1
    return count

    # c = a["aUSTrackingLogs"]
    # v=len(c)
    # print(v)
    # print(c)
    # num = 1
    # print(" the borrower name is ", c["logBorrowerName"])
    # if "logCoborrowerName" in c.keys():
    #     print(" the CO-borrower name is ", c["logCoborrowerName"])
    #     num = 2
    #
    # return num


print(number_borrowers(loanid=2))
