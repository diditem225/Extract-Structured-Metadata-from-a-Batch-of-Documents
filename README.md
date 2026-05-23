# Document Tagger - Extract Structured Metadata from Documents

Automatically extract structured metadata from unstructured documents using AI and validate with Pydantic.

## 🎯 Features

- ✅ **PDF files** (.pdf)
- ✅ **Text files** (.txt)
- ✅ **HTML files** (.html, .htm)
- ✅ **Batch processing** - Process entire folders
- ✅ **Pydantic validation** - Ensures data quality
- ✅ **JSON output** - Ready for databases or analytics

## 🚀 Quick Start

```bash
cd 7
pip install -r requirements.txt
python document_tagger.py
```

## 📁 How It Works

### 1. Place Documents in `documents/` Folder
```
documents/
├── article1.txt
├── article2.html
├── report.pdf
└── news.htm
```

### 2. Run the Script
```bash
python document_tagger.py
```

### 3. Get Structured Output
Creates `tagged_documents.json` with all metadata

## 📋 What It Does

Transforms unstructured documents into structured, validated metadata:

**Input**: Raw documents (PDF, TXT, HTML)  
**Process**: AI extracts metadata → Pydantic validates → JSON output  
**Output**: Clean structured data ready for databases or analytics

### Extracted Fields

- **headline**: Article title
- **journalist**: Author name
- **published_on**: Date (YYYY-MM-DD format)
- **tags**: List of relevant topics (3-5 tags)
- **category**: One of: news, opinion, feature, review
- **source_file**: Original filename

## 📋 Example Output

```
DOCUMENT TAGGER - MULTI-FORMAT SUPPORT
Supports: PDF, TXT, HTML files

Found 3 document(s)

Processing Document 1: article1.txt
   ✓ Successfully read 399 characters
✅ Successfully extracted metadata
   Headline: Breaking: New Electric Vehicle Regulations
   Journalist: Emma Rodriguez
   Published: 2025-01-15
   Category: news
   Tags: Electric Vehicles, Regulations, Sustainability

Processing Document 2: article2.html
   ✓ Successfully read 356 characters
✅ Successfully extracted metadata
   Headline: Why Remote Work is Here to Stay
   Journalist: Michael Chen
   Published: 2024-11-20
   Category: opinion
   Tags: Remote Work, Productivity, Work-Life Balance

Processing Document 3: article3.txt
   ✓ Successfully read 450 characters
✅ Successfully extracted metadata
   Headline: Inside the World of Competitive Gaming
   Journalist: Jessica Park
   Published: 2024-12-03
   Category: feature
   Tags: Esports, Gaming, Competition

SUMMARY
Total documents: 3
Successfully processed: 3
Failed: 0

✅ Structured data saved to: tagged_documents.json

SAMPLE OUTPUT
{
  "headline": "Breaking: New Electric Vehicle Regulations",
  "journalist": "Emma Rodriguez",
  "published_on": "2025-01-15",
  "tags": ["Electric Vehicles", "Regulations", "Sustainability"],
  "category": "news",
  "source_file": "article1.txt"
}
```

## 📤 JSON Output Structure

All extracted metadata is saved to `tagged_documents.json`:

```json
[
  {
    "headline": "Breaking: New Electric Vehicle Regulations",
    "journalist": "Emma Rodriguez",
    "published_on": "2025-01-15",
    "tags": ["Electric Vehicles", "Regulations", "Sustainability"],
    "category": "news",
    "source_file": "article1.txt"
  },
  {
    "headline": "Why Remote Work is Here to Stay",
    "journalist": "Michael Chen",
    "published_on": "2024-11-20",
    "tags": ["Remote Work", "Productivity", "Work-Life Balance"],
    "category": "opinion",
    "source_file": "article2.html"
  },
  {
    "headline": "Inside the World of Competitive Gaming",
    "journalist": "Jessica Park",
    "published_on": "2024-12-03",
    "tags": ["Esports", "Gaming", "Competition"],
    "category": "feature",
    "source_file": "article3.txt"
  }
]
```

**Note**: Console shows only the first document to avoid clutter. Full data is in the JSON file.

## 🎓 How It Works

### 1. Document Reading
Automatically detects file format and uses appropriate parser:
- **Text files**: Direct reading
- **HTML files**: BeautifulSoup extracts clean text (removes scripts/styles)
- **PDF files**: PyPDF2 extracts text from all pages

### 2. AI Extraction
Sends document content to Groq AI (llama-3.3-70b-versatile) with structured prompt to extract metadata fields.

### 3. Pydantic Validation
Validates extracted data:
- Date format must be YYYY-MM-DD
- Category must be: news, opinion, feature, or review
- All required fields must be present
- Rejects invalid data

### 4. JSON Export
Saves validated metadata to `tagged_documents.json` for downstream use.

## 💡 Use Cases

- **Digital Libraries**: Catalog mixed document types automatically
- **News Aggregation**: Extract metadata from articles for organization
- **Research**: Process academic papers and web articles
- **Content Management**: Auto-tag and categorize imported documents
- **Data Analytics**: Build structured datasets from unstructured sources

## 🛠️ Technical Details

### Dependencies
```
langchain-core      # LLM orchestration
langchain-groq      # Groq AI integration
pydantic           # Data validation
python-dotenv      # Environment variables
PyPDF2             # PDF parsing
beautifulsoup4     # HTML parsing
```

### Supported File Formats

| Format | Extension | Parser |
|--------|-----------|--------|
| Text | .txt | Built-in |
| HTML | .html, .htm | BeautifulSoup4 |
| PDF | .pdf | PyPDF2 |

### Environment Setup
Create `.env` file with your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## ✅ Sample Documents

The script automatically creates sample documents if the `documents/` folder is empty:
- `article1.txt` - News article about electric vehicles
- `article2.html` - Opinion piece on remote work
- `article3.txt` - Feature story on competitive gaming

Add your own documents to process them!

---

**Built with LangChain + Groq AI + Pydantic 🚀**
