from sentence_transformers import SentenceTransformer
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(override = True)

# Initialise MongoDB client
mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Load recipes from CSV
recipes_df = pd.read_csv('server/sample_data/recipes.csv')

db = client['recipes-generation']
collection = db['recipes']

# Compute embeddings and add to recipes
recipes = recipes_df.to_dict(orient='records')
for recipe in recipes:
    recipe['embedding'] = model.encode(recipe['ingredients']).tolist()

# Ingest into the collection
collection.insert_many(recipes)
