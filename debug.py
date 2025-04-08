def ask_claude(prompt):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": "claude-3-haiku-20240307",  # versi stabil
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()

        # Jika sukses
        if "content" in data and isinstance(data["content"], list):
            return data["content"][0]["text"]
        
        # Jika error
        elif "error" in data:
            return f"Claude error: {data['error']['message']}"
        
        else:
            return f"Claude tidak memberikan jawaban yang sesuai: {data}"
    
    except Exception as e:
        return f"Error saat memproses respon Claude: {e}"
