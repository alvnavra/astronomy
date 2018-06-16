# astronomy

----------
Install Mongo
----------
sudo apt install mongodb # Servidor mongo
sudo apt install mongodb-client #Cliente mongo
sudo apt install mongo-tools #Herramientas mongo (mongodump, mongorestore)
------------
MongoDump & Mongo Restore
------------
mongodump -h ds119060.mlab.com:19060 -d astronomy -u alvnavra -p temporal1 -o .
mongorestore --db astronomy --dir astronomy/
------------
Start Mongo Manually
-------------
cd /etc
sudo mongod --config mongodb.cnf &
cerrar terminal
mongo
