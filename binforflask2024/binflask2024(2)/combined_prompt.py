# combined_prompt.py

# Base prompt from the previous `prompt_template.py`
anlysis_prompt = """Analyze this landing page based on its visual structure and user engagement. Generate a list of 5 suggestions in json, return only the json without anything else.
Output example:
{
  "suggestions": [
    {
      "element": "Headline",
      "suggestion": "Make the headline more specific to the product or service offered to better capture user interest and improve targeting."
    },
    {
      "element": "Value Proposition",
      "suggestion": "Include a more detailed description of benefits and features to clearly communicate the value proposition to visitors."
    },
    {
      "element": "Hero Image",
      "suggestion": "Replace the placeholder with an actual high-quality image or graphic that represents the product or service effectively."
    },
    {
      "element": "Call to Action (CTA)",
      "suggestion": "Make the CTA button more prominent with contrasting colors and actionable text that encourages clicks."
    },
    {
      "element": "Social Proof",
      "suggestion": "Show actual customer testimonials or case studies instead of just a rating to add authenticity and trustworthiness."
    }
  ]
}
"""

# Persona-specific prompts from the previous `ai_personas.py`
persona_prompts_small = [
    {"Marketer": "As a marketing expert, focus on conversion and customer acquisition."},
    {"Designer": "As a design expert, focus on layout, typography, and visual appeal."},
    {"SEO Specialist": "As an SEO specialist, focus on metadata, site speed, and keywords."}
]
persona_prompts_big = [
    {"Young Entrepreneur": "As a young, tech-savvy entrepreneur interested in the latest market trends and innovations, "},
    {"College Student": "As a computer science student with interests in gaming and social media, "},
    {"Freelance Graphic Designer": "As a freelance graphic designer, "},
    {"Corporate Executive": "As a busy corporate executive, "},
    {"Small Business Owner": "As a small business owner of a local café, "},
    {"Professional Blogger": "As a professional blogger, "},
    {"Travel Enthusiast": "As a travel enthusiast, "},
    {"Software Developer": "As a software developer, "},
    {"Fashion Influencer": "As a fashion influencer, "},
    {"Senior Research Scientist": "As a senior research scientist, "},
    {"Digital Nomad": "As a digital nomad who travels while working remotely, "},
    {"Art Student": "As an art student, "},
    {"Digital Marketing Expert": "As a digital marketing expert with a strong background in SEO, PPC, and social media advertising, "}
]

# Function to combine the prompts into one final prompt
def create_combined_prompt():
    combined_prompt = anlysis_prompt + " "

    for persona in persona_prompts_small:
        for title, prompt in persona.items():
            combined_prompt += f"{prompt} "

    return combined_prompt.strip()
