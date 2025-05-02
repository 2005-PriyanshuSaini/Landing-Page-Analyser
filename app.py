import streamlit as st
from PIL import Image
from openai_functions import generate_with_response_model
from image_analysis import analyze_image_hf
import web_screenshot
from ai_personas import persona_prompts_small
from prompt_template import analysis_prompt
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.models import ResNet50_Weights
from torchvision import models
import asyncio

# Load a pre-trained CNN model (e.g., ResNet)
cnn_model = torchvision.models.resnet50(weights=ResNet50_Weights.DEFAULT)
cnn_model.eval()

async def main():
    st.title("Landing Page Analyzer")
    st.write("Welcome to the Landing Page Analyzer. Please provide an image of a landing page for analysis.")

    method = st.radio("Choose your method to provide the image:", ('Capture Webpage Screenshot', 'Upload Your Own Screenshot'))
    image_path = None

    if method == 'Capture Webpage Screenshot':
        image_path = await handle_webpage_screenshot()
    elif method == 'Upload Your Own Screenshot':
        image_path = await handle_image_upload()

    if image_path and st.button("Analyze Image"):
        with st.spinner('Analyzing image...'):
            await analyze_image(image_path)

async def handle_webpage_screenshot():
    capture_url = st.text_input("Enter the URL to capture the webpage:")
    if capture_url:
        captured_image_path = web_screenshot.capture_web_page_image(capture_url, "screenshot_test.png")
        if not captured_image_path:
            st.error("Error capturing screenshot.")
            return None

        resized_image_path = web_screenshot.resize_image(captured_image_path)
        st.image(resized_image_path, caption='Captured Screenshot', use_container_width=True)
        return resized_image_path
    return None

async def handle_image_upload():
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "gif", "bmp", "tiff"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Screenshot", use_container_width=True)

        # Save image locally if needed, or process directly
        image_path = "uploaded_image.png"
        image.save(image_path)

        return image_path
    return None
# Function for CNN analysis
async def cnn_visual_analysis(image_path):
    image = Image.open(image_path)
    
    # Check if the image has 4 channels (RGBA), and convert it to RGB if necessary
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        cnn_output = cnn_model(image)

    # Placeholder: Replace with your own logic to interpret CNN results
    visual_analysis_result = "CNN visual analysis completed. Layout and image quality issues detected."
    
    return visual_analysis_result


async def analyze_image(image_path):
    if not image_path:
        st.error("No valid image provided.")
        return

    try:
        # Step 1: Analyze image using CNN for visual feedback
        visual_feedback = await cnn_visual_analysis(image_path)
        st.write("Visual Feedback from CNN:")
        st.text_area("CNN Feedback", visual_feedback, height=150)

        # Step 2: Text-based analysis using personas with GPT-4
        all_persona_suggestions = []

        for persona in persona_prompts_small:
            for title, prompt in persona.items():
                combined_prompt = f"{prompt} {analysis_prompt}"
                
                # Integrate image-based analysis into the prompt
                image_analysis_results = analyze_image_hf(image_path, combined_prompt)
                
                # Request suggestions from the text-generation model (GPT-4)
                suggestions = generate_with_response_model(combined_prompt)

                if suggestions:
                    all_persona_suggestions.append({
                        "persona": title,
                        "suggestions": suggestions
                    })
                else:
                    all_persona_suggestions.append({
                        "persona": title,
                        "suggestions": "No suggestions could be generated for this persona."
                    })

        # Display persona-specific suggestions
        for persona_suggestion in all_persona_suggestions:
            st.write(f"Suggestions from {persona_suggestion['persona']}:")
            st.text_area("Persona Feedback", persona_suggestion['suggestions'], height=150)

    except Exception as e:
        st.error(f"An error occurred during the analysis: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
