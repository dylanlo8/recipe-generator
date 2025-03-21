from flask import Flask, render_template, request
from server.llm_inference import LLMInference

app = Flask(__name__)
llm_inference = LLMInference()

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        expiring_ingredients = request.form.get('ingredients')
        user_preferences = request.form.get('preferences')
        chat_history = request.form.get('chat_history', '')
        
        response = llm_inference.generate_llm_response(
            expiring_ingredients=expiring_ingredients,
            user_preferences=user_preferences,
            chat_history=chat_history
        )
    
    return render_template('index.html',  response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)