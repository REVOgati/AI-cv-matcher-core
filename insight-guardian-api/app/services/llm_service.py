# File: /insight-guardian-api/insight-guardian-api/app/services/llm_service.py

# This file serves as the service layer for integrating with the OpenAI LLM. 
# It will contain functions to interact with the LLM for insights and anomaly detection.

from typing import Any, Dict
from openai import OpenAI
from app.core.config import settings

# Initialize the OpenAI client for OpenRouter
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


class LLMService:
    """
    Handles interaction with OpenAI models.
    This class can be reused for any LLM-related tasks (e.g., chat, completion, analysis).
    """

    @staticmethod
    def ask_model(prompt: str, model: str = "gpt-4") -> str:
        """
        Sends a prompt to the specified OpenAI model and returns the response.

        Args:
            prompt (str): The user's input or question.
            model (str): The model to use (default: "gpt-4").

        Returns:
            str: The model's response or an error message.
        """
        try:
            # Create a chat completion using the OpenAI client
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are Insight Guardian API."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            # Extract and return the assistant's reply
            return response.choices[0].message.content
        except Exception as e:
            # Return a readable error message
            return f"Error with LLM request: {str(e)}"

    @staticmethod
    def extract_cv_info(cv_text: str, model: str = "gpt-4") -> dict:
        """
        Extracts candidate info, work experience, and education from CV text using LLM.
        Returns a structured dict or error message.
        """
        # Truncate CV text to fit within token limits (e.g., first 1000 characters)
        truncated_text = cv_text[:1000]
        prompt_instructions = (
            "Extract the following information from the provided CV text. If any field is missing, return null. "
            "Recognize synonyms and context (e.g., 'Professional History' for 'Work Experience'). "
            "Return arrays for work_experiences and educations. Portfolio links should be valid URLs. "
            "Use this JSON schema for your response. Only return valid JSON, do not include any explanation or extra text.\n"
            "{\n"
            "  'candidate': {\n"
            "    'full_name': 'string',\n"
            "    'first_name': 'string or null',\n"
            "    'last_name': 'string or null',\n"
            "    'email': 'string',\n"
            "    'phone': 'string or null',\n"
            "    'date_of_birth': 'YYYY-MM-DD or null',\n"
            "    'links': [\n"
            "      {'link_1': 'url or null'},\n"
            "      {'link_2': 'url or null'},\n"
            "      {'link_3': 'url or null'}\n"
            "    ],\n"
            "    'preferences': 'json structure or null'\n"
            "  },\n"
            "  'work_experiences': [\n"
            "    {\n"
            "      'company_name': 'string',\n"
            "      'job_title': 'string',\n"
            "      'from_date': 'YYYY-MM-DD',\n"
            "      'to_date': 'YYYY-MM-DD or null',\n"
            "      'is_current': 'boolean',\n"
            "      'responsibilities': 'string or null'\n"
            "    }\n"
            "  ],\n"
            "  'educations': [\n"
            "    {\n"
            "      'institution_name': 'string',\n"
            "      'course': 'string',\n"
            "      'from_date': 'YYYY-MM-DD',\n"
            "      'to_date': 'YYYY-MM-DD or null',\n"
            "      'is_current': 'boolean'\n"
            "    }\n"
            "  ]\n"
            "}\n"
        )
        prompt = prompt_instructions + f"\nCV Text:\n{truncated_text}"
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for CV parsing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=330
            )
            raw_output = response.choices[0].message.content
            print("--- Raw LLM Output ---")
            print(raw_output)
            import json
            if not raw_output or raw_output.strip() == "":
                return {"error": "LLM returned empty response."}
            try:
                return json.loads(raw_output)
            except Exception as e:
                return {"error": f"Failed to parse LLM output as JSON: {str(e)}", "output": raw_output}
        except Exception as e:
            return {"error": str(e)}


