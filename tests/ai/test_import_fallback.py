"""AI availability must survive the PraisonAIAgents alias missing from the root.

praisonaiagents only re-exports the pre-1.0 `PraisonAIAgents` alias from its
package root on recent versions (PraisonAI PR #3675); on 1.6.163 and earlier
it exists only at `praisonaiagents.agents`. praisonaiwp imported it from the
root with a bare try/except, so on those versions every AI command was
disabled with a message blaming a missing install (praisonaiwp-cli#1).
"""
import importlib
import sys
import types

import pytest


def _reload_ai_with(fake_root, fake_agents):
    """Reload praisonaiwp.ai against a stubbed praisonaiagents."""
    saved = {
        name: sys.modules.pop(name)
        for name in list(sys.modules)
        if name == "praisonaiagents" or name.startswith("praisonaiagents.")
    }
    saved_ai = sys.modules.pop("praisonaiwp.ai", None)
    try:
        sys.modules["praisonaiagents"] = fake_root
        sys.modules["praisonaiagents.agents"] = fake_agents
        return importlib.import_module("praisonaiwp.ai")
    finally:
        for name in list(sys.modules):
            if name == "praisonaiagents" or name.startswith("praisonaiagents."):
                del sys.modules[name]
        sys.modules.update(saved)
        if saved_ai is not None:
            sys.modules["praisonaiwp.ai"] = saved_ai
        else:
            sys.modules.pop("praisonaiwp.ai", None)


class _Sentinel:
    pass


def _stub_packages(alias_at_root):
    root = types.ModuleType("praisonaiagents")
    root.Agent = _Sentinel
    root.Task = _Sentinel
    agents = types.ModuleType("praisonaiagents.agents")
    agents.PraisonAIAgents = _Sentinel
    if alias_at_root:
        root.PraisonAIAgents = _Sentinel
    root.agents = agents
    return root, agents


def test_old_praisonaiagents_root_alias_missing_still_available():
    """The 1.6.163-and-earlier layout: alias only under .agents."""
    ai = _reload_ai_with(*_stub_packages(alias_at_root=False))
    assert ai.AI_AVAILABLE is True
    assert ai.PraisonAIAgents is _Sentinel
    assert ai.AI_IMPORT_ERROR is None


def test_new_praisonaiagents_root_alias_present():
    ai = _reload_ai_with(*_stub_packages(alias_at_root=True))
    assert ai.AI_AVAILABLE is True
    assert ai.PraisonAIAgents is _Sentinel


def test_truly_missing_reports_real_error():
    """When the base import fails, the message must carry the actual cause."""
    root = types.ModuleType("praisonaiagents")  # no Agent/Task at all
    agents = types.ModuleType("praisonaiagents.agents")
    ai = _reload_ai_with(root, agents)
    assert ai.AI_AVAILABLE is False
    assert ai.AI_IMPORT_ERROR is not None
    with pytest.raises(ImportError) as exc:
        ai.check_ai_available()
    assert "import failed with" in str(exc.value)
