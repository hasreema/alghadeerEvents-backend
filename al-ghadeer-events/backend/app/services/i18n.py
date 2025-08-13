from typing import Dict

from app.core.config import settings


TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "monthly_report": "Monthly Report",
        "total_revenue": "Total Revenue",
        "total_expenses": "Total Expenses",
        "total_labor": "Total Labor",
        "total_profit": "Total Profit",
    },
    "he": {
        "monthly_report": "דוח חודשי",
        "total_revenue": "סה\"כ הכנסות",
        "total_expenses": "סה\"כ הוצאות",
        "total_labor": "סה\"כ עבודה",
        "total_profit": "סה\"כ רווח",
    },
    "ar": {
        "monthly_report": "تقرير شهري",
        "total_revenue": "إجمالي الإيرادات",
        "total_expenses": "إجمالي المصروفات",
        "total_labor": "إجمالي العمل",
        "total_profit": "إجمالي الربح",
    },
}

RTL_LANGS = {"he", "ar"}


def t(key: str, lang: str = None) -> str:
    lang = lang or settings.default_language
    if lang not in settings.supported_languages:
        lang = settings.default_language
    return TRANSLATIONS.get(lang, TRANSLATIONS[settings.default_language]).get(key, key)


def is_rtl(lang: str = None) -> bool:
    lang = lang or settings.default_language
    return lang in RTL_LANGS