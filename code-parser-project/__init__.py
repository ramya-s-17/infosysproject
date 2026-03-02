"""
Code Parser Project - Module 1: Code Parsing & Preprocessing

This package provides tools for parsing, analyzing, and preprocessing Python code
using Abstract Syntax Tree (AST) technology.
"""

__version__ = "1.0.0"
__author__ = "Infoysys"

from code_parser_project.parser import (
    CodeParser,
    ASTNodeVisitor,
    analyze_code
)

__all__ = [
    'CodeParser',
    'ASTNodeVisitor',
    'analyze_code'
]
