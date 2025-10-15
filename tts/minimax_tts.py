"""MiniMax Text-to-Speech integration utilities."""

from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import requests
from dotenv import load_dotenv


class MiniMaxTTSError(RuntimeError):
    """Raised when the MiniMax TTS service returns an error."""


@dataclass
class MiniMaxTTSConfig:
    """Configuration for the MiniMax TTS client."""

    api_key: str
    group_id: Optional[str] = None
    model: str = "speech-01"
    voice_id: str = "female-qn-fantasy"
    speed: float = 1.0
    volume: float = 1.0
    pitch: float = 1.05
    emotion: Optional[str] = "positive"
    sample_rate: int = 24000
    format: str = "mp3"
    timeout: int = 30
    base_url: str = "https://api.minimax.chat/v1/text_to_speech"


def _load_default_config() -> MiniMaxTTSConfig:
    """Load default configuration values from environment variables."""

    load_dotenv()

    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise MiniMaxTTSError(
            "MINIMAX_API_KEY 未设置。请在环境变量或 .env 文件中配置 MiniMax API 密钥。"
        )

    return MiniMaxTTSConfig(
        api_key=api_key,
        group_id=os.getenv("MINIMAX_GROUP_ID"),
        model=os.getenv("MINIMAX_TTS_MODEL", "speech-01"),
        voice_id=os.getenv("MINIMAX_TTS_VOICE", "female-qn-fantasy"),
        speed=float(os.getenv("MINIMAX_TTS_SPEED", 1.0)),
        volume=float(os.getenv("MINIMAX_TTS_VOLUME", 1.05)),
        pitch=float(os.getenv("MINIMAX_TTS_PITCH", 1.05)),
        emotion=os.getenv("MINIMAX_TTS_EMOTION", "positive"),
        sample_rate=int(os.getenv("MINIMAX_TTS_SAMPLE_RATE", 24000)),
        format=os.getenv("MINIMAX_TTS_FORMAT", "mp3"),
        timeout=int(os.getenv("MINIMAX_TTS_TIMEOUT", 30)),
        base_url=os.getenv("MINIMAX_TTS_URL", "https://api.minimax.chat/v1/text_to_speech"),
    )


class MiniMaxTTSClient:
    """Client for calling the MiniMax Text-to-Speech API."""

    def __init__(self, config: Optional[MiniMaxTTSConfig] = None):
        self.config = config or _load_default_config()
        self.session = requests.Session()

    # Public API -----------------------------------------------------------------
    def synthesize(
        self,
        text: str,
        *,
        voice_id: Optional[str] = None,
        emotion: Optional[str] = None,
        speed: Optional[float] = None,
        pitch: Optional[float] = None,
        volume: Optional[float] = None,
        model: Optional[str] = None,
        response_format: Optional[str] = None,
    ) -> Tuple[bytes, Dict[str, Any]]:
        """Convert text into speech using the MiniMax API.

        Returns a tuple containing the audio bytes and metadata that can be used for
        debugging or logging (does not include sensitive information).
        """

        payload = self._build_payload(
            text=text,
            voice_id=voice_id,
            emotion=emotion,
            speed=speed,
            pitch=pitch,
            volume=volume,
            model=model,
            response_format=response_format,
        )
        headers = self._build_headers()

        try:
            response = self.session.post(
                self.config.base_url,
                headers=headers,
                json=payload,
                timeout=self.config.timeout,
            )
        except requests.RequestException as exc:  # pragma: no cover - network failure
            raise MiniMaxTTSError(f"调用 MiniMax TTS API 失败: {exc}") from exc

        if response.status_code != 200:
            message = self._extract_error_message(response)
            raise MiniMaxTTSError(
                f"MiniMax TTS API 返回错误 (status={response.status_code}): {message}"
            )

        data = response.json()
        audio_bytes = self._decode_audio(data)
        metadata = {
            "request_payload": {k: v for k, v in payload.items() if k != "text"},
            "response_fields": {k: v for k, v in data.items() if k != "audio_base64"},
        }
        return audio_bytes, metadata

    def generate_voiceover(
        self,
        strategy_text: str,
        *,
        intro: Optional[str] = None,
        outro: Optional[str] = None,
        voice_id: Optional[str] = None,
        emotion: Optional[str] = None,
        speed: Optional[float] = None,
        pitch: Optional[float] = None,
        volume: Optional[float] = None,
        model: Optional[str] = None,
        response_format: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an engaging voiceover for the supplied strategy text."""

        script = build_engaging_voiceover_script(strategy_text, intro=intro, outro=outro)
        audio_bytes, metadata = self.synthesize(
            script,
            voice_id=voice_id,
            emotion=emotion,
            speed=speed,
            pitch=pitch,
            volume=volume,
            model=model,
            response_format=response_format,
        )
        return {
            "script": script,
            "audio_bytes": audio_bytes,
            "metadata": metadata,
        }

    # Internal helpers -----------------------------------------------------------
    def _build_headers(self) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        if self.config.group_id:
            headers["X-Group-Id"] = self.config.group_id
        return headers

    def _build_payload(
        self,
        *,
        text: str,
        voice_id: Optional[str],
        emotion: Optional[str],
        speed: Optional[float],
        pitch: Optional[float],
        volume: Optional[float],
        model: Optional[str],
        response_format: Optional[str],
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model or self.config.model,
            "text": text,
            "voice_id": voice_id or self.config.voice_id,
            "speed": speed or self.config.speed,
            "volume": volume or self.config.volume,
            "pitch": pitch or self.config.pitch,
            "sample_rate": self.config.sample_rate,
            "format": response_format or self.config.format,
        }
        if emotion or self.config.emotion:
            payload["emotion"] = emotion or self.config.emotion
        return payload

    @staticmethod
    def _decode_audio(data: Dict[str, Any]) -> bytes:
        if "audio_base64" in data:
            return base64.b64decode(data["audio_base64"])

        if "data" in data and isinstance(data["data"], dict):
            audio = data["data"].get("audio")
            if isinstance(audio, str):
                return base64.b64decode(audio)

        raise MiniMaxTTSError("MiniMax TTS API 响应中未找到音频数据。")

    @staticmethod
    def _extract_error_message(response: requests.Response) -> str:
        try:
            payload = response.json()
        except ValueError:
            return response.text
        return payload.get("message") or payload.get("error") or json.dumps(payload, ensure_ascii=False)


def build_engaging_voiceover_script(
    strategy_text: str,
    *,
    intro: Optional[str] = None,
    outro: Optional[str] = None,
) -> str:
    """Create a lively narration script from the generated strategy text."""

    intro_line = intro or "嗨，欢迎来到米塔视界！我马上为你揭晓专属策略亮点。"
    outro_line = outro or "期待你带着这份策略，闪耀整个展台！"

    sections = []
    current_section: Optional[str] = None
    for raw_line in strategy_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("---"):
            continue
        if line.startswith("**") and line.endswith("**"):
            current_section = line.strip("* ").replace(":", "").replace("：", "")
            continue
        normalized = line.lstrip("*-• ")
        if current_section:
            sections.append(f"{current_section}：{normalized}")
        else:
            sections.append(normalized)

    body_lines = []
    for item in sections:
        if len(item) <= 2:
            continue
        body_lines.append(item)

    body_text = "；".join(body_lines)
    if body_text:
        body_text += "。"

    script = f"{intro_line}{body_text}{outro_line}"
    return script
