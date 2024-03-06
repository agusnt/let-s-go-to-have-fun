# DB

Configure a docker with a [mongoDB](https://www.mongodb.com/) database to use in research.

You should create a `.env` file with the following data:

```
'''
MONGO_INITDB_ROOT_USERNAME=
MONGO_INITDB_ROOT_PASSWORD=
ME_CONFIG_BASICAUTH_USERNAME=
ME_CONFIG_BASICAUTH_PASSWORD=
ME_CONFIG_MONGODB_ADMINUSERNAME=
ME_CONFIG_MONGODB_ADMINPASSWORD=
ME_CONFIG_MONGODB_URL=mongodb://username:pass@mongo:27017/
'''
```

Deploy the database with the following command `docker-compose up -d`.
