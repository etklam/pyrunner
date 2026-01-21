"""
爬蟲模組
用於抓取香港房委會公屋配房狀態資料
"""

import json
import re
import requests
from datetime import datetime
from typing import Optional, Dict, Any

from public_house.config import ScraperConfig, ApplicationType, Region, setup_logging
from public_house.exceptions import DataFetchError, DataParseError

logger = setup_logging()


class HousingAllocationScraper:
    """公屋配房狀態爬蟲"""

    def __init__(self):
        self.base_url = ScraperConfig.BASE_URL
        self.url = ScraperConfig.STATUS_URL
        self.headers = ScraperConfig.REQUEST_HEADERS
        self.timeout = ScraperConfig.REQUEST_TIMEOUT

    def crawl(self) -> Optional[Dict[str, Any]]:
        """執行爬蟲任務"""
        logger.info(f"開始爬取網頁: {self.url}")

        try:
            json_data = self._fetch_json_data()

            if json_data:
                all_data = self._parse_json_data(json_data)

                if all_data:
                    logger.info("爬取成功")

                    return {
                        "fetch_date": datetime.now(),
                        "data": all_data,
                        "last_revision_date": json_data.get("LastRevisionDate", ""),
                    }
                else:
                    logger.error("爬取失敗：無法解析配房狀態")
                    return None
            else:
                logger.error("爬取失敗：無法獲取資料")
                return None
        except (DataFetchError, DataParseError):
            logger.error("爬取失敗")
            return None

    def _fetch_json_data(self) -> Optional[Dict[str, Any]]:
        """獲取 JSON 資料"""
        try:
            json_url = ScraperConfig.DATA_URL
            response = requests.get(
                json_url, headers=self.headers, timeout=self.timeout
            )
            response.raise_for_status()
            response.encoding = "utf-8"

            match = re.search(
                r"var ALLOCATION_STATUS = (\{.*\});", response.text, re.DOTALL
            )
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                return data
            else:
                logger.error("無法從回應中提取 JSON 資料")
                raise DataParseError("無法從回應中提取 JSON 資料")

        except requests.RequestException as e:
            logger.error(f"獲取 JSON 資料失敗: {e}")
            raise DataFetchError(f"獲取 JSON 資料失敗: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"解析 JSON 失敗: {e}")
            raise DataParseError(f"解析 JSON 失敗: {e}")

    def _parse_json_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析 JSON 資料，包含三組申請類別"""
        try:
            app_map = json_data.get("DATA", {}).get("applicationNumberMap", {})
            lowest_quota_map = json_data.get("DATA", {}).get("lowestQuotaMap", {})
            quota = json_data.get("DATA", {}).get("quota", "")

            logger.info("applicationNumberMap: %s", app_map)
            logger.info("lowestQuotaMap: %s", lowest_quota_map)
            logger.info("quota: %s", quota)

            # 一般家庭：包含市區、擴展市區、新界、離島四個區域
            # GIUB=市區, GIEB=擴展市區, GINT=新界, GIIS=離島
            general_family = {
                "詳細資格審查": {
                    "2人": {
                        Region.URBAN: app_map.get("GIUB02", ""),
                        Region.EXTENDED_URBAN: app_map.get("GIEB02", ""),
                        Region.NEW_TERRITORIES: app_map.get("GINT02", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GIIS02", ""),
                    },
                    "3人": {
                        Region.URBAN: app_map.get("GIUB03", ""),
                        Region.EXTENDED_URBAN: app_map.get("GIEB03", ""),
                        Region.NEW_TERRITORIES: app_map.get("GINT03", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GIIS03", ""),
                    },
                    "4人": {
                        Region.URBAN: app_map.get("GIUB04", ""),
                        Region.EXTENDED_URBAN: app_map.get("GIEB04", ""),
                        Region.NEW_TERRITORIES: app_map.get("GINT04", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GIIS04", ""),
                    },
                    "5人": {
                        Region.URBAN: app_map.get("GIUB05", ""),
                        Region.EXTENDED_URBAN: app_map.get("GIEB05", ""),
                        Region.NEW_TERRITORIES: app_map.get("GINT05", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GIIS05", ""),
                    },
                    "6人": {
                        Region.URBAN: app_map.get("GIUB06", ""),
                        Region.EXTENDED_URBAN: app_map.get("GIEB06", ""),
                        Region.NEW_TERRITORIES: app_map.get("GINT06", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GIIS06", ""),
                    },
                    "7人或以上": {
                        Region.URBAN: app_map.get("GIUB07", ""),
                        Region.EXTENDED_URBAN: app_map.get("GIEB07", ""),
                        Region.NEW_TERRITORIES: app_map.get("GINT07", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GIIS07", ""),
                    },
                },
                "已接受配房": {
                    "2人": {
                        Region.URBAN: app_map.get("GAUB02", ""),
                        Region.EXTENDED_URBAN: app_map.get("GAEB02", ""),
                        Region.NEW_TERRITORIES: app_map.get("GANT02", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GAIS02", ""),
                    },
                    "3人": {
                        Region.URBAN: app_map.get("GAUB03", ""),
                        Region.EXTENDED_URBAN: app_map.get("GAEB03", ""),
                        Region.NEW_TERRITORIES: app_map.get("GANT03", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GAIS03", ""),
                    },
                    "4人": {
                        Region.URBAN: app_map.get("GAUB04", ""),
                        Region.EXTENDED_URBAN: app_map.get("GAEB04", ""),
                        Region.NEW_TERRITORIES: app_map.get("GANT04", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GAIS04", ""),
                    },
                    "5人": {
                        Region.URBAN: app_map.get("GAUB05", ""),
                        Region.EXTENDED_URBAN: app_map.get("GAEB05", ""),
                        Region.NEW_TERRITORIES: app_map.get("GANT05", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GAIS05", ""),
                    },
                    "6人": {
                        Region.URBAN: app_map.get("GAUB06", ""),
                        Region.EXTENDED_URBAN: app_map.get("GAEB06", ""),
                        Region.NEW_TERRITORIES: app_map.get("GANT06", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GAIS06", ""),
                    },
                    "7人或以上": {
                        Region.URBAN: app_map.get("GAUB07", ""),
                        Region.EXTENDED_URBAN: app_map.get("GAEB07", ""),
                        Region.NEW_TERRITORIES: app_map.get("GANT07", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("GAIS07", ""),
                    },
                },
            }

            # 高齡人士優先：包含市區、擴展市區、新界、離島四個區域
            elderly_priority = {
                "詳細資格審查": {
                    "1人": {
                        Region.URBAN: app_map.get("EIUB01", ""),
                        Region.EXTENDED_URBAN: app_map.get("EIEB01", ""),
                        Region.NEW_TERRITORIES: app_map.get("EINT01", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("EIIS01", ""),
                    },
                    "2人": {
                        Region.URBAN: app_map.get("EIUB02", ""),
                        Region.EXTENDED_URBAN: app_map.get("EIEB02", ""),
                        Region.NEW_TERRITORIES: app_map.get("EINT02", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("EIIS02", ""),
                    },
                    "3人": {
                        Region.URBAN: app_map.get("EIUB03", ""),
                        Region.EXTENDED_URBAN: app_map.get("EIEB03", ""),
                        Region.NEW_TERRITORIES: app_map.get("EINT03", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("EIIS03", ""),
                    },
                },
                "已接受配房": {
                    "1人": {
                        Region.URBAN: app_map.get("EAUB01", ""),
                        Region.EXTENDED_URBAN: app_map.get("EAEB01", ""),
                        Region.NEW_TERRITORIES: app_map.get("EANT01", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("EAIS01", ""),
                    },
                    "2人": {
                        Region.URBAN: app_map.get("EAUB02", ""),
                        Region.EXTENDED_URBAN: app_map.get("EAEB02", ""),
                        Region.NEW_TERRITORIES: app_map.get("EANT02", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("EAIS02", ""),
                    },
                    "3人": {
                        Region.URBAN: app_map.get("EAUB03", ""),
                        Region.EXTENDED_URBAN: app_map.get("EAEB03", ""),
                        Region.NEW_TERRITORIES: app_map.get("EANT03", ""),
                        Region.OUTLYING_ISLANDS: app_map.get("EAIS03", ""),
                    },
                },
            }

            single_person = {
                "正獲安排詳細資格審查": {
                    "最低分數": quota,
                },
                "已接受配房": {
                    Region.URBAN: lowest_quota_map.get("UB", ""),
                    Region.EXTENDED_URBAN: lowest_quota_map.get("EB", ""),
                    Region.NEW_TERRITORIES: lowest_quota_map.get("NT", ""),
                    Region.OUTLYING_ISLANDS: lowest_quota_map.get("IS", ""),
                },
            }

            return {
                ApplicationType.GENERAL_FAMILY: general_family,
                ApplicationType.ELDERLY_PRIORITY: elderly_priority,
                ApplicationType.SINGLE_PERSON: single_person,
            }

        except Exception as e:
            logger.error(f"解析 JSON 資料失敗: {e}")
            raise DataParseError(f"解析 JSON 資料失敗: {e}")
