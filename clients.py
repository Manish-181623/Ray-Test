from transformers import pipeline

def test_translation():
    try:
        # Initialize the translation pipeline
        translator = pipeline("translation_en_to_fr", model="t5-small")
        
        # Test cases
        test_texts = [
            "Hello, how are you?",
            "I love programming python ",
            "The weather is beautiful today"
        ]
        
        print("Testing English to French translation:")
        print("-" * 40)
        
        for text in test_texts:
            translation = translator(text)[0]["translation_text"]
            print(f"\nEnglish: {text}")
            print(f"French:  {translation}")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_translation()