import json
from pathlib import Path

import yaml

from src.models.contract import PromptConfig

CURRENT_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"
class PromptManager:
    """ Class for interacting with prompts as versioned yaml"""
    def __init__(self, prompts_dir: str = CURRENT_DIR):
        """
        Initializes the Prompt manager Class.

        Args:
            prompts_dir: (str): hardcoded 'prompts' directory containing versioned prompts
        """
        self.prompts_dir = Path(prompts_dir)

    def load_prompt_config(self, prompt_name: str, version: str) -> PromptConfig:
        """Loads a specific version of a prompt from a YAML file."""
        file_name = f"{prompt_name}_{version}.yaml"
        file_path = self.prompts_dir / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)

        return PromptConfig.model_validate(raw_config)

    def get_openai_messages(self, prompt_config: PromptConfig, user_input: str) -> list[dict[str, str]]:
        """Formats the system prompt, few-shot examples, and user input for OpenAI."""
        messages = [{"role": "system", "content": prompt_config.system_prompt}]

        for example in prompt_config.few_shot_examples:
            messages.append({"role": "user", "content": example.input})
            messages.append(
                {
                    "role": "assistant",
                    "content": json.dumps(example.output.model_dump()),
                }
            )

        messages.append({"role": "user", "content": user_input})
        return messages
