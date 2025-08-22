# File: /insight-guardian-api/insight-guardian-api/app/services/llm_service.py

# This file serves as the service layer for integrating with the OpenAI LLM. 
# It will contain functions to interact with the LLM for insights and anomaly detection.

from typing import Any, Dict
import openai
from core.config import settings

import openai
from app.core.config import settings

# Initialize OpenAI client
openai.api_key = settings.OPENAI_API_KEY

class LLMService:
    """Handles interaction with OpenAI models"""

    @staticmethod
    def ask_model(prompt: str, model="gpt-4"):
        """
        Sends a prompt to OpenAI and returns the response.
        """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "system", "content": "You are Insight Guardian API."},
                          {"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error with LLM request: {str(e)}"


   