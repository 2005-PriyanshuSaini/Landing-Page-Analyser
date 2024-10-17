import streamlit as st
from ai_personas import persona_prompts_small
from prompt_template import anlysis_prompt
from openai_functions import generate_with_response_model
from image_analysis import analyze_image_hf
import web_screenshot

def main():
    st.title("Landing Page Analyzer")
    st.write("Welcome to the Landing Page Analyzer. Please provide an image of a landing page for analysis.")

    method = st.radio("Choose your method to provide the image:", ('Capture Webpage Screenshot', 'Upload Your Own Screenshot'))
    image_url = None

    if method == 'Capture Webpage Screenshot':
        image_url = handle_webpage_screenshot()
    elif method == 'Upload Your Own Screenshot':
        image_url = handle_image_upload()

    if image_url and st.button("Analyze Image"):
        with st.spinner('Analyzing image...'):
            analyze_image(image_url)

def handle_webpage_screenshot():
    capture_url = st.text_input("Enter the URL to capture the webpage:")
    if capture_url:
        captured_image_path = web_screenshot.capture_web_page_image(capture_url, "screenshot_test.png")
        resized_image_path = web_screenshot.resize_image(captured_image_path)
        st.image(resized_image_path, caption='Captured Screenshot', use_column_width=True)
        image_url = web_screenshot.upload_to_imgur(resized_image_path)
        if image_url:
            st.success(f"Image uploaded successfully! URL: {image_url}")
            return image_url
        else:
            st.error("Failed to upload image to Imgur. Please try again.")
    return None

def handle_image_upload():
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image_path = "uploaded_image.png"
        web_screenshot.save_uploaded_image(uploaded_file, image_path)
        resized_image_path = web_screenshot.resize_image(image_path)
        st.image(resized_image_path, caption="Uploaded Screenshot", use_column_width=True)
        image_url = web_screenshot.upload_to_imgur(resized_image_path)
        if image_url:
            st.success(f"Image uploaded successfully! URL: {image_url}")
            return image_url
        else:
            st.error("Failed to upload image to Imgur. Please try again.")
    return None

def analyze_image(image_url):
    if not image_url:
        st.error("No valid image URL provided.")
        return

    all_persona_prompts = [f"{prompt} {anlysis_prompt}" for persona in persona_prompts_small for title, prompt in persona.items()]
    combined_prompt = " ".join(all_persona_prompts)

    image_analysis_results = analyze_image_hf(image_url, combined_prompt)
    if image_analysis_results:
        st.write("Image Analysis Suggestions:")
        st.json(image_analysis_results)
    else:
        st.error("No suggestions could be generated from the image analysis.")

    try:
        suggestions = generate_with_response_model(combined_prompt)
        if suggestions:
            st.write("Overall Analysis:")
            st.json(suggestions)
        else:
            st.error("No text suggestions could be generated.")
    except Exception as e:
        st.error(f"An error occurred while generating text suggestions: {str(e)}")

if __name__ == "__main__":
    main()
