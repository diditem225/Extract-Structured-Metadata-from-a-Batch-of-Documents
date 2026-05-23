from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field, field_validator
from langchain_groq import ChatGroq
from datetime import datetime
from dotenv import load_dotenv
import json
import os
from pathlib import Path

load_dotenv()


class ArticleMetadata(BaseModel):
    """
    Defines the structure for article metadata.
    Each field has validation rules to ensure data quality.
    """
    headline: str = Field(..., description="Main headline or title of the article")
    journalist: str = Field(..., description="Name of the journalist or writer")
    published_on: str = Field(..., description="Publication date in YYYY-MM-DD format")
    tags: list[str] = Field(..., description="List of relevant tags or topics (3-5 tags)")
    category: str = Field(..., description="Article category: news, opinion, feature, or review")
    source_file: str = Field(..., description="Original filename")
    
    @field_validator('published_on')
    @classmethod
    def validate_date(cls, value):
        """Ensures date is in correct format (YYYY-MM-DD)"""
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, value):
        """Ensures category is one of the allowed values"""
        allowed_categories = ['news', 'opinion', 'feature', 'review']
        if value.lower() not in allowed_categories:
            raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        return value.lower()


def read_text_file(filepath):
    """Read content from a .txt file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return None


def read_pdf_file(filepath):
    """Read content from a PDF file"""
    try:
        import PyPDF2
        with open(filepath, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except ImportError:
        print("PyPDF2 not installed. Install with: pip install PyPDF2")
        return None
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


def read_html_file(filepath):
    """Read content from an HTML file"""
    try:
        from bs4 import BeautifulSoup
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            # Get text
            text = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
    except ImportError:
        print("BeautifulSoup not installed. Install with: pip install beautifulsoup4")
        return None
    except Exception as e:
        print(f"Error reading HTML: {e}")
        return None


def read_document(filepath):
    """
    Read document content based on file extension.
    Supports: .txt, .pdf, .html, .htm
    """
    file_extension = Path(filepath).suffix.lower()
    
    if file_extension == '.txt':
        return read_text_file(filepath)
    elif file_extension == '.pdf':
        return read_pdf_file(filepath)
    elif file_extension in ['.html', '.htm']:
        return read_html_file(filepath)
    else:
        print(f"Unsupported file type: {file_extension}")
        return None


def setup_llm_chain():
    """
    Sets up the LLM chain for metadata extraction.
    Returns a chain that takes article text and returns structured metadata.
    """
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    parser = JsonOutputParser(pydantic_object=ArticleMetadata)
    
    prompt = PromptTemplate(
        template="""You are a document metadata extractor. Extract the following information from the article text:

- headline: The main title
- journalist: The author's name
- published_on: Date in YYYY-MM-DD format
- tags: List of relevant topics (3-5 tags)
- category: One of: news, opinion, feature, review
- source_file: The filename provided

Return ONLY valid JSON matching this schema:
{format_instructions}

Source file: {source_file}

Article text:
{article_text}
""",
        input_variables=["article_text", "source_file"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    return prompt | llm | parser


def process_document(filepath, chain, doc_number):
    """
    Process a single document file and extract metadata.
    
    Args:
        filepath: Path to the document file
        chain: The LLM chain for extraction
        doc_number: Document number for logging
    
    Returns:
        dict: Extracted metadata or None if failed
    """
    filename = os.path.basename(filepath)
    print(f"Processing Document {doc_number}: {filename}")
    
    # Read document content
    content = read_document(filepath)
    if not content:
        print(f"❌ Failed to read document")
        print()
        return None
    
    print(f"   ✓ Successfully read {len(content)} characters")
    
    # Extract metadata
    try:
        metadata = chain.invoke({
            "article_text": content,
            "source_file": filename
        })
        
        print(f"✅ Successfully extracted metadata")
        print(f"   Headline: {metadata['headline']}")
        print(f"   Journalist: {metadata['journalist']}")
        print(f"   Published: {metadata['published_on']}")
        print(f"   Category: {metadata['category']}")
        print(f"   Tags: {', '.join(metadata['tags'])}")
        print()
        
        return metadata
        
    except Exception as error:
        print(f"❌ Failed to extract metadata")
        print(f"   Error: {str(error)}")
        print()
        return None


def find_documents(directory="documents"):
    """
    Find all supported document files in a directory.
    Supports: .txt, .pdf, .html, .htm
    """
    supported_extensions = ['.txt', '.pdf', '.html', '.htm']
    documents = []
    
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found. Creating sample documents...")
        return None
    
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        if os.path.isfile(filepath):
            ext = Path(filepath).suffix.lower()
            if ext in supported_extensions:
                documents.append(filepath)
    
    return documents


def save_to_json(data, filename="tagged_documents.json"):
    """Save structured data to JSON file"""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
    print(f"✅ Structured data saved to: {filename}")


def print_summary(total, successful, failed):
    """Print processing summary"""
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total documents: {total}")
    print(f"Successfully processed: {successful}")
    print(f"Failed: {failed}")
    print()


def print_sample_output(data):
    """Print a sample of the extracted data"""
    print("=" * 80)
    print("SAMPLE OUTPUT")
    print("=" * 80)
    if data:
        print(json.dumps(data[0], indent=2))
    print()


def create_sample_documents():
    """Create sample documents in different formats for testing"""
    os.makedirs("documents", exist_ok=True)
    
    # Sample 1: Text file
    with open("documents/article1.txt", 'w') as f:
        f.write("""Breaking: New Electric Vehicle Regulations Announced

By Emma Rodriguez, published January 15, 2025

The government today unveiled comprehensive new regulations for electric vehicles, 
focusing on battery safety standards and charging infrastructure requirements. 
Industry experts predict this will accelerate the transition to sustainable transportation.
The new rules will take effect in Q3 2025.""")
    
    # Sample 2: HTML file
    with open("documents/article2.html", 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>Remote Work Opinion</title></head>
<body>
    <h1>Opinion: Why Remote Work is Here to Stay</h1>
    <p>Written by Michael Chen on 2024-11-20</p>
    <p>Despite corporate pushback, remote work has fundamentally changed how we think about 
    productivity and work-life balance. This opinion piece explores why companies that 
    resist flexible work arrangements may struggle to attract top talent in the coming years.</p>
</body>
</html>""")
    
    # Sample 3: Another text file
    with open("documents/article3.txt", 'w') as f:
        f.write("""Feature Story: Inside the World of Competitive Gaming

A deep dive by Jessica Park, December 3, 2024

From basement hobby to billion-dollar industry, esports has transformed entertainment. 
This feature explores the lives of professional gamers, the psychology of competition, 
and the future of digital sports. Interviews with top players reveal the dedication 
required to compete at the highest level.""")
    
    print("✅ Created sample documents in 'documents/' folder")
    print()


def main():
    """Main function to process all documents"""
    
    print("=" * 80)
    print("DOCUMENT TAGGER - MULTI-FORMAT SUPPORT")
    print("Supports: PDF, TXT, HTML files")
    print("=" * 80)
    print()
    
    # Find documents
    documents = find_documents("documents")
    
    if documents is None:
        create_sample_documents()
        documents = find_documents("documents")
    
    if not documents:
        print("No documents found in 'documents/' folder")
        print("Supported formats: .txt, .pdf, .html, .htm")
        return
    
    print(f"Found {len(documents)} document(s)")
    print()
    
    # Setup chain
    chain = setup_llm_chain()
    
    # Process documents
    structured_data = []
    
    for idx, filepath in enumerate(documents, start=1):
        result = process_document(filepath, chain, idx)
        if result:
            structured_data.append(result)
    
    # Print summary
    print_summary(
        total=len(documents),
        successful=len(structured_data),
        failed=len(documents) - len(structured_data)
    )
    
    # Save results
    if structured_data:
        save_to_json(structured_data)
        print()
        print_sample_output(structured_data)
    else:
        print("No documents were successfully processed")


if __name__ == "__main__":
    main()
