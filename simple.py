import difflib
from responses import responses

class SimpleLLM:
    def __init__(self):
        self.responses = responses
    
    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # First, try to find a close match with a high cutoff
        close_match = difflib.get_close_matches(user_input, self.responses.keys(), n=1, cutoff=0.8)
        if close_match:
            return self.responses[close_match[0]]

        # If no close match, look for keywords in the user input
        user_words = set(user_input.split())
        best_match = None
        max_matches = 0

        for key in self.responses.keys():
            key_words = set(key.split())
            common_elements = user_words.intersection(key_words)
            if len(common_elements) > max_matches:
                max_matches = len(common_elements)
                best_match = key

        if best_match:
            return self.responses[best_match]

        return "I'm not sure how to respond to that. Can you try asking something else?"

def main():
    print("\n***************************************************************\n")
    print("Hello! I'm programmed to answer 120 different prompts. Type 'help' to see what you can ask, or 'exit' to quit.")
    print("\n***************************************************************\n")
    model = SimpleLLM()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Model: Goodbye!")
            break
        response = model.get_response(user_input)
        print(f"Model: {response}")

if __name__ == "__main__":
    main()
