"""家庭旅行规划师 - 数据模型"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class TravelPreference(str, Enum):
    NATURE = "自然"
    CITY = "城市"
    CULTURE = "文化"
    BEACH = "海边"
    THEME_PARK = "主题乐园"


class AccommodationLevel(str, Enum):
    ECONOMIC = "经济"
    COMFORTABLE = "舒适"
    LUXURY = "豪华"


class ChildInterest(str, Enum):
    ANIMALS = "动物"
    PLAYGROUND = "游乐"
    MUSEUM = "博物馆"
    NATURE = "自然"


@dataclass
class Destination:
    name: str
    suitability_score: float
    key_attractions: List[str]
    recommended_days: int
    budget_estimate: Dict[str, int]


@dataclass
class DailyItinerary:
    day: int
    morning: str
    afternoon: str
    evening: str
    tips: List[str]


@dataclass
class BudgetBreakdown:
    transportation: int
    accommodation: int
    food: int
    tickets: int
    shopping: int
    emergency: int


@dataclass
class KidFriendlyAttraction:
    name: str
    age_suitability: str
    duration: str
    notes: List[str]
    interest_tags: List[str] = field(default_factory=list)


@dataclass
class PackingList:
    clothing: List[str]
    toiletries: List[str]
    medication: List[str]
    documents: List[str]
    electronics: List[str] = field(default_factory=list)
    kid_items: List[str] = field(default_factory=list)


@dataclass
class FamilyTripRequest:
    """用户旅行请求"""
    destination: Optional[str] = None
    time_range: Optional[str] = None
    days: Optional[int] = None
    budget: Optional[int] = None
    child_ages: List[int] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)
    accommodation_level: str = "舒适"
    food_preference: str = "普通"
    interests: List[str] = field(default_factory=list)
    special_needs: List[str] = field(default_factory=list)


@dataclass
class FamilyTripResponse:
    """旅行规划响应"""
    destinations: List[Destination] = field(default_factory=list)
    daily_itinerary: List[DailyItinerary] = field(default_factory=list)
    budget_breakdown: Optional[BudgetBreakdown] = None
    kid_friendly_attractions: List[KidFriendlyAttraction] = field(default_factory=list)
    packing_list: Optional[PackingList] = None
    error: Optional[str] = None
