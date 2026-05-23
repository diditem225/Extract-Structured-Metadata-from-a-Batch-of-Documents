# Code Explanation - Document Tagger

## 📚 Simple Breakdown

### What This Code Does
Takes messy article text → Extracts clean metadata → Saves as JSON

---

## 🔧 Main Components

### 1. **ArticleMetadata Class** (Lines 11-36)
```python
class ArticleMetadata(BaseModel):
    headline: str
    journalist: str
    published_on: str
    tags: list[str]
    category: str
```

**What it does:** Defines what data we want to extract  
**Why it matters:** Pydantic validates the data automatically

**Validators:**
- `validate_date()` - Checks date is YYYY-MM-DD format
- `validate_category()` - Checks category is: news, opinion, feature, or review

---

### 2. **setup_llm_chain()** (Lines 39-62)
```python
def setup_llm_chain():
    llm = ChatGroq(...)
    parser = JsonOutputParser(...)
    prompt = PromptTemplate(...)
    return prompt | llm | parser
```

**What it does:** Creates the AI extraction pipeline  
**Steps:**
1. LLM - The AI that reads the text
2. Parser - Converts AI response to JSON
3. Prompt - Instructions for the AI
4. Chain - Connects everything with `|`

---

### 3. **process_document()** (Lines 65-89)
```python
def process_document(article_text, chain, doc_number):
    metadata = chain.invoke({"article_text": article_text})
    return metadata
```

**What it does:** Processes one article  
**Steps:**
1. Send article to AI
2. Get back structured metadata
3. Print results
4. Return metadata or None if failed

---

### 4. **Helper Functions** (Lines 92-122)

**save_to_json()** - Saves data to file  
**print_summary()** - Shows statistics  
**print_sample_output()** - Displays example output

---

### 5. **main()** (Lines 161-183)
```python
def main():
    chain = setup_llm_chain()
    
    for article in articles:
        result = process_document(article, chain, idx)
        structured_data.append(result)
    
    save_to_json(structured_data)
```

**What it does:** Runs the whole process  
**Steps:**
1. Setup AI chain
2. Loop through articles
3. Extract metadata from each
4. Save all results to JSON

---

## 🔄 Flow Diagram

```
Article Text
    ↓
setup_llm_chain()
    ↓
process_document()
    ↓
AI Extraction
    ↓
Pydantic Validation
    ↓
Structured JSON
    ↓
save_to_json()
    ↓
tagged_documents.json
```

---

## 💡 Key Concepts

### 1. **Pydantic Model**
- Defines structure
- Validates data types
- Custom validation rules

### 2. **LangChain Chain**
```python
prompt | llm | parser
```
- `prompt` - Instructions
- `llm` - AI processing
- `parser` - JSON conversion

### 3. **Error Handling**
```python
try:
    metadata = chain.invoke(...)
except Exception as error:
    print(f"Failed: {error}")
```
- Continues if one document fails
- Tracks errors
- Shows which documents succeeded

---

## 📊 Example Flow

### Input:
```
Breaking: New Electric Vehicle Regulations
By Emma Rodriguez, published January 15, 2025
The government today unveiled...
```

### Processing:
1. **setup_llm_chain()** - Creates AI pipeline
2. **process_document()** - Sends to AI
3. **AI extracts** - Finds headline, journalist, date, etc.
4. **Pydantic validates** - Checks date format, category
5. **Returns JSON** - Clean structured data

### Output:
```json
{
  "headline": "Breaking: New Electric Vehicle Regulations",
  "journalist": "Emma Rodriguez",
  "published_on": "2025-01-15",
  "tags": ["Electric Vehicles", "Regulations"],
  "category": "news"
}
```

---

## 🎯 Why Each Part Matters

| Component | Purpose | Benefit |
|-----------|---------|---------|
| Pydantic Model | Define structure | Automatic validation |
| Validators | Check data quality | Catch errors early |
| LLM Chain | Extract metadata | Automated processing |
| Error Handling | Handle failures | Robust system |
| Functions | Organize code | Easy to understand |
| Comments | Explain logic | Maintainable code |

---

## 🔑 Key Improvements Made

### Before:
- All code in one block
- Hard to understand flow
- No function separation
- Minimal comments

### After:
- ✅ Separated into clear functions
- ✅ Each function has one job
- ✅ Docstrings explain purpose
- ✅ Better variable names
- ✅ Updated to Pydantic V2 (`@field_validator`)
- ✅ Main function orchestrates everything

---

## 📝 Function Summary

| Function | Input | Output | Purpose |
|----------|-------|--------|---------|
| `setup_llm_chain()` | None | Chain | Creates AI pipeline |
| `process_document()` | Article text | Metadata dict | Extracts metadata |
| `save_to_json()` | Data list | File | Saves to JSON |
| `print_summary()` | Stats | Console output | Shows results |
| `main()` | None | None | Runs everything |

---

## 🚀 Running the Code

```bash
python document_tagger.py
```

**What happens:**
1. Loads 4 sample articles
2. Extracts metadata from each
3. Validates all data
4. Saves to `tagged_documents.json`
5. Prints summary and sample

**Output:**
- Console: Progress and results
- File: `tagged_documents.json` with all metadata

---

## 💪 Strengths

1. **Modular** - Each function does one thing
2. **Documented** - Comments explain everything
3. **Validated** - Pydantic ensures quality
4. **Robust** - Handles errors gracefully
5. **Scalable** - Easy to add more documents
6. **Maintainable** - Clear structure

Perfect for understanding and extending! 🎉
