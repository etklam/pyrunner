"""
異常處理模組
定義爬蟲相關的自定義異常
"""


class DataFetchError(Exception):
    """數據獲取異常"""

    pass


class DataParseError(Exception):
    """數據解析異常"""

    pass
