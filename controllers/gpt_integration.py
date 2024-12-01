# gpt_integration.py

import os
import openai
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def improve_text(text, date, manager_name, force_name, location):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Adjust the model as needed
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant specializing in creating text in a military style, tailored specifically for the IDF. "
                        "Your task is to improve the text, making it more professional and impactful, and to organize it into four sections according to the following military structure:\n\n"
                        "1. Introduction ('הקדמה'):\n"
                        "   - Provide the following details in **2 lines**:\n"
                        f"     - Name of the force: {force_name}\n"
                        f"     - Date: {date}\n"
                        f"     - Manager: {manager_name}\n"
                        f"     - Location: {location}\n\n"
                        "2. Exercise 1 ('תרגיל 1'):\n"
                        "   - Limit to **7 lines**.\n"
                        "   - Three paragraphs:\n"
                        "     - Paragraph one: Describe the events in chronological order, not in a list.\n"
                        "     - Paragraph two: What the force did well.\n"
                        "     - Paragraph three: Where the force needs to improve.\n\n"
                        "3. Exercise 2 ('תרגיל 2'):\n"
                        "   - Limit to **7 lines**.\n"
                        "   - Three paragraphs, same structure as Exercise 1.\n\n"
                        "4. Summary ('סיכום'):\n"
                        "   - Limit to **5 lines**.\n"
                        "   - A conclusion of the exercises, highlighting the critical disadvantages of the force (if any) and where the force did well.\n"
                        "   - The summary should maintain a positive tone.\n\n"
                        "Guidelines:\n"
                        "- Replace any instances of 'Scenario' ('תרחיש') with 'Exercise' ('תרגיל').\n"
                        "- Describe events in chronological order, avoiding division into sub-events.\n"
                        "- Ensure the entire output is well-organized and professional.\n"
                        "- Write exclusively in Hebrew, adhering to military jargon and style appropriate for the IDF.\n"
                        "- Each section must start with its title on a new line, without any additional formatting or symbols.\n"
                        "- Maintain a formal and authoritative tone suitable for IDF documentation.\n"
                        "- **Strictly adhere to the specified line limits for each section.**"
                    )
                },
                {
                    "role": "user",
                    "content": f"Please improve this text and divide it into four parts as instructed: {text}"
                }
            ],
            temperature=0.7
        )
        raw_text = response.choices[0].message['content'].strip()
        print("Raw LLM response:\n", raw_text)  # For debugging

        return raw_text

    except Exception as e:
        print(f"Error occurred while communicating with LLM: {e}")
        return ""

def parse_to_sections(text):
    """
    Splits the text into a dictionary with the updated sections.
    """
    # Remove unwanted formatting characters
    text = text.replace('**', '').replace('*', '').strip()

    # Define default empty sections
    sections = {"Introduction": "", "Exercise 1": "", "Exercise 2": "", "Summary": ""}

    # Define the possible section names in both English and Hebrew
    section_names = {
        "Introduction": ["הקדמה", "מבוא", "Introduction"],
        "Exercise 1": ["תרגיל 1", "Exercise 1"],
        "Exercise 2": ["תרגיל 2", "Exercise 2"],
        "Summary": ["סיכום", "Summary"]
    }

    # Prepare regex patterns for each section
    patterns = {}
    for section, names in section_names.items():
        # Create a regex pattern that matches any of the names
        name_pattern = r'|'.join(re.escape(name) for name in names)
        # Pattern to match the section heading
        patterns[section] = r'^\s*(%s)[^\n]*\n(.*?)(?=(^\s*(%s)[^\n]*\n|\Z))' % (
            name_pattern,
            '|'.join(re.escape(n) for n in sum(section_names.values(), []))
        )

    # Preprocess the text to ensure consistent line breaks
    text = text.replace('\r\n', '\n')

    # Initialize the sections dictionary
    extracted_sections = {}

    for section, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        if match:
            content = match.group(2).strip()
            # Remove '#' and '*' from content
            content = content.replace('#', '').replace('*', '')
            extracted_sections[section] = content
        else:
            print(f"Warning: Could not find section '{section}' in the text. It may be missing or formatted differently.")
            extracted_sections[section] = ''

    return extracted_sections
