from pymongo import MongoClient
from pprint import pprint
client=MongoClient("mongodb+srv://201701154:201701154@mycluster-j55ge.mongodb.net/201701154?retryWrites=true&w=majority")
db=client["201701154"]

agr = [
       {"$lookup" : {
            "from" : "Transactions",
            "localField" : "accounts",
            "foreignField" : "account_id",
            "as" : "output"
        }},
        {"$unwind" : {"path" : "$output"}},
        {"$match" : {"username":"ashley97"}},
        {"$project": {"username" : "ashley97","ans":"output.transactions.total",
                     "Code": {
                "$filter": {
                    "input": "$output.transactions",
                    "as": "s",
                    "cond": {
                        "$eq": ["$$s.transaction_code", "buy"]
                    }
                }
            }
         }
         },
        {"$unwind":{"path":"$Code"}},
        {"$project": {"_id" : "$username","fa":{"$toDecimal":"$Code.total"}}},
        {"$group": {"_id" : "$username","final":{"$sum":"$fa"}}}
       ]

val = db.Customers.aggregate(agr)

for v in val:
    pprint(v)
