import json
from pathlib import Path
from typing import Any


class Translator:
    def __init__(self, locales_dir: Path, lang: str = "en"):
        self._lang = lang
        self._locales_dir = locales_dir
        self._cache: dict[str, dict[str, Any]] = {}
        self.load_locales()

    def load_locales(self) -> None:
        """Загружает все языковые файлы в оперативную память при старте."""
        for file_path in self._locales_dir.glob("*.json"):
            lang_code = file_path.stem
            with open(file_path, "r", encoding="utf-8") as f:
                self._cache[lang_code] = json.load(f)
        print(f"🌍 Загружены локализации для языков: {list(self._cache.keys())}")

    def _get_lang_data(self, priority_lang: str = None):
        lang = priority_lang or self._lang
        return self._cache.get(lang, self._cache.get("en", {}))

    def get(self, key: str, priority_lang: str = None,
            **kwargs: Any) -> str | dict[str, str]:
        """
        Достает текст из кэша по точечной нотации и подставляет аргументы.
        """
        lang_data = self._get_lang_data(priority_lang)
        keys = key.split(".")
        val = lang_data

        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                val = None
                break

        if not val:
            return f"[{key}]"

        # Если есть переменные для подстановки, форматируем строку
        if kwargs and isinstance(val, str):
            return val.format(**kwargs)

        return val


LOCALES_PATH = Path("app/core/locales")
i18n = Translator(LOCALES_PATH)
