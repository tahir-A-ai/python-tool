from utils import ask_gemini

print("--- AI Style Rewriter ---")

while True:
    text_input = input("\n1. Enter text to rewrite (or 'exit'): ")
    if text_input.lower() == 'exit': break
    
    style_input = input("2. Enter target style/audience (e.g., 'for a 5yo', 'professional', 'pirate'): ")
    
    # Prompt Engineering: We inject both variables into the instruction
    final_prompt = f"""
    Rewrite the following text.
    Target Audience/Style: {style_input}
    
    Original Text: "{text_input}"
    """
    
    print("\nRewriting...")
    response = ask_gemini("Rewriting", final_prompt)
    print(f"\nResult:\n{response}")