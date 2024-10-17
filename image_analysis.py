from transformers import pipeline

image_classifier = None  # Lazy load ResNet-50

def analyze_image_hf(image_url, prompt):
    global image_classifier
    if not image_classifier:
        image_classifier = pipeline("image-classification", model="microsoft/resnet-50")
    
    results = image_classifier(image_url)
    suggestions = []

    for result in results:
        suggestions.append({
            "element": result['label'],
            "suggestion": f"Consider improving the '{result['label']}' as it might need adjustments."
        })
    
    return {"suggestions": suggestions}
