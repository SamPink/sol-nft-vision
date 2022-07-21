# NFT Vision

This is a python application that is run through Flask using the magiceden api to collect data.

Currently this app is setup to use a static data source stored in the `data` folder through csv files.

## how to run

1. create a virtual environment (python -m venv venv)
2. activate the virtual environment (source venv/bin/activate)
3. install the dependencies (pip install -r requirements.txt)
4. flask run (python app.py)

## update / get data

Currently this is done manualy by running the get_collection.py script. This will get the data from the magiceden api and for each collection in collection.json it will create a folder in the data folder and put the data in there.

The update listings flag can be set to true to update the listings for each collection.