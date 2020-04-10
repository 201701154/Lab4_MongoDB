from pprint import pprint
#use pprint instead of print to clearly print output documents
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,OperationFailure
client=MongoClient("mongodb+srv://201701154:201701154@mycluster-j55ge.mongodb.net/201701154?retryWrites=true&w=majority")
db=client["201701154"]
try:
    client.admin.command('ismaster')

except ConnectionFailure:
    print('Server not available')

except OperationFailure:
    print('wrong credentials')

else:
    print('connected to database')
    casa=db.Sales.aggregate([{ "$group": { "_id": "$storeLocation", "total": { "$sum":1 } } }])


finally:
	client.close()

for docs in casa:
    print(docs)
