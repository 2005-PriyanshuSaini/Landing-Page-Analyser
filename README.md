<div align="center">
  <img src="https://media.giphy.com/media/dWesBcTLavkZuG35MI/giphy.gif" width="600" height="300" alt="Landing Page Analyzer Banner"/>
</div>

# Landing Page Analyzer

A comprehensive tool for evaluating landing pages through both visual and AI-powered analysis. This project independently combines computer vision and language models to provide actionable, multi-perspective feedback for web designers and marketers.

---

## 🚀 Features

- **Visual Analysis:** Uses a pre-trained ResNet50 model to assess design and layout.
- **AI Persona Feedback:** Multiple AI personas (e.g., UX designer, marketer) offer targeted recommendations.
- **Flexible Input:** Analyze screenshots from URLs or upload your own images.
- **Streamlit UI:** Simple, interactive interface for instant results.

---

## 🛠️ Tech Stack

<div>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="Python"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/streamlit/streamlit-original.svg" height="40" alt="Streamlit"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytorch/pytorch-original.svg" height="40" alt="PyTorch"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/openai/openai-original.svg" height="40" alt="OpenAI"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/huggingface/huggingface-original.svg" height="40" alt="Hugging Face"/>
</div>

---

## 📝 Installation

git clone https://github.com/2005-PriyanshuSaini/Landing-Page-Analyser.git
cd Landing-Page-Analyser
pip install -r requirements.txt

---

## 💡 Usage

streamlit run app.py

- Choose to capture a screenshot from a URL or upload an image.
- Click **Analyze Image** to receive detailed feedback.

---

## 📂 Project Structure

- `app.py` - Main Streamlit application.
- `web_screenshot.py` - Captures webpage screenshots.
- `image_analysis.py` - Handles image analysis with Hugging Face.
- `openai_functions.py` - Manages OpenAI API calls.
- `ai_personas.py` - Persona prompt definitions.
- `prompt_template.py` - Templates for AI interactions.

---

## 🔮 Future Plans

- Add more AI personas for broader feedback.
- Batch analysis for multiple pages.
- Exportable analysis reports.
- A/B testing insights.

---

## 👤 Author

Built independently by Priyanshu Saini.

---
=======

>>>>>>> 0da2361e6356f9cab7d3c9b682eec04145e39cf4
