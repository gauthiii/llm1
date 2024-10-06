# Here’s a basic approach to modify simple.py using Cosine Similarity and sklearn's TfidfVectorizer:
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process  # Additional library for fuzzy matching (pip install fuzzywuzzy)
from responses import responses

class SimpleLLM:
    def __init__(self):
        self.responses = responses
        self.vectorizer = TfidfVectorizer()
        
        # Fit the TF-IDF vectorizer on the predefined prompts
        self.prompts = list(self.responses.keys())
        self.prompt_vectors = self.vectorizer.fit_transform(self.prompts)
    
    def preprocess_input(self, user_input):
        """
        Normalize the user input by correcting abbreviations, handling repeated characters, and standardizing common typos.
        """
        user_input = user_input.lower().strip()
        
        # Replace common abbreviations and misspellings
        replacements = {
            "u": "you",
            "r": "are",
            "whats": "what is",
            "heyy": "hey",
            "wassssup": "wassup",
            "sup": "wassup",
            "mofo": ""  # Remove any inappropriate words or slangs
        }
        for word, replacement in replacements.items():
            user_input = user_input.replace(word, replacement)
        
        # Replace repeated characters (e.g., "heyyyy" -> "hey")
        user_input = re.sub(r'(.)\1{2,}', r'\1\1', user_input)
        
        return user_input

    def extract_math_from_text(self, text):
        """
        Extract numerical values and operators from a word problem and translate them into a mathematical expression.
        This is a basic implementation and may need to be expanded for more complex word problems.
        """
        # Remove any non-numeric, non-operator characters and retain keywords for operations
        text = re.sub(r'[^0-9+\-*/=(). ]+', '', text)

        # Define keyword mapping for basic arithmetic
        keyword_map = {
            "add": "+",
            "plus": "+",
            "sum": "+",
            "subtract": "-",
            "minus": "-",
            "difference": "-",
            "times": "*",
            "multiply": "*",
            "product": "*",
            "divide": "/",
            "over": "/",
            "quotient": "/",
            "gave" : "+"
        }

        # Replace keywords in text with mathematical operators
        for keyword, operator in keyword_map.items():
            text = re.sub(r'\b' + keyword + r'\b', operator, text)

        # Use regex to capture basic arithmetic expressions
        expression = re.findall(r'[0-9+\-*/().]+', text)
        if expression:
            return expression[0]
        return None

    def solve_word_problem(self, text):
        """
        Extracts mathematical expressions from word problems and solves them.
        """
        # Extract math expression from text
        math_expression = self.extract_math_from_text(text)
        if math_expression:
            try:
                # Evaluate the math expression safely
                result = eval(math_expression, {"__builtins__": None}, {})
                return f"The answer is {result}"
            except Exception as e:
                return f"I couldn't solve the expression due to: {str(e)}"
        return None

    def get_response(self, user_input):
        # Preprocess user input to normalize it
        user_input = self.preprocess_input(user_input)

        # Check if it can be solved as a word problem first
        word_problem_response = self.solve_word_problem(user_input)
        if word_problem_response:
            return word_problem_response

        # Try to handle it as a simple math operation next
        try:
            # Evaluate any simple math expressions entered directly
            math_result = eval(user_input, {"__builtins__": None}, {})
            if isinstance(math_result, (int, float)):
                return f"The result is {math_result}"
        except:
            pass  # If eval fails, move on to matching responses
        
        # Compute the TF-IDF vector for the user input
        user_input_vector = self.vectorizer.transform([user_input])

        # Calculate cosine similarities between the user input and all predefined prompts
        similarities = cosine_similarity(user_input_vector, self.prompt_vectors).flatten()
        
        # Find the most similar prompt based on cosine similarity score
        max_similarity_index = np.argmax(similarities)
        max_similarity_score = similarities[max_similarity_index]

        # Set a lower similarity threshold to capture more variations
        if max_similarity_score >= 0.4:
            best_match = self.prompts[max_similarity_index]
            return self.responses[best_match]
        
        # Use fuzzy matching as a secondary measure
        fuzzy_match, match_score = process.extractOne(user_input, self.prompts)
        if match_score >= 75:  # Match score out of 100
            return self.responses[fuzzy_match]

        return "I’m not sure how to respond to that. Can you try asking something else?"

def main():
    print("\n***************************************************************\n")
    print("Hello! I'm programmed to answer "+str(len(responses))+" different prompts. Type 'help' to see what you can ask, or 'exit' to quit.")
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
