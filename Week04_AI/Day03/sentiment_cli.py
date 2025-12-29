from services import analyze_sentiment

def main():
    print("--- AI Sentiment Analyzer (CLI) ---")
    print("Type 'exit' to quit.")

    while True:
        user_text = input("\n> Enter text to analyze: ")
        
        if user_text.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        if not user_text.strip():
            continue

        print("Analyzing...")
        try:
            # Reusing the same logic from services.py
            result = analyze_sentiment(user_text)
            
            # Formatting the output nicely for the terminal
            sentiment = result.get("sentiment", "UNKNOWN")
            score = result.get("score", 0.0)
            
            # Visual indicator
            icon = "🟢" if sentiment == "POSITIVE" else "🔴" if sentiment == "NEGATIVE" else "⚪"
            
            print(f"{icon} Verdict: {sentiment}")
            print(f"Confidence Score: {score}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()