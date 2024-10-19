# utils.py

def get_bot_response(user_message):
    # Simple example of a bot response. Replace this with your bot logic.
    responses = {
        'hello': 'Hi there!',
        'how are you?': 'I am good, thank you!',
        'bye': 'Goodbye!',
    }
    return responses.get(user_message.lower(), "I didn't understand that.")
