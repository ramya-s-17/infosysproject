import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import math
from datetime import datetime

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from parser import CodeParser, analyze_code


class CodeFeedbackSystem:
   
    
    def __init__(self):
        """Initialize the feedback system."""
        self.parser = CodeParser()
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.groq_model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
        
    def validate_api_keys(self) -> bool:
        """
        Validate that required API keys are configured.
        
        Returns:
            bool: True if all keys are configured, False otherwise
        """
        if not self.groq_api_key or self.groq_api_key == 'your_api_key_here':
            print("⚠ Warning: GROQ_API_KEY not properly configured in .env file")
            print("  Visit https://console.groq.com to get your API key")
            return False
        return True
    
    def process_code(self, code: str) -> dict:
        """
        Process student code through the parsing pipeline.
        
        Args:
            code (str): Student's Python code
            
        Returns:
            dict: Processing results with parsed, formatted, and structure info
        """
        print("\n" + "="*60)
        print("CODE FEEDBACK SYSTEM - Module 1: Parsing & Preprocessing")
        print("="*60)
        
        # Perform comprehensive analysis
        analysis = analyze_code(code)
        
        if not analysis['success']:
            print(f"\n✗ Error parsing code: {analysis['error']}")
            return analysis
        
        print("\n✓ Code parsing successful!")
        
        # Display analysis results
        self._display_results(analysis)
        
        return analysis
    
    def _display_results(self, analysis: dict) -> None:
        """
        Display code analysis results in a formatted manner.
        
        Args:
            analysis (dict): Analysis results from analyze_code()
        """
        print("\n--- PARSED CODE (Formatted) ---")
        print(analysis['formatted_code'])
        
        print("\n--- CODE STRUCTURE ---")
        structure = analysis['structure']
        
        if structure['functions']:
            print(f"\nFunctions ({len(structure['functions'])}):")
            for func in structure['functions']:
                print(f"  • {func['name']}({', '.join(func['args'])}) @ Line {func['lineno']}")
        
        if structure['classes']:
            print(f"\nClasses ({len(structure['classes'])}):")
            for cls in structure['classes']:
                print(f"  • {cls['name']} @ Line {cls['lineno']}")
                if cls['methods']:
                    for method in cls['methods']:
                        print(f"      - {method}()")
        
        if structure['imports']:
            print(f"\nImports: {len(structure['imports'])} statement(s)")
        
        if structure['assignments']:
            print(f"Variable Assignments: {len(structure['assignments'])}")
        
        print("\n--- AST STATISTICS ---")
        stats = analysis['ast_stats']
        print(f"Total AST Nodes: {stats['total_nodes']}")
        print(f"Unique Node Types: {stats['unique_node_types']}")
    
    def save_results(self, analysis: dict, output_file: str = "analysis_results.txt") -> bool:
        """
        Save analysis results to a file.
        
        Args:
            analysis (dict): Analysis results from analyze_code()
            output_file (str): Path to save results
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with open(output_file, 'w') as f:
                f.write("CODE FEEDBACK SYSTEM - Analysis Results\n")
                f.write("="*60 + "\n\n")
                
                f.write("--- FORMATTED CODE ---\n")
                f.write(analysis['formatted_code'])
                f.write("\n\n")
                
                f.write("--- CODE STRUCTURE ---\n")
                structure = analysis['structure']
                f.write(f"Functions: {structure['functions']}\n")
                f.write(f"Classes: {structure['classes']}\n")
                f.write(f"Imports: {len(structure['imports'])}\n")
                f.write(f"Assignments: {len(structure['assignments'])}\n\n")
                
                f.write("--- AST STATISTICS ---\n")
                stats = analysis['ast_stats']
                f.write(f"Total nodes: {stats['total_nodes']}\n")
                f.write(f"Unique types: {stats['unique_node_types']}\n")
            
            print(f"\n✓ Results saved to {output_file}")
            return True
        except Exception as e:
            print(f"\n✗ Error saving results: {str(e)}")
            return False

def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n - 1)

class DataProcessor:
    def __init__(self, name):
        self.name = name
        self.data = []
    
    def add_data(self, value):
        self.data.append(value)
        return len(self.data)
    
    def get_average(self):
        if len(self.data) == 0:
            return 0
        return sum(self.data) / len(self.data)
    
    def process_data(self):
        processed = [x * 2 for x in self.data]
        return processed

def interactive_mode():
    """
    Run the system in interactive mode for testing and development.
    """
    system = CodeFeedbackSystem()
    
    print("\n" + "="*60)
    print("CODE FEEDBACK SYSTEM - Interactive Mode")
    print("="*60)
    print("\nInstructions:")
    print("1. Paste your Python code (Press Enter twice to finish)")
    print("2. Code will be analyzed and formatted")
    print("3. Results displayed with structure and suggestions")
    print("\nType 'quit' to exit\n")
    
    while True:
        print("-" * 60)
        print("Enter Python code (or 'quit' to exit):")
        print("-" * 60)
        
        lines = []
        blank_lines = 0
        
        while True:
            try:
                line = input()
                if line.lower() == 'quit':
                    print("\nExiting...")
                    return
                if line == '':
                    blank_lines += 1
                    if blank_lines >= 2:
                        break
                else:
                    blank_lines = 0
                lines.append(line)
            except EOFError:
                break
        
        code = '\n'.join(lines).strip()
        
        if code:
            # Validate API keys
            system.validate_api_keys()
            
            # Process the code
            analysis = system.process_code(code)
            if analysis['success']:
                save = input("\nSave results to file? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Enter filename (default: analysis_results.txt): ").strip()
                    if not filename:
                        filename = "analysis_results.txt"
                    system.save_results(analysis, filename)


def main():
    """Main entry point for the application."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Code Parsing & Preprocessing System - Module 1'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Path to Python file to analyze'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    parser.add_argument(
        '--check-env',
        action='store_true',
        help='Check environment configuration'
    )
    
    args = parser.parse_args()
    
    # Check environment
    if args.check_env:
        print("\n" + "="*60)
        print("Environment Configuration Check")
        print("="*60)
        system = CodeFeedbackSystem()
        if system.validate_api_keys():
            print("✓ All environment variables configured correctly!")
        print(f"\nModel: {system.groq_model}")
        print(f"API Key configured: {'✓' if system.groq_api_key else '✗'}")
        return
    
    # Analyze file
    if args.file:
        try:
            with open(args.file, 'r') as f:
                code = f.read()
            system = CodeFeedbackSystem()
            analysis = system.process_code(code)
            
            # Auto-save analysis
            output_file = args.file.replace('.py', '_analysis.txt')
            system.save_results(analysis, output_file)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
        except Exception as e:
            print(f"Error: {str(e)}")
        return
    
    # Interactive mode (default)
    interactive_mode()


if __name__ == "__main__":
    main()
