"""Error detection module for Python code analysis."""

import ast
import re
from typing import List, Dict, Any


class ErrorDetector:
    """Detects common errors and issues in Python code."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def detect_errors(self, code: str) -> Dict[str, Any]:
        """Analyze code and detect potential errors."""
        self.errors = []
        self.warnings = []
        
        # Check for syntax errors
        try:
            tree = ast.parse(code)
            self._analyze_ast(tree, code)
        except SyntaxError as e:
            self.errors.append({
                'type': 'SyntaxError',
                'line': e.lineno,
                'message': str(e.msg),
                'severity': 'error'
            })
        
        # Check for common issues
        self._check_common_issues(code)
        
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings)
        }
    
    def _analyze_ast(self, tree: ast.AST, code: str):
        """Analyze AST for potential issues."""
        for node in ast.walk(tree):
            # Check for unused variables
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                pass  # Could track variable usage
            
            # Check for bare except clauses
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    self.warnings.append({
                        'type': 'BareExcept',
                        'line': node.lineno,
                        'message': 'Bare except clause catches all exceptions',
                        'severity': 'warning'
                    })
    
    def _check_common_issues(self, code: str):
        """Check for common coding issues."""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for missing whitespace around operators
            if re.search(r'\w+=[^=]', line) and '==' not in line:
                if not re.search(r'\w+\s*=\s*', line):
                    self.warnings.append({
                        'type': 'StyleIssue',
                        'line': i,
                        'message': 'Missing whitespace around assignment operator',
                        'severity': 'warning'
                    })
