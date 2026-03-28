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
from story_generator import StoryGenerator
from code_reviewer import CodeReviewer

app = Flask(__name__)

# Initialize modules
error_detector = ErrorDetector()
try:
    ai_suggestor = AISuggestor()
except ValueError as e:
    print(f"Warning: AI Suggestor not initialized - {e}")
    ai_suggestor = None

try:
    story_gen = StoryGenerator()
except ValueError as e:
    print(f"Warning: Story Generator not initialized - {e}")
    story_gen = None

try:
    code_reviewer = CodeReviewer()
except ValueError as e:
    print(f"Warning: Code Reviewer not initialized - {e}")
    code_reviewer = None

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

@app.route('/reviewer')
def reviewer():
    return render_template('reviewer.html')

@app.route('/api/review', methods=['POST'])
def review_code():
    try:
        if not code_reviewer:
            return jsonify({'success': False, 'error': 'Code Reviewer not available.'}), 503
        data = request.get_json()
        code = data.get('code', '').strip()
        language = data.get('language', 'python')
        focus = data.get('focus', 'all')
        if not code:
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        result = code_reviewer.review(code, language, focus)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/review-chat', methods=['POST'])
def review_chat():
    try:
        if not code_reviewer:
            return jsonify({'success': False, 'error': 'Code Reviewer not available.'}), 503
        data = request.get_json()
        code = data.get('code', '')
        question = data.get('question', '')
        history = data.get('history', [])
        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400
        result = code_reviewer.chat(code, question, history)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/story')
def story():
    return render_template('story.html')

@app.route('/api/generate-story', methods=['POST'])
def generate_story():
    try:
        if not story_gen:
            return jsonify({'success': False, 'error': 'Story Generator not available.'}), 503
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        style = data.get('style', 'epic')
        length = int(data.get('length', 5))
        if not prompt:
            return jsonify({'success': False, 'error': 'No prompt provided'}), 400
        result = story_gen.generate_story(prompt, style, length)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/continue-story', methods=['POST'])
def continue_story():
    try:
        if not story_gen:
            return jsonify({'success': False, 'error': 'Story Generator not available.'}), 503
        data = request.get_json()
        story = data.get('story', {})
        direction = data.get('direction', 'continue the adventure')
        result = story_gen.continue_story(story, direction)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


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
    import os
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*60)
    print("CODE PARSING WEB APPLICATION")
    print("="*60)
    print(f"\nStarting web server on port {port}...")
    print("\n" + "="*60 + "\n")
    app.run(debug=False, port=port, host='0.0.0.0')
