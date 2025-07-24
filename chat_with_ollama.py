import ollama  # This imports the Ollama Python SDK,
               # allowing you to interact with locally running LLMs like Mistral, LLaMA 3, etc.

# This defines a function that takes a prompt (your message) and sends it to the local AI model.
# It returns the model’s response.
def chat_with_model(prompt): 
    response = ollama.chat(  # Starts a chat-like conversation with the model.
        model='mistral',
        messages=[
            {'role': 'user', 'content': prompt}  # Formatted like OpenAI's Chat API.
        ]
    )
    return response['message']['content']

# This checks if the script is being run directly, not imported as a module.
# It's a Python best practice for scripts.
if __name__ == "__main__":        
    user_input = input("You: ")  # Prompts the user to type a message in the terminal.
    reply = chat_with_model(user_input)  # Sends input to the chat_with_model() function.
    print("\nAssistant:", reply)  # Prints the model's reply.
