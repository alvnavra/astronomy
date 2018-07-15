# astronomy

----------
Install Mongo
----------
sudo apt install mongodb # Mongo Server<br/>
sudo apt install mongodb-client #Mongo Client<br/>
sudo apt install mongo-tools #Ubuntu's Mongo Tools (mongodump, mongorestore)

MongoDump & Mongo Restore
------------
mongodump -h ds119060.mlab.com:19060 -d astronomy -u <user> -p <path> -o /tmp/dumps
mongorestore --db astronomy --dir astronomy/

MongoRestore of one Collection
------------------------------
mongorestore --host <host destination of restore> --port <port> --username <user> --password <temporal> --db <database> --collection <collection to restore> <location of dumps> ex: ./dumps/mydb/mycollection.bson

Start Mongo Manually
-------------
cd /etc
sudo mongod --config mongodb.cnf &
cerrar terminal
mongo
