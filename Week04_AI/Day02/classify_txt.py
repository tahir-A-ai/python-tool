from utils import ask_gemini

print("--- Sentiment Classifier ---")
print("I will classify text as: POSITIVE, NEGATIVE, NEUTRAL, or URGENT.")

while True:
    user_text = input("\n> Enter customer review: ")
    if user_text.lower() == 'exit': break

    final_prompt = f"""
    Analyze the sentiment of this text.
    Rules:
    1. Respond with ONLY one word.
    2. Choose from: [POSITIVE, NEGATIVE, NEUTRAL, URGENT].
    3. Do not add punctuation or explanation.
    
    Text: "{user_text}"
    """
    
    print("\nAnalyzing...")
    response = ask_gemini("Classification", final_prompt)
    print(f"\nLabel: {response}")