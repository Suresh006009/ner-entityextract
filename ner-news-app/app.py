import spacy
import webbrowser
from flask import Flask, request, jsonify, render_template
from threading import Timer

# Load the spaCy model (download first: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def extract_entities(text):
    """Extract PERSON, ORG, and GPE entities using spaCy."""
    doc = nlp(text)
    persons, orgs, locs = {}, {}, {}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            persons[ent.text] = persons.get(ent.text, 0) + 1
        elif ent.label_ == "ORG":
            orgs[ent.text] = orgs.get(ent.text, 0) + 1
        elif ent.label_ == "GPE":          # geopolitical entity = location
            locs[ent.text] = locs.get(ent.text, 0) + 1

    # Convert to sorted lists (most frequent first)
    persons = [{"name": k, "count": v} for k, v in sorted(persons.items(), key=lambda x: x[1], reverse=True)]
    orgs    = [{"name": k, "count": v} for k, v in sorted(orgs.items(), key=lambda x: x[1], reverse=True)]
    locs    = [{"name": k, "count": v} for k, v in sorted(locs.items(), key=lambda x: x[1], reverse=True)]
    return persons, orgs, locs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get input (either file or text field)
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        text = file.read().decode('utf-8')
    else:
        text = request.form.get('text', '').strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Basic stats using spaCy
    doc = nlp(text)
    word_count = len([token for token in doc if not token.is_punct and not token.is_space])
    sentence_count = len(list(doc.sents))

    # Entity extraction
    persons, orgs, locs = extract_entities(text)

    return jsonify({
        "persons": persons,
        "organizations": orgs,
        "locations": locs,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "text": text
    })

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)