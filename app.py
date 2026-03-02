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
from error_detector import ErrorDetector
from ai_suggestor import AISuggestor

app = Flask(__name__)

# Initialize modules
error_detector = ErrorDetector()
try:
    ai_suggestor = AISuggestor()
except ValueError as e:
    print(f"Warning: AI Suggestor not initialized - {e}")
    ai_suggestor = None

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze code with advanced features."""
    try:
        data = request.get_json()
        code = data.get('code', '')
        include_ai = data.get('include_ai', False)
        
        if not code.strip():
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        # Analyze the code
        parser = CodeParser()
        analysis = analyze_code(code)
        
        # Detect errors
        error_analysis = error_detector.detect_errors(code)
        
        # Get AI suggestions if requested
        ai_suggestions = None
        if include_ai and ai_suggestor:
            all_issues = error_analysis['errors'] + error_analysis['warnings']
            ai_result = ai_suggestor.get_suggestions(code, all_issues)
            if ai_result['success']:
                ai_suggestions = ai_result['suggestions']
        
        return jsonify({
            'success': True,
            'formatted_code': analysis['formatted_code'],
            'structure': analysis['structure'],
            'ast_stats': analysis['ast_stats'],
            'errors': error_analysis['errors'],
            'warnings': error_analysis['warnings'],
            'error_count': error_analysis['error_count'],
            'warning_count': error_analysis['warning_count'],
            'ai_suggestions': ai_suggestions
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

@app.route('/api/detect-errors', methods=['POST'])
def detect_errors():
    """API endpoint for error detection only."""
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code.strip():
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        result = error_detector.detect_errors(code)
        result['success'] = True
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500

@app.route('/api/ai-suggest', methods=['POST'])
def ai_suggest():
    """API endpoint for AI suggestions."""
    try:
        if not ai_suggestor:
            return jsonify({
                'success': False,
                'error': 'AI Suggestor not available. Check GROQ_API_KEY.'
            }), 503
        
        data = request.get_json()
        code = data.get('code', '')
        errors = data.get('errors', [])
        
        if not code.strip():
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        result = ai_suggestor.get_suggestions(code, errors)
        
        return jsonify(result)
    
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
