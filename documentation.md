Backend flask application using postgresql.

After installing packages, to use flask session object for cookies, do the following:

1. Create a .env file in the root directory
2. Create an enviromental variable and set it equal to anything you want. You can also generate a key by running the following in the ubuntu terminal. Set the results to your variable. 

```
python -c 'import os; print(os.urandom(16))'
```
3. In the following line add the variable name like so:

```
app.secret_key= os.getenv('YOUR ENVIROMENT VARIABLE GOES HERE')
```

Assuming postgresql is installed and ready to use, to start working on project:

1. Login and start postgresql server in one ubuntu terminal 

Note: postgresql is a database server seperate from the flask application server. When starting the database locally, you can start it from any root user in the ubuntu terminal. It doesn't need to be at the root of the projects directory but that is okay too.

```
sudo service postgresql start
psql -U username -d database_name
```
Leave postgres terminal running

2. Start the flask application in another ubuntu terminal in the project root directory

NOTE: MAKE SURE YOU ARE IN PIPENV SHELL when you run python app.py. Being in the shell will make the connection from the database to the api possible. If you are not in the shell, flask won't be able to connect to the postgresql database

```
pipenv shell
python app.py
```

To successfully seed the data when importing all the modules, running the regular 
```
python seed/species.py
``` 

command will throw a "No module named config" error. To avoid this run the seed files in the seed folder using the following command: 

```
python -m seed.species # to seed species data
or 
python -m seed.classifications # to seed classification data 

#etc
```

# Marshmallow

Note: When creating a new schema for a model and a nested model is used, to avoid import issues pass the name of the schema as a string and add it to the __init__.py file in the marshmallow_schema folder


# Building a model

1. Build the model 
2. Seed the database
3. Create Marshmallow schema for model
4. Test marshmallow serialized data in a route

# Building Routes
When building protected routes, makes sure to add an endpoint (api.add_resource(Resource, '/resource', endpoint='resource'))and add that name as a string in the protected_routes array that is in the authenticate.py file in utils folder

### Creating Routes
when creating a new route script/file, it needs to be added to the routes.py file to establish the connection. All routes are being access through the routes.py file.

## POSTGRES
To reset table primary key to 1:

```
TRUNCATE TABLE table_name RESTART IDENTITY;
```