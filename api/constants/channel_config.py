from typing import Dict, List, Literal

# Channel type definitions
ChannelType = Literal["community", "sns"]

# Supported channels by type
COMMUNITY_CHANNELS = [
    {"key": "reddit", "label": "Reddit (레딧)"},
    {"key": "ppomppu", "label": "뽐뿌"},
    {"key": "dcinside", "label": "디씨인사이드"},
    {"key": "theqoo", "label": "더쿠"},
    {"key": "ruliweb", "label": "루리웹"},
    {"key": "clien", "label": "클리앙"}
]

SNS_CHANNELS = [
    {"key": "instagram", "label": "인스타그램"},
    {"key": "youtube", "label": "유튜브"},
    {"key": "facebook", "label": "페이스북"},
    {"key": "x", "label": "X (구 트위터)"},
    {"key": "threads", "label": "스레드"}
]

# All supported channels
ALL_CHANNELS = COMMUNITY_CHANNELS + SNS_CHANNELS

# Channel type mapping
CHANNEL_TYPES: Dict[str, ChannelType] = {
    **{channel["key"]: "community" for channel in COMMUNITY_CHANNELS},
    **{channel["key"]: "sns" for channel in SNS_CHANNELS}
}

# Channel display names
CHANNEL_NAMES: Dict[str, str] = {
    "reddit": "Reddit",
    "ppomppu": "뽐뿌",
    "dcinside": "디시인사이드",
    "theqoo": "더쿠",
    "ruliweb": "루리웹",
    "clien": "클리앙",
    "instagram": "인스타그램",
    "youtube": "유튜브",
    "facebook": "페이스북",
    "x": "X",
    "threads": "스레드"
}

# 기존 코드와의 호환성을 위한 키 리스트
COMMUNITY_KEYS = [c["key"] for c in COMMUNITY_CHANNELS]
SNS_KEYS = [c["key"] for c in SNS_CHANNELS]
ALL_KEYS = COMMUNITY_KEYS + SNS_KEYS

def is_valid_channel(channel: str) -> bool:
    """
    주어진 채널이 지원되는 채널인지 확인합니다.
    
    Args:
        channel (str): 확인할 채널 이름
        
    Returns:
        bool: 지원되는 채널이면 True, 아니면 False
    """
    return channel in ALL_KEYS

def get_channel_type(channel: str) -> str:
    """
    채널의 유형을 반환합니다.
    
    Args:
        channel (str): 채널 이름
        
    Returns:
        str: "community" 또는 "sns"
    """
    if channel in COMMUNITY_KEYS:
        return "community"
    elif channel in SNS_KEYS:
        return "sns"
    else:
        return "unknown"

def get_channel_label(channel: str) -> str:
    """
    채널의 사용자 표시용 라벨을 반환합니다.
    
    Args:
        channel (str): 채널 키
        
    Returns:
        str: 채널 라벨, 없는 경우 키 반환
    """
    for c in ALL_CHANNELS:
        if c["key"] == channel:
            return c["label"]
    return channel

def format_result_with_channel(channel: str, content: str) -> str:
    """
    채널 라벨을 포함한 결과 문자열을 생성합니다.
    
    Args:
        channel (str): 채널 키
        content (str): 원본 내용
        
    Returns:
        str: 채널 라벨이 포함된 결과 문자열
    """
    label = get_channel_label(channel)
    return f"[{label}] {content}"

def get_supported_channels() -> dict:
    """
    지원되는 모든 채널 정보를 반환합니다.
    
    Returns:
        dict: 커뮤니티와 SNS 채널 정보를 포함한 딕셔너리
    """
    return {
        "community": COMMUNITY_CHANNELS,
        "sns": SNS_CHANNELS
    }

def get_channel_name(channel: str) -> str:
    """
    Get the display name of a channel
    
    Args:
        channel: Channel name
        
    Returns:
        Display name of the channel
        
    Raises:
        ValueError: If channel is not valid
    """
    if not is_valid_channel(channel):
        raise ValueError(f"Invalid channel: {channel}")
    return CHANNEL_NAMES[channel] 