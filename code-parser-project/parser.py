"""
Code Parser Module
Handles parsing, preprocessing, and formatting of Python code using AST.

This module provides functionality to:
- Parse Python code using ast.parse()
- Unparse AST back to formatted code using ast.unparse()
- Dump AST tree structure using ast.dump()
- Analyze code structure with custom visitor patterns
"""

import ast
import sys
from typing import Dict, Any, Optional


class CodeParser:
    """
    Parser for Python code using Abstract Syntax Tree (AST).
    
    The AST module is Python's internal library for understanding and parsing code.
    It converts source code into a tree structure that can be analyzed and manipulated.
    """
    
    def __init__(self):
        """Initialize the code parser."""
        self.ast_tree = None
        self.source_code = None
        self.formatted_code = None
        
    def parse_code(self, code: str) -> Dict[str, Any]:
        """
        Parse Python code and convert it to AST.
        
        Uses ast.parse() which internally understands code structure and corrects formatting.
        
        Args:
            code (str): The Python source code to parse
            
        Returns:
            Dict[str, Any]: Dictionary containing parse results with keys:
                - 'success': bool indicating if parsing was successful
                - 'ast': The AST tree object
                - 'error': Error message if parsing failed (None if successful)
                - 'error_type': Type of error encountered (None if successful)
        """
        try:
            self.source_code = code
            self.ast_tree = ast.parse(code)
            return {
                'success': True,
                'ast': self.ast_tree,
                'error': None,
                'error_type': None
            }
        except SyntaxError as e:
            return {
                'success': False,
                'ast': None,
                'error': str(e),
                'error_type': 'SyntaxError'
            }
        except Exception as e:
            return {
                'success': False,
                'ast': None,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def format_code(self, code: str) -> Optional[str]:
        """
        Parse and format Python code to improve readability.
        
        Uses ast.parse() to understand the code structure, then ast.unparse()
        to convert it back to properly formatted code.
        
        Args:
            code (str): The Python source code to format
            
        Returns:
            Optional[str]: Formatted code if successful, None if parsing failed
        """
        parse_result = self.parse_code(code)
        if parse_result['success']:
            try:
                self.formatted_code = ast.unparse(self.ast_tree)
                return self.formatted_code
            except Exception as e:
                print(f"Error during formatting: {str(e)}")
                return None
        else:
            print(f"Cannot format code: {parse_result['error']}")
            return None
    
    def dump_ast(self, code: Optional[str] = None, annotate_fields: bool = True, 
                 include_attributes: bool = False) -> Optional[str]:
        """
        Generate a detailed string representation of the AST.
        
        Uses ast.dump() to create a printable representation of the AST tree.
        Useful for understanding code structure and analyzing syntax.
        
        Args:
            code (str, optional): Source code to parse. If None, uses previously parsed code.
            annotate_fields (bool): If True, includes field names in output
            include_attributes (bool): If True, includes position/lineno info
            
        Returns:
            Optional[str]: String dump of AST tree, or None if no code available
        """
        if code is not None:
            parse_result = self.parse_code(code)
            if not parse_result['success']:
                print(f"Cannot dump AST: {parse_result['error']}")
                return None
        
        if self.ast_tree is None:
            print("No parsed code available. Please parse code first.")
            return None
        
        try:
            ast_dump = ast.dump(
                self.ast_tree,
                annotate_fields=annotate_fields,
                include_attributes=include_attributes
            )
            return ast_dump
        except Exception as e:
            print(f"Error dumping AST: {str(e)}")
            return None
    
    def get_code_structure(self) -> Optional[Dict[str, Any]]:
        """
        Extract code structure information from parsed AST.
        
        Analyzes the AST tree to extract:
        - Functions and their signatures
        - Classes and their methods
        - Module-level imports
        - Top-level assignments
        
        Returns:
            Optional[Dict[str, Any]]: Structure information or None if no code parsed
        """
        if self.ast_tree is None:
            return None
        
        structure = {
            'functions': [],
            'classes': [],
            'imports': [],
            'assignments': []
        }
        
        try:
            for node in ast.walk(self.ast_tree):
                if isinstance(node, ast.FunctionDef):
                    structure['functions'].append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'args': [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    structure['classes'].append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    structure['imports'].append({
                        'lineno': node.lineno,
                        'type': type(node).__name__
                    })
                elif isinstance(node, ast.Assign):
                    structure['assignments'].append({
                        'lineno': node.lineno
                    })
        except Exception as e:
            print(f"Error extracting structure: {str(e)}")
            return None
        
        return structure


class ASTNodeVisitor(ast.NodeVisitor):
    """
    Custom AST Node Visitor for traversing and analyzing code structure.
    
    NodeVisitor is the base class for visiting all nodes in the AST tree.
    Subclass this to implement custom analysis and transformations.
    """
    
    def __init__(self):
        """Initialize the visitor."""
        self.node_count = 0
        self.nodes_by_type = {}
    
    def visit(self, node):
        """
        Visit a node in the AST tree.
        
        Called for every node when traversing the tree.
        Overrides the default visit to count node types.
        
        Args:
            node: AST node to visit
        """
        node_type = type(node).__name__
        self.nodes_by_type[node_type] = self.nodes_by_type.get(node_type, 0) + 1
        self.node_count += 1
        self.generic_visit(node)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about visited AST nodes.
        
        Returns:
            Dict[str, Any]: Dictionary with node counts and statistics
        """
        return {
            'total_nodes': self.node_count,
            'nodes_by_type': self.nodes_by_type,
            'unique_node_types': len(self.nodes_by_type)
        }


def analyze_code(code: str) -> Dict[str, Any]:
    """
    Comprehensive analysis of Python code.
    
    Performs multiple analyses on the provided code:
    1. AST parsing and validation
    2. Code formatting
    3. Structure extraction
    4. AST statistics
    
    Args:
        code (str): Python source code to analyze
        
    Returns:
        Dict[str, Any]: Complete analysis results
    """
    parser = CodeParser()
    
    # Parse the code
    parse_result = parser.parse_code(code)
    
    if not parse_result['success']:
        return {
            'success': False,
            'error': parse_result['error'],
            'error_type': parse_result['error_type']
        }
    
    # Get formatted code
    formatted = parser.format_code(code)
    
    # Get code structure
    structure = parser.get_code_structure()
    
    # Get AST statistics
    visitor = ASTNodeVisitor()
    visitor.visit(parser.ast_tree)
    stats = visitor.get_statistics()
    
    return {
        'success': True,
        'original_code': code,
        'formatted_code': formatted,
        'structure': structure,
        'ast_stats': stats,
        'ast_dump': parser.dump_ast(annotate_fields=True, include_attributes=False)
    }


if __name__ == "__main__":
    # Example usage
    sample_code = """
def hello_world():
    x=1
    y=2
    print(x+y)

class MyClass:
    def __init__(self):
        self.value = 0
"""
    
    print("=" * 60)
    print("CODE PARSER - AST Analysis Demo")
    print("=" * 60)
    
    # Analyze the sample code
    result = analyze_code(sample_code)
    
    if result['success']:
        print("\n✓ Parsing successful!")
        print("\n--- Original Code ---")
        print(result['original_code'])
        print("\n--- Formatted Code ---")
        print(result['formatted_code'])
        print("\n--- Code Structure ---")
        print(f"Functions: {result['structure']['functions']}")
        print(f"Classes: {result['structure']['classes']}")
        print("\n--- AST Statistics ---")
        print(f"Total nodes: {result['ast_stats']['total_nodes']}")
        print(f"Unique node types: {result['ast_stats']['unique_node_types']}")
    else:
        print(f"\n✗ Parsing failed: {result['error']}")
