"""
配置模組
包含爬蟲相關的配置設定
"""

from enum import Enum


class ApplicationType(str, Enum):
    """申請類型"""

    GENERAL_FAMILY = "一般家庭"
    ELDERLY_PRIORITY = "高齡人士優先"
    SINGLE_PERSON = "一人公屋"


class Region(str, Enum):
    """區域"""

    URBAN = "市區"
    EXTENDED_URBAN = "擴展市區"
    NEW_TERRITORIES = "新界"
    OUTLYING_ISLANDS = "離島"


class ScraperConfig:
    """爬蟲配置"""

    BASE_URL = "https://www.housingauthority.gov.hk"
    STATUS_URL = "https://www.housingauthority.gov.hk/tc/flat-application/allocation-status/index.html"
    DATA_URL = "https://www.housingauthority.gov.hk/tc/common/js/allocation-status-data.js"
    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    REQUEST_TIMEOUT = 30


def setup_logging():
    """設置日誌記錄"""
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)
