# Code Parsing & Preprocessing Project - Module 1

A Python-based code parsing and preprocessing system using Abstract Syntax Tree (AST) for analyzing and formatting Python code.

## Project Overview

This project provides intelligent feedback to users based on Python's AST (Abstract Syntax Tree) library. The AST module is Python's internal library for understanding and parsing code, converting source code into a tree structure that can be analyzed and manipulated.

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation Steps

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   - On Windows:
     ```bash
     venv\Scripts\Activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individual packages:
   ```bash
   pip install langchain langchain-core langchain-community langchain-groq python-dotenv
   ```

4. **Configure API Keys**
   - Copy `.env` file and add your Groq API key:
     ```
     GROQ_API_KEY=your_api_key_here
     ```
   - Get your key from: https://console.groq.com

## Project Structure

```
infoysys project/
├── code-parser-project/
│   ├── parser.py              # Core AST parsing module
│   └── main.py                # Main application entry point
├── .env                       # API configuration (not tracked in git)
├── requirements.txt           # Project dependencies
└── README.md                  # This file
```

## Core Features - Module 1

### 1. **Code Parsing (parser.py)**
   - **ast.parse()**: Parse Python code into an Abstract Syntax Tree
   - **ast.unparse()**: Convert AST back to formatted code
   - **ast.dump()**: Generate detailed AST tree representation
   - **ast.NodeVisitor**: Custom visitor for analyzing code structure

### 2. **CodeParser Class**
   Main class for parsing and preprocessing code with methods:
   - `parse_code()`: Parse Python code and validate syntax
   - `format_code()`: Format code for better readability
   - `dump_ast()`: Generate AST dump for analysis
   - `get_code_structure()`: Extract functions, classes, imports, and assignments

### 3. **ASTNodeVisitor Class**
   Custom AST visitor for traversing and analyzing code:
   - Count different node types
   - Generate AST statistics
   - Collect node information

### 4. **Utility Functions**
   - `analyze_code()`: Comprehensive code analysis combining all features

## Key AST Functions Explained

### ast.parse(code, mode='exec', type_comments=False, feature_version=None)
- Parses Python source code into an AST tree
- Internally corrects code formatting
- Raises `SyntaxError` if code is invalid

### ast.unparse(node)
- Converts AST back to valid Python code
- Returns properly formatted source code
- Useful for displaying corrected versions

### ast.dump(node, annotate_fields=True, include_attributes=False, *, indent=None)
- Creates a string representation of the AST
- Shows tree structure and node types
- Helpful for debugging and understanding code structure

### ast.NodeVisitor
- Base class for traversing AST nodes
- Implement `visit_<NodeType>()` methods for custom analysis
- Use `generic_visit()` to traverse child nodes

## Usage Examples

### Basic Code Parsing
```python
from code-parser-project.parser import CodeParser

parser = CodeParser()
result = parser.parse_code("x = 1 + 2")

if result['success']:
    print("Code parsed successfully!")
else:
    print(f"Error: {result['error']}")
```

### Code Formatting
```python
dirty_code = """
def hello(x,y,z):
    a=1
    b=2
    return a+b
"""

formatted = parser.format_code(dirty_code)
print(formatted)
```

### Get Code Structure
```python
structure = parser.get_code_structure()
print(structure['functions'])
print(structure['classes'])
```

### Full Analysis
```python
from code-parser-project.parser import analyze_code

result = analyze_code(your_code)
print(result['formatted_code'])
print(result['structure'])
print(result['ast_stats'])
```

## Model Configuration

This project uses the following LLM model:
- **Provider**: Groq
- **Model**: `llama-3.1-8b-instant`
- **Integration**: LangChain's ChatGroq wrapper

## Next Steps (Future Modules)

- Module 2: AI-powered code analysis and suggestions using LLM
- Module 3: Integration with web interface
- Module 4: Support for additional programming languages

## Troubleshooting

### Issue: Virtual environment not activating
**Solution**: Ensure you're in the project directory and run the correct activation command for your OS

### Issue: Import errors with langchain
**Solution**: Verify all packages installed correctly: `pip list | grep langchain`

### Issue: .env file not loading
**Solution**: Ensure python-dotenv is installed and you load it in your code with: `from dotenv import load_dotenv; load_dotenv()`

### Issue: Groq API authentication fails
**Solution**: Verify your API key is correct and active at https://console.groq.com

## Resources

- Python AST Documentation: https://docs.python.org/3/library/ast.html
- Groq Console: https://console.groq.com
- LangChain Documentation: https://python.langchain.com/
- LangChain Groq Integration: https://python.langchain.com/docs/integrations/chat/groq

## License

This project is part of the Infoysys educational program.

---

