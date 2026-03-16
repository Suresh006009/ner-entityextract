EntityExtract – Named Entity Recognition for News

EntityExtract is a lightweight web application that extracts persons, organizations, and locations from news articles or any text input. Built with Flask and spaCy, it provides a clean, modern interface for quick entity analysis with frequency counts.

 Features

- 📝 Text input         – Paste or type any text (up to 5000 characters).
- 📁 File upload        – Upload `.txt` files for analysis.
- 🧠 Accurate NER       – Uses spaCy’s `en_core_web_sm` model, which handles lowercase names (e.g., “suresh”) without extra preprocessing.
- 📊 Tabulated results  – Entities are grouped into three cards: Persons, Organizations, Locations, each showing entity names and occurrence counts.
- 🔢 Basic statistics   – Word count, sentence count, and total unique entities.
- 🎨 Sleek dark theme   – Responsive design with animations, gradients, and example chips.
- ⚡ Fast & lightweight – Minimal dependencies, real‑time processing.

 Technologies Used

- Backend: Python, Flask
- NLP Engine: spaCy (`en_core_web_sm`)
- Frontend: HTML5, CSS3, JavaScript (ES6)
- Templating: Jinja2 (built into Flask)
- Version Control: Git



  Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
