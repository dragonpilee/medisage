import requests
import json

class GemmaClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    def generate(self, prompt: str) -> str:
        """Generate response using Gemma model with streaming."""
        try:
            # Use streaming to handle long responses
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                json={
                    "model": "gemma-4b",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2048,
                    "top_p": 0.95,
                    "frequency_penalty": 0.5,
                    "presence_penalty": 0.5,
                    "stream": True
                },
                stream=True,
                timeout=60  # Increased timeout
            )
            response.raise_for_status()
            
            # Process streaming response
            complete_response = ""
            for line in response.iter_lines():
                if line:
                    json_line = line.decode('utf-8')
                    if json_line.startswith('data: '):
                        json_line = json_line[6:]
                        if json_line == '[DONE]':
                            break
                        try:
                            data = json.loads(json_line)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {}).get('content', '')
                                complete_response += delta
                        except json.JSONDecodeError:
                            continue
            
            return complete_response
            
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Error: Network error - {str(e)}"
        except Exception as e:
            return f"Error: Unexpected error - {str(e)}"
