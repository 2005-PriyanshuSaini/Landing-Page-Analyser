from transformers import pipeline

text_generator = None  # Lazy load GPT-3 model
fallback_generator = None  # Lazy load fallback model (e.g., GPT-Neo)

def generate_with_response_model(combined_prompt):
    global text_generator, fallback_generator
    
    if not text_generator:
        try:
            text_generator = pipeline("text-generation", model="gpt3.5")
        except Exception as e:
            print(f"Error loading GPT-3 model: {e}")
            text_generator = None
    
    if text_generator:
        try:
            tokenizer = text_generator.tokenizer
            input_tokens = tokenizer(combined_prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            result = text_generator(
                tokenizer.decode(input_tokens['input_ids'][0]),
                max_new_tokens=150,
                num_return_sequences=1, 
                pad_token_id=tokenizer.eos_token_id,
                truncation=True
            )
            return result[0]['generated_text']
        except Exception as e:
            print(f"Error generating text with GPT-3: {e}")

    if not fallback_generator:
        try:
            fallback_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")
        except Exception as e:
            print(f"Error loading fallback model (GPT-Neo): {e}")
            return None
    
    if fallback_generator:
        try:
            tokenizer = fallback_generator.tokenizer
            input_tokens = tokenizer(combined_prompt, return_tensors="pt", truncation=True, max_length=1024)
            
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

analysis_prompt = "Analyze this landing page based on its visual structure and user engagement."