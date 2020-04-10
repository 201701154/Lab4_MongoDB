#Recommended to use python try-except block to perform error handling.
from pprint import pprint
#use pprint instead of print to clearly print output documents
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,OperationFailure
client=MongoClient("mongodb+srv://201701154:201701154@mycluster-j55ge.mongodb.net/201701154?retryWrites=true&w=majority")
db=client["201701154"]
mycol=db["Stock_replenish"]

try:
    client.admin.command('ismaster')

except ConnectionFailure:
    print('Server not available')

except OperationFailure:
    print('wrong credentials')

else:
    print('connected to database')
    val = db.Sales.aggregate([
                {"$unwind" : {"path" : "$items"}},
                {"$group" : {
                        "_id" : "$items.name",
                        "sales_history" : {"$push" : {"storeLocation" : "$storeLocation","quantity" : {"$multiply" : ["$items.price","$items.quantity"]}}}
                            }
                },
                #{"$out" : "stock_replenish"}
            ])
    for v in val:
        mycol.insert_one(v)

finally:
	client.close()
