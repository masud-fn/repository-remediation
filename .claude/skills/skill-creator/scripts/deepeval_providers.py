"""Provider factory for DeepEval LLM backends.

Supported providers:
  claude   — claude -p CLI (local, no API key required; uses Claude Code auth)
  bedrock  — AWS Bedrock via IAM default credential chain (requires AWS_BEDROCK_REGION)
  copilot  — GitHub Models API via LiteLLM (uses `gh auth token`; falls back to GITHUB_TOKEN)

Usage:
    from scripts.deepeval_providers import get_model
    model = get_model("claude")
    model = get_model("bedrock", region="us-east-1")
    model = get_model("copilot", model="gpt-4o")
"""

import os
import subprocess
from typing import Optional, Tuple, Union

from deepeval.models.base_model import DeepEvalBaseLLM

from scripts.utils import claude_subprocess_env

DEFAULT_MODELS = {
    # claude: no default — CLI uses whatever model the user has configured.
    "bedrock": "us.anthropic.claude-sonnet-4-6",
    "copilot": "gpt-4o",
}

_GITHUB_MODELS_BASE_URL = "https://models.inference.ai.azure.com"

_VALID_PROVIDERS = ("claude", "bedrock", "copilot")


class ClaudeCliModel(DeepEvalBaseLLM):
    """DeepEval LLM that shells out to the claude -p CLI.

    Uses the local Claude Code installation for both eval execution and GEval
    grading — no API key required. The claude CLI must be installed and
    authenticated (run `claude login` if not already done).
    """

    def __init__(self, model: Optional[str] = None):
        # Store model ID before super().__init__ overwrites self.model via load_model().
        self._model_id = model
        super().__init__(model)

    def load_model(self):
        return self

    def get_model_name(self) -> str:
        return self.name

    def generate(
        self, prompt: str, schema=None
    ) -> Tuple[Union[str, object], float]:
        text = self._run_claude(prompt)
        if schema is None:
            return text, 0.0
        from deepeval.models.llms.utils import trim_and_load_json
        return schema.model_validate(trim_and_load_json(text)), 0.0

    async def a_generate(
        self, prompt: str, schema=None
    ) -> Tuple[Union[str, object], float]:
        import asyncio
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: self.generate(prompt, schema))

    def _run_claude(self, prompt: str) -> str:
        cmd = ["claude", "-p", prompt]
        if self._model_id:
            cmd += ["--model", self._model_id]
        env = claude_subprocess_env()
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            raise RuntimeError(
                f"claude -p exited {result.returncode}: {result.stderr[:300]}"
            )
        return result.stdout.strip()


def _get_github_token() -> str:
    """Return a GitHub token from `gh auth token` or GITHUB_TOKEN env var."""
    result = subprocess.run(
        ["gh", "auth", "token"], capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    raise EnvironmentError(
        "No GitHub token found. Either:\n"
        "  • Run `gh auth login` to authenticate the GitHub CLI, or\n"
        "  • Set GITHUB_TOKEN to a personal access token with model access."
    )


def get_model(
    provider: str,
    model: Optional[str] = None,
    region: Optional[str] = None,
):
    """Return a DeepEval-compatible model instance for the given provider.

    Args:
        provider: One of "claude", "bedrock", or "copilot".
        model: Override the model ID. For claude, falls back to the CLI default.
               For bedrock/copilot, falls back to DEFAULT_MODELS[provider].
        region: AWS region (bedrock only). Falls back to AWS_BEDROCK_REGION env var.

    Raises:
        ValueError: Unknown provider.
        EnvironmentError: Required env var or credential is missing.
    """
    if provider not in _VALID_PROVIDERS:
        raise ValueError(
            f"Unknown provider: {provider!r}. Choose from: {', '.join(_VALID_PROVIDERS)}"
        )

    model_id = model or DEFAULT_MODELS.get(provider)  # None is valid for claude

    if provider == "claude":
        return ClaudeCliModel(model=model_id)

    elif provider == "bedrock":
        from deepeval.models.llms.amazon_bedrock_model import AmazonBedrockModel

        resolved_region = (
            region
            or os.environ.get("AWS_BEDROCK_REGION")
            or os.environ.get("AWS_DEFAULT_REGION")
        )
        if not resolved_region:
            raise EnvironmentError(
                "AWS region not configured. "
                "Pass --region <region> or set AWS_BEDROCK_REGION / AWS_DEFAULT_REGION."
            )
        # Credentials: no explicit keys passed here — boto3 falls back to its
        # default chain (env vars, ~/.aws/credentials, instance profile, SSO, etc.)
        return AmazonBedrockModel(model=model_id, region=resolved_region)

    elif provider == "copilot":
        from deepeval.models.llms.litellm_model import LiteLLMModel

        api_key = _get_github_token()
        # GitHub Models is an OpenAI-compatible endpoint. LiteLLM routes to it
        # via the "github/" prefix. Only add the prefix for bare model names
        # (e.g., "gpt-4o"); leave namespaced IDs (e.g., "github/gpt-4o",
        # "openai/gpt-4o") unchanged so callers can control LiteLLM routing.
        prefixed = f"github/{model_id}" if "/" not in model_id else model_id
        return LiteLLMModel(
            model=prefixed,
            api_key=api_key,
            base_url=_GITHUB_MODELS_BASE_URL,
        )

    else:
        raise ValueError(
            f"Unknown provider: {provider!r}. Choose from: claude, bedrock, copilot"
        )
