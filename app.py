from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'code-parser-project'))

from parser import CodeParser, analyze_code

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze code."""
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code.strip():
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        # Analyze the code
        parser = CodeParser()
        analysis = analyze_code(code)
        
        return jsonify({
            'success': True,
            'formatted_code': analysis['formatted_code'],
            'structure': analysis['structure'],
            'ast_stats': analysis['ast_stats']
        })
    
    except SyntaxError as e:
        return jsonify({
            'success': False,
            'error': f'Syntax Error: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("CODE PARSING WEB APPLICATION")
    print("="*60)
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, port=5000, host='localhost')
