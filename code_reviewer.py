"""AI-Driven Code Reviewer using Groq API."""
import os, json, ast, re
from groq import Groq
from typing import Dict, Any

class CodeReviewer:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"

    def review(self, code: str, language: str = "python", focus: str = "all") -> Dict[str, Any]:
        try:
            static = self._static_analysis(code, language)
            system = """You are a senior software engineer doing a thorough code review.
Return ONLY valid JSON:
{
  "overall_score": 0-100,
  "grade": "A+|A|B|C|D|F",
  "summary": "2 sentence overall assessment",
  "categories": {
    "readability":  {"score":0-100,"comment":"brief comment"},
    "performance":  {"score":0-100,"comment":"brief comment"},
    "security":     {"score":0-100,"comment":"brief comment"},
    "maintainability":{"score":0-100,"comment":"brief comment"},
    "best_practices":{"score":0-100,"comment":"brief comment"}
  },
  "issues": [
    {"line":number,"severity":"critical|warning|info","category":"security|performance|style|logic|naming","title":"short title","description":"what is wrong","fix":"how to fix it","code_fix":"corrected code snippet if applicable"}
  ],
  "strengths": ["what the code does well"],
  "refactored_code": "complete improved version of the code",
  "complexity": {"cyclomatic": number, "cognitive": number, "lines": number},
  "suggestions": ["actionable improvement suggestions"]
}"""
            focus_note = f" Focus especially on: {focus}." if focus != "all" else ""
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": f"Review this {language} code.{focus_note}\n\n```{language}\n{code}\n```"}
                ],
                temperature=0.3,
                max_tokens=3000
            )
            content = response.choices[0].message.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            review_data = json.loads(content)
            review_data["static"] = static
            return {"success": True, "review": review_data}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Parse error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _static_analysis(self, code: str, language: str) -> Dict:
        result = {"lines": len(code.splitlines()), "chars": len(code), "issues": []}
        if language == "python":
            try:
                ast.parse(code)
            except SyntaxError as e:
                result["issues"].append({"line": e.lineno, "type": "SyntaxError", "msg": str(e.msg)})
            # basic checks
            for i, line in enumerate(code.splitlines(), 1):
                if len(line) > 120:
                    result["issues"].append({"line": i, "type": "LineLength", "msg": f"Line too long ({len(line)} chars)"})
                if re.search(r'except\s*:', line):
                    result["issues"].append({"line": i, "type": "BareExcept", "msg": "Bare except clause"})
                if re.search(r'print\s*\(', line) and '#' not in line.split('print')[0]:
                    result["issues"].append({"line": i, "type": "DebugPrint", "msg": "Debug print statement"})
        return result

    def chat(self, code: str, question: str, history: list) -> Dict[str, Any]:
        """Chat about the code."""
        try:
            messages = [{"role": "system", "content": f"You are a code review assistant. The user is asking about this code:\n```\n{code}\n```\nBe concise and helpful."}]
            for h in history[-6:]:
                messages.append({"role": h["role"], "content": h["content"]})
            messages.append({"role": "user", "content": question})
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.5, max_tokens=800
            )
            return {"success": True, "answer": response.choices[0].message.content}
        except Exception as e:
            return {"success": False, "error": str(e)}
