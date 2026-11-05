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

    def get(self, key: str, **kwargs: Any) -> str:
        """Достает текст из кэша по точечной нотации (например: 'start.welcome')

        и подставляет аргументы.
        """
        lang_data = self._cache.get(self._lang, self._cache.get("en", {}))

        # Ищем ключ по уровням (например, "start.welcome" -> start -> welcome)
        keys = key.split(".")
        val = lang_data
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                val = None
                break

        if not val:
            return f"[{key}]"    # Заглушка, если ключ не найден

        # Если есть переменные для подстановки, форматируем строку
        if kwargs and isinstance(val, str):
            return val.format(**kwargs)

        return val


LOCALES_PATH = Path("app/core/locales")
i18n = Translator(LOCALES_PATH)
