from enum import Enum


class Timeframe(Enum):
    MINUTE = ['m', 60 * 1000]
    HOUR = ['h', 3600 * 1000]
    DAY = ['d', 86400 * 1000]

