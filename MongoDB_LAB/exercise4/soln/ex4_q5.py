from pymongo import MongoClient
from pprint import pprint
client=MongoClient("mongodb+srv://201701154:201701154@mycluster-j55ge.mongodb.net/201701154?retryWrites=true&w=majority")
db=client["201701154"]

t = list(db.Accounts.find(
            {"products" : {"$in" : ["Commodity"]}}
        ))
db.temp.drop()
db.temp.insert_many(t)


agr = [{"$lookup" : {
            "from" : "temp",
            "localField" : "accounts",
            "foreignField" : "account_id",
            "as" : "output"
        }},
        { "$match" : { "name" : "Leslie Martinez" } },
        {"$project" : {"output.account_id" : 1,"_id" : 0,"output.products":1}},
        {"$unwind" : {"path" : "$output"}}
       ]


val = list(db.Customers.aggregate(agr))

for v in val:
    pprint(v["output"]["account_id"])
    db.Transactions.remove({"account_id" : v["output"]["account_id"]})
    db.Accounts.delete_one({"account_id" : v["output"]["account_id"]})
    db.Customers.update_one(
            {},
            {"$pull" : { "accounts" : v["accounts"]}}
            )
db.temp.drop()
