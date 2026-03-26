"""Model client factory — creates 4 agents via Microsoft Agent Framework."""

import os

from agent_framework.openai import OpenAIChatClient
from agent_framework_anthropic import AnthropicClient

from .config import MAX_TOKENS, SYSTEM_PROMPT, TEMPERATURE


def create_agents() -> dict:
    """Create and return agents for all 4 models."""
    opts = {"temperature": TEMPERATURE, "max_tokens": MAX_TOKENS}

    agents = {
        "claude-opus-4.6": AnthropicClient(
            model_id="claude-opus-4-6",
        ).as_agent(
            name="evaluator",
            instructions=SYSTEM_PROMPT,
            default_options=opts,
        ),
        "gpt-5.4": OpenAIChatClient(
            model_id="gpt-5.4",
        ).as_agent(
            name="evaluator",
            instructions=SYSTEM_PROMPT,
            default_options=opts,
        ),
        "gemini-3.1-pro": OpenAIChatClient(
            model_id="gemini-3.1-pro-preview",
            api_key=os.environ.get("GOOGLE_API_KEY", ""),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        ).as_agent(
            name="evaluator",
            instructions=SYSTEM_PROMPT,
            default_options=opts,
        ),
        "glm-5": OpenAIChatClient(
            model_id="zai-org/GLM-5",
            api_key=os.environ.get("TOGETHER_API_KEY", ""),
            base_url="https://api.together.xyz/v1",
        ).as_agent(
            name="evaluator",
            instructions=SYSTEM_PROMPT,
            default_options=opts,
        ),
        "kimi-k2.5": OpenAIChatClient(
            model_id="moonshotai/Kimi-K2.5",
            api_key=os.environ.get("TOGETHER_API_KEY", ""),
            base_url="https://api.together.xyz/v1",
        ).as_agent(
            name="evaluator",
            instructions=SYSTEM_PROMPT,
            default_options=opts,
        ),
    }
    return agents
