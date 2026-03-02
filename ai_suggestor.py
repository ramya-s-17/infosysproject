"""AI-powered code suggestion module using Groq API."""

import os
from groq import Groq
from typing import Dict, Any, Optional


class AISuggestor:
    """Provides AI-powered code suggestions and improvements."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Groq API key from environment or parameter."""
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def get_suggestions(self, code: str, errors: list = None) -> Dict[str, Any]:
        """Get AI-powered suggestions for code improvement."""
        try:
            prompt = self._build_prompt(code, errors)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Python code expert. Provide concise, actionable suggestions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            suggestions = response.choices[0].message.content
            
            return {
                'success': True,
                'suggestions': suggestions,
                'model': self.model
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_prompt(self, code: str, errors: list = None) -> str:
        """Build prompt for AI analysis."""
        prompt = f"Analyze this Python code and provide improvement suggestions:\n\n```python\n{code}\n```\n\n"
        
        if errors:
            prompt += f"Detected issues:\n"
            for error in errors:
                prompt += f"- Line {error.get('line', 'N/A')}: {error.get('message', 'Unknown')}\n"
            prompt += "\n"
        
        prompt += "Provide:\n1. Code quality improvements\n2. Best practice recommendations\n3. Performance optimizations"
        
        return prompt
