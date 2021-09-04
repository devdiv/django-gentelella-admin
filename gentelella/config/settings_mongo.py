import pymongo

MONGOHOST ='127.0.0.1'
MONGOPOST = 27017
DATABASE = 'Gentelella'
DBCONNECT = pymongo.MongoClient(host=MONGOHOST,port=MONGOPOST).get_database(DATABASE)