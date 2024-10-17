from transformers import pipeline

text_generator = None  # Lazy load GPT-2 model
fallback_generator = None  # Lazy load fallback model (e.g., GPT-Neo)

def generate_with_response_model(persona_prompt):
    global text_generator, fallback_generator
    
    # Try with GPT-2 model first
    if not text_generator:
        try:
            text_generator = pipeline("text-generation", model="gpt2")
        except Exception as e:
            print(f"Error loading GPT-2 model: {e}")
            text_generator = None
    
    if text_generator:
        try:
            # Tokenize the input to ensure it doesn't exceed the model's max length
            tokenizer = text_generator.tokenizer
            input_tokens = tokenizer(persona_prompt, return_tensors="pt", truncation=True, max_length=2048)
            
            # Generate new text
            result = text_generator(
                tokenizer.decode(input_tokens['input_ids'][0]),
                max_new_tokens=50,
                num_return_sequences=1, 
                pad_token_id=tokenizer.eos_token_id,
                truncation=True
            )
            return result[0]['generated_text']
        except Exception as e:
            print(f"Error generating text with GPT-2: {e}")

    # If GPT-2 fails, fallback to another model (e.g., GPT-Neo)
    if not fallback_generator:
        try:
            fallback_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")
        except Exception as e:
            print(f"Error loading fallback model (GPT-Neo): {e}")
            return None
    
    if fallback_generator:
        try:
            # Tokenize and generate text with fallback model
            tokenizer = fallback_generator.tokenizer
            input_tokens = tokenizer(persona_prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            result = fallback_generator(
                tokenizer.decode(input_tokens['input_ids'][0]),
                max_new_tokens=50,
                num_return_sequences=1, 
                pad_token_id=tokenizer.eos_token_id,
                truncation=True
            )
            return result[0]['generated_text']
        except Exception as e:
            print(f"Error generating text with fallback model: {e}")
            return None
