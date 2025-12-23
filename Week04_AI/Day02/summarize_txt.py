from utils import ask_gemini

print("--- AI Summarizer Tool ---")
print("Enter a paragraph to summarize (or type 'exit' to quit).")

while True:
    user_text = input("\n> Paste text here: ")
    
    if user_text.lower() == 'exit':
        break
    
    if not user_text.strip():
        continue

    # Prompt Engineering: We enforce a specific constraint (One sentence)
    final_prompt = f"""
    You are an expert editor. 
    Summarize the following text into exactly ONE punchy sentence.
    
    Text: "{user_text}"
    """
    
    print("\nProcessing...")
    response = ask_gemini("Summarization", final_prompt)
    print(f"\nSummary: {response}")