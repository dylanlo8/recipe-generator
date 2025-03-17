from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(override = True)

mongo_uri = os.getenv("MONGODB_URI")
db_name = 'recipes-generation'
collection_name = 'recipes'
model_name = 'sentence-transformers/all-MiniLM-L6-v2'

class RecipeSearch:
    def __init__(self, mongo_uri, db_name, collection_name, model_name):
        # Initialise MongoDB client
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        # Load the model
        self.model = SentenceTransformer(model_name)

    def search_recipes(self, ingredients_query):
        # Compute the embedding for the query
        query_embedding = self.model.encode(ingredients_query).tolist()

        # Perform a vector search using the aggregate method
        pipeline = [
            {
                # Performing vector search
                '$vectorSearch': {
                    'index': 'vector_index',
                    'path': 'embedding',
                    'queryVector': query_embedding,
                    'numCandidates': 100, 
                    'limit': 10
                }
            },
            {
                # Define the fields to include in the output
                '$project': {
                    '_id' : 0,
                    'recipe_name': 1, 
                    'ingredients': 1, 
                    'directions': 1
                }
            }
        ]

        # Run the Mongo Pipeline
        search_results = list(self.collection.aggregate(pipeline))

        context = "\n".join(
            f"Recipe: {result['recipe_name']}\nIngredients: {result['ingredients']}\nDirections: {result['directions']}\n"
            for result in search_results
        ) or "No relevant recipes found."

        return context

recipe_search = RecipeSearch(mongo_uri, db_name, collection_name, model_name)


# # Example usage
if __name__ == "__main__":
    recipe_search = RecipeSearch(mongo_uri, db_name, collection_name, model_name)
    query = "chicken, garlic, onion, butter"
    search_results = recipe_search.search_recipes(query)
    for result in search_results:
        print(result)