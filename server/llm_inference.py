from server.prompts import GENERATION_PROMPT
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from server.search import recipe_search
import os
from dotenv import load_dotenv

class LLMInference:
    def __init__(self):
        # Load environment variables
        load_dotenv(override=True)

        # Ensure API Key is loaded
        self.OPENAI_KEY = os.getenv("OPENAI_KEY")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL")

        if not self.OPENAI_KEY or not self.OPENAI_MODEL:
            raise ValueError("Missing OpenAI API Key or Model in environment variables!")

        # Initialize the OpenAI model
        self.gpt_4o_mini = ChatOpenAI(
            api_key=self.OPENAI_KEY,
            model=self.OPENAI_MODEL,
            temperature=0  # Set temperature to 0 for deterministic outputs
        )

        # Define the pipeline (RunnableSequence)
        self.answer_chain = (
            ChatPromptTemplate.from_messages(
                [
                    ("system", GENERATION_PROMPT),
                    ("human", "{expiring_ingredients}"),
                    ("human", "{user_preferences}"),
                    ("human", "{context}"),
                    ("human", "{chat_history}"),
                ]
            )
            | self.gpt_4o_mini
            | StrOutputParser()
        )

    def generate_llm_response(self, expiring_ingredients: str = "", user_preferences: str = "", chat_history: str = ""):
        search_query = expiring_ingredients + " " + user_preferences
        
        # Handle missing search results gracefully
        context = recipe_search.search_recipes(search_query) or "No relevant recipes found."
        
        print(f"Generated Context: {context}")  # Debugging print

        try:
            input = {
                "expiring_ingredients": expiring_ingredients,
                "user_preferences": user_preferences,
                "context": context,
                "chat_history": chat_history,
            }
            response = self.answer_chain.invoke(input=input)
            return response
        except Exception as e:
            print(f"Error during LLM invocation: {e}")
            return "An error occurred while generating a response."
