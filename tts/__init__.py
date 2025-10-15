"""Utility package for speech synthesis integrations."""

from .minimax_tts import MiniMaxTTSClient, MiniMaxTTSError, build_engaging_voiceover_script

__all__ = [
    "MiniMaxTTSClient",
    "MiniMaxTTSError",
    "build_engaging_voiceover_script",
]
