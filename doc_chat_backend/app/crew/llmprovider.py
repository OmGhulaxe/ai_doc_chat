# app/crew/llmprovider.py
from crewai import LLM
import os
from typing import Any, Dict, Optional
from pydantic import ConfigDict
import logging
from tenacity import (
    retry, stop_after_attempt, wait_exponential, 
    retry_if_exception_type, before_sleep_log
)
import time
from litellm import ModelResponse

logger = logging.getLogger(__name__)

class CustomLLM(LLM):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    _instance: Optional['CustomLLM'] = None
    _last_request_time: float = 0
    _min_delay: float = 1.0  # Minimum delay between requests

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.model_config: Dict[str, Any] = {
                "model": "mistralai/mixtral-8x7b-instruct",
                "provider": "openrouter",
                "api_key": os.getenv("OPENROUTER_API_KEY"),
                "base_url": "https://openrouter.ai/api/v1",
                "fallback_models": [
                    "claude-3-opus-20240229",
                    "gpt-4-0125-preview",
                    "mistral-large-latest"
                ],
                "timeout": 30,
                "max_retries": 3,
                "http_headers": {
                    "HTTP-Referer": os.getenv("APP_URL", "http://localhost:8000"),
                    "X-Title": "AI Doc Chat"
                }
            }
            super().__init__(
                model="openrouter/mistralai/mixtral-8x7b-instruct",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1"
            )
            self._initialized = True
            self._current_model_index = 0
            logger.info("CustomLLM initialized with fallback models")

    def _rate_limit(self):
        current_time = time.time()
        elapsed = current_time - self._last_request_time
        if elapsed < self._min_delay:
            time.sleep(self._min_delay - elapsed)
        self._last_request_time = time.time()

    def _try_fallback_model(self, error: Exception) -> bool:
        if self._current_model_index < len(self.model_config["fallback_models"]) - 1:
            self._current_model_index += 1
            new_model = self.model_config["fallback_models"][self._current_model_index]
            logger.warning(f"Switching to fallback model: {new_model} due to: {str(error)}")
            self.model_config["model"] = new_model
            return True
        return False

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def acompletion(self, prompt: str, **kwargs: Any) -> str:
        try:
            self._rate_limit()
            kwargs['model'] = self.model_config
            return await super().acompletion(prompt, **kwargs)
        except Exception as e:
            if self._try_fallback_model(e):
                return await self.acompletion(prompt, **kwargs)
            logger.error(f"All models failed: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def completion(self, prompt: str, **kwargs: Any) -> str:
        try:
            self._rate_limit()
            kwargs['model'] = self.model_config
            return super().completion(prompt, **kwargs)
        except Exception as e:
            if self._try_fallback_model(e):
                return self.completion(prompt, **kwargs)
            logger.error(f"All models failed: {str(e)}")
            raise

# Singleton instance
llm = CustomLLM()
