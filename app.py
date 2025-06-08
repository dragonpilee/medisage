from flask import Flask, request, render_template, jsonify
import markdown
from lmstudio_client import GemmaClient

app = Flask(__name__)
# Initialize Gemma client with default LM Studio URL
client = GemmaClient(base_url="http://localhost:1234")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    user_input = request.json.get("input")
    
    # Format the prompt for Gemma to generate a structured patient-friendly summary
    prompt = f"""You are a professional pharmacist. Please provide a clear, patient-friendly summary of the drug: {user_input}

Structure the response in this format:

1. Drug Summary Header
   - Start with "Drug Name Summary"
   - Add "A Professional Pharmacist's Overview" as a subtitle

2. Key Information Sections
   - Generic Name & Common Names
   - Common Brand Names
   - Primary Uses & Key Indications
   - Important Safety Information
   - Common Dosage Information

Format each section clearly with bullet points and proper indentation. Use a friendly, professional tone suitable for patient education. Keep the response concise but comprehensive (about 200-300 words)."""

    try:
        response = client.generate(prompt)
        # Clean up the response to ensure proper markdown formatting
        cleaned_response = response.strip()
        # Add extra newlines between sections for better readability
        cleaned_response = cleaned_response.replace('\n\n', '\n\n\n')
        html_response = markdown.markdown(cleaned_response)
        return jsonify({"response": html_response})
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        return jsonify({"response": error_msg}), 500
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        return jsonify({"response": error_msg}), 500

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', debug=True)
    except Exception as e:
        print(f"Error starting Flask app: {str(e)}")