from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlencode

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass(frozen=True)
class Language:
    code: str
    name: str


LANGUAGES: dict[str, Language] = {
    "1": Language("zh-TW", "Chinese (Traditional)"),
    "2": Language("en", "English"),
    "3": Language("fr", "French"),
    "4": Language("de", "German"),
    "5": Language("es", "Spanish"),
    "6": Language("ru", "Russian"),
    "7": Language("it", "Italian"),
    "8": Language("ko", "Korean"),
    "9": Language("ja", "Japanese"),
}


class GoogleTranslateClient:
    """Small Selenium client for the Google Translate web UI."""

    BASE_URL = "https://translate.google.com/"
    RESULT_LOCATORS = (
        (By.CSS_SELECTOR, "span[jsname='W297wb']"),
        (By.CSS_SELECTOR, "[data-language-for-alternatives]"),
    )

    def __init__(self, *, headless: bool = True, wait_seconds: int = 10) -> None:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")

        # Selenium Manager (Selenium 4.6+) resolves ChromeDriver automatically.
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, wait_seconds)

    def __enter__(self) -> GoogleTranslateClient:
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def close(self) -> None:
        self.driver.quit()

    def translate(self, text: str, target: Language) -> str:
        if not text.strip():
            raise ValueError("Text must not be empty")

        query = urlencode({"sl": "auto", "tl": target.code, "op": "translate"})
        self.driver.get(f"{self.BASE_URL}?{query}")

        source = self.wait.until(EC.element_to_be_clickable((By.TAG_NAME, "textarea")))
        source.clear()
        source.send_keys(text)

        translated = self.wait.until(self._find_translation)
        return translated

    def _find_translation(self, _driver) -> str | bool:
        for by, value in self.RESULT_LOCATORS:
            for element in self.driver.find_elements(by, value):
                text = element.text.strip()
                if text:
                    return text
        return False


class TranslationCLI:
    def __init__(
        self,
        client_factory: Callable[[], GoogleTranslateClient] = GoogleTranslateClient,
    ) -> None:
        self.client_factory = client_factory

    def run(self) -> None:
        print("Google Translate CLI\n")

        try:
            with self.client_factory() as client:
                while True:
                    target = self._select_language()
                    if target is None:
                        return

                    text = input(
                        f"Translate into {target.name}.\n"
                        "Text (or leave blank to cancel): "
                    ).strip()
                    if not text:
                        continue

                    try:
                        result = client.translate(text, target)
                    except (ValueError, WebDriverException) as exc:
                        print(f"Translation failed: {exc}\n")
                        continue

                    print(f"\n{result}\n")
                    if input("Press Enter to continue, or q to quit: ").strip().lower() == "q":
                        return
        except WebDriverException as exc:
            print(f"Could not start Chrome: {exc}")

    @staticmethod
    def _select_language() -> Language | None:
        menu = "\n".join(
            f"{number}. {language.name}" for number, language in LANGUAGES.items()
        )

        while True:
            selection = input(f"Target language:\n{menu}\nq. Quit\n> ").strip().lower()
            if selection == "q":
                return None
            if selection in LANGUAGES:
                return LANGUAGES[selection]
            print("Unknown selection. Please choose again.\n")
