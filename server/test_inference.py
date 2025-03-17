from server.llm_inference import LLMInference

# Initialize the LLMInference class
llm_inference = LLMInference()

expiring_ingredients = "beef"
user_preferences = "chinese"
chat_history = ""

# Call the function
response = llm_inference.generate_llm_response(
    expiring_ingredients=expiring_ingredients,
    user_preferences=user_preferences,
    chat_history=chat_history
)

print(response)