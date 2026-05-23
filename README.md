# Document Tagger - Multi-Format Support

Extract structured metadata from **PDF, TXT, HTML** files automatically using AI.

## 🎯 What's New

Now supports multiple file formats:
- ✅ **PDF files** (.pdf)
- ✅ **Text files** (.txt)
- ✅ **HTML files** (.html, .htm)
- ✅ **Scanned reports** (via PDF)

## 🚀 Quick Start

```bash
cd 7
pip install -r requirements.txt
python document_tagger_advanced.py
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
python document_tagger_advanced.py
```

### 3. Get Structured Output
Creates `tagged_documents.json` with all metadata

## 📊 Supported Formats

| Format | Extension | Library Used |
|--------|-----------|--------------|
| Text | .txt | Built-in |
| HTML | .html, .htm | BeautifulSoup4 |
| PDF | .pdf | PyPDF2 |

## 🔧 How Each Format is Processed

### **Text Files (.txt)**
```python
def read_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()
```
- Direct reading
- No preprocessing needed

### **HTML Files (.html, .htm)**
```python
def read_html_file(filepath):
    soup = BeautifulSoup(f.read(), 'html.parser')
    # Remove scripts and styles
    # Extract clean text
    return text
```
- Parses HTML structure
- Removes scripts/styles
- Extracts clean text

### **PDF Files (.pdf)**
```python
def read_pdf_file(filepath):
    pdf_reader = PyPDF2.PdfReader(f)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
```
- Reads all pages
- Extracts text from each page
- Combines into single string

## 📋 Example Run

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

Processing Document 2: article2.html
   ✓ Successfully read 356 characters
✅ Successfully extracted metadata
   Headline: Why Remote Work is Here to Stay
   Journalist: Michael Chen
   Published: 2024-11-20
   Category: opinion

Processing Document 3: report.pdf
   ✓ Successfully read 1250 characters
✅ Successfully extracted metadata
   Headline: Q4 Financial Report
   Journalist: Sarah Johnson
   Published: 2025-01-10
   Category: news

SUMMARY
Total documents: 3
Successfully processed: 3
Failed: 0

✅ Structured data saved to: tagged_documents.json
```

## 📤 Output Format

```json
[
  {
    "headline": "Breaking: New Electric Vehicle Regulations",
    "journalist": "Emma Rodriguez",
    "published_on": "2025-01-15",
    "tags": ["Electric Vehicles", "Regulations"],
    "category": "news",
    "source_file": "article1.txt"
  },
  {
    "headline": "Why Remote Work is Here to Stay",
    "journalist": "Michael Chen",
    "published_on": "2024-11-20",
    "tags": ["Remote Work", "Productivity"],
    "category": "opinion",
    "source_file": "article2.html"
  }
]
```

## 🎓 Key Features

### 1. **Automatic Format Detection**
```python
def read_document(filepath):
    file_extension = Path(filepath).suffix.lower()
    
    if file_extension == '.txt':
        return read_text_file(filepath)
    elif file_extension == '.pdf':
        return read_pdf_file(filepath)
    elif file_extension in ['.html', '.htm']:
        return read_html_file(filepath)
```

### 2. **Batch Processing**
- Processes all files in `documents/` folder
- Handles multiple formats in one run
- Continues if one file fails

### 3. **Error Handling**
- Graceful failure for unsupported formats
- Continues processing other files
- Reports which files failed

### 4. **Validation**
- Pydantic validates all extracted data
- Ensures date format (YYYY-MM-DD)
- Checks category is valid
- Rejects invalid data

## 🔄 Workflow

```
1. Scan documents/ folder
   ↓
2. Detect file format (.txt, .pdf, .html)
   ↓
3. Read content using appropriate parser
   ↓
4. Send to AI for metadata extraction
   ↓
5. Validate with Pydantic
   ↓
6. Save to tagged_documents.json
```

## 💡 Use Cases

### **1. Digital Library**
- Process mixed document types
- Extract metadata for cataloging
- Build searchable database

### **2. News Aggregation**
- Scrape articles from websites (HTML)
- Process press releases (PDF)
- Tag and categorize automatically

### **3. Research**
- Process academic papers (PDF)
- Extract metadata from web articles (HTML)
- Organize research materials

### **4. Content Management**
- Import documents from various sources
- Auto-tag and categorize
- Build content database

## 🛠️ Customization

### Add New File Format

```python
def read_docx_file(filepath):
    """Read content from Word documents"""
    from docx import Document
    doc = Document(filepath)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Add to read_document()
elif file_extension == '.docx':
    return read_docx_file(filepath)
```

### Add New Metadata Field

```python
class ArticleMetadata(BaseModel):
    headline: str
    journalist: str
    published_on: str
    tags: list[str]
    category: str
    source_file: str
    word_count: int  # New field
```

## 📦 Dependencies

```
langchain-core      # LLM orchestration
langchain-groq      # Groq AI integration
pydantic           # Data validation
python-dotenv      # Environment variables
PyPDF2             # PDF parsing
beautifulsoup4     # HTML parsing
```

## 🎯 Advantages Over Simple Version

| Feature | Simple | Advanced |
|---------|--------|----------|
| Text files | ✅ | ✅ |
| PDF files | ❌ | ✅ |
| HTML files | ❌ | ✅ |
| Batch processing | ✅ | ✅ |
| Auto format detection | ❌ | ✅ |
| Source tracking | ❌ | ✅ |

## 🚨 Limitations

### **PDF Scanned Images**
- PyPDF2 extracts text from PDFs
- For scanned images, need OCR (Tesseract)
- Add OCR support if needed

### **Complex HTML**
- JavaScript-rendered content not supported
- Use Selenium for dynamic pages

### **Large Files**
- Very large PDFs may be slow
- Consider pagination for huge documents

## 🔮 Future Enhancements

- [ ] Add OCR for scanned PDFs
- [ ] Support Word documents (.docx)
- [ ] Support Excel files (.xlsx)
- [ ] Add image extraction
- [ ] Parallel processing for speed
- [ ] Web scraping support
- [ ] Database integration

## ✅ Testing

The script automatically creates sample documents if none exist:
- `article1.txt` - Text file
- `article2.html` - HTML file
- `article3.txt` - Another text file

Add your own documents to the `documents/` folder!

---

**Perfect for processing mixed document collections! 🚀**
