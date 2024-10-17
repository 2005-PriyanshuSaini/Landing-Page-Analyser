from transformers import pipeline

text_generator = None  # Lazy load GPT model

def generate_with_response_model(combined_prompt):
    global text_generator
    if not text_generator:
        text_generator = pipeline("text-generation", model="gpt2")  # Use local GPT-2 model
    
    result = text_generator(combined_prompt, max_length=500, num_return_sequences=1)
    return result[0]['generated_text']
