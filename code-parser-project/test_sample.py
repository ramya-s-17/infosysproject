"""Test script for analyzing sample code."""
import sys
sys.path.insert(0, '.')

from parser import analyze_code

# Read sample code
with open('../sample_code.py', 'r') as f:
    code = f.read()

# Analyze
result = analyze_code(code)

print("\n" + "="*60)
print("SAMPLE CODE ANALYSIS - Module 1 Test")
print("="*60)

if result['success']:
    print("\n✓ PARSING SUCCESSFUL\n")
    
    print("--- EXTRACTED FUNCTIONS ---")
    for func in result['structure']['functions']:
        print(f"  • {func['name']}({', '.join(func['args'])}) @ Line {func['lineno']}")
    
    print("\n--- EXTRACTED CLASSES ---")
    for cls in result['structure']['classes']:
        print(f"  • {cls['name']} @ Line {cls['lineno']}")
        if cls['methods']:
            for method in cls['methods']:
                print(f"      - {method}()")
    
    print("\n--- AST STATISTICS ---")
    stats = result['ast_stats']
    print(f"  Total Nodes: {stats['total_nodes']}")
    print(f"  Unique Node Types: {stats['unique_node_types']}")
    print(f"  Node Types: {list(stats['nodes_by_type'].keys())}")
    
    print("\n--- FORMATTED CODE (First 300 chars) ---")
    print(result['formatted_code'][:300] + "...")
else:
    print(f"\n✗ PARSING FAILED: {result['error']}")

print("\n" + "="*60)
print("Test complete!")
