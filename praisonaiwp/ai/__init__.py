"""PraisonAI integration for WordPress CLI tool"""

# Check if PraisonAI is available.
#
# `PraisonAIAgents` is a pre-1.0 alias that praisonaiagents only re-exports
# from its package root on recent versions (PraisonAI PR #3675); on older
# versions it lives only at `praisonaiagents.agents`. Import each with a
# fallback so one missing alias does not disable every AI command, and keep
# the real error so the failure message can say what actually went wrong
# instead of blaming a missing install (praisonaiwp-cli#1).
AI_IMPORT_ERROR = None
try:
    from praisonaiagents import Agent, Task
    try:
        from praisonaiagents import PraisonAIAgents
    except ImportError:
        from praisonaiagents.agents import PraisonAIAgents
    AI_AVAILABLE = True
except Exception as _exc:  # ImportError, or OpenAIError when no API key is set
    AI_AVAILABLE = False
    AI_IMPORT_ERROR = f"{type(_exc).__name__}: {_exc}"
    Agent = None
    Task = None
    PraisonAIAgents = None


def check_ai_available():
    """Check if AI features are available"""
    if not AI_AVAILABLE:
        detail = f" (import failed with {AI_IMPORT_ERROR})" if AI_IMPORT_ERROR else ""
        raise ImportError(
            "AI features require praisonaiagents. "
            f"Install with: pip install 'praisonaiwp[ai]'{detail}"
        )
    return True


__all__ = ['AI_AVAILABLE', 'AI_IMPORT_ERROR', 'check_ai_available', 'Agent', 'Task', 'PraisonAIAgents']
