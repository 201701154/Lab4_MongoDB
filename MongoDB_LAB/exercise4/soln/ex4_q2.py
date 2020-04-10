from pymongo import MongoClient
from pprint import pprint
client=MongoClient("mongodb+srv://201701154:201701154@mycluster-j55ge.mongodb.net/201701154?retryWrites=true&w=majority")
db=client["201701154"]

agr = [
       {"$lookup" : {
            "from" : "Accounts",
            "localField" : "accounts",
            "foreignField" : "account_id",
            "as" : "output"
        }},
       {"$unwind":"$output"},
        {"$match":{"output.products":"Commodity"}},
        {"$group":{"_id": "$username","avgAmount":  {"$avg": "$output.limit"}}}
       ]

val = db.Customers.aggregate(agr)

for v in val:
    pprint(v)
