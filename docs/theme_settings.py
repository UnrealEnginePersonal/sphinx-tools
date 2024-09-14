from typing import Dict, List


class ThemeSettings:

    def __init__(self, theme_name: str,
                 theme_options: Dict[str, str],
                 html_context: Dict[str, str] = None,
                 custom_css: List[str] = None,
                 show_copyright: bool = True
                 ) -> None:
        self.show_copyright = show_copyright
        self.theme_name = theme_name
        self.theme_options = theme_options
        self.html_context = html_context
        self.custom_css = custom_css


GroundWork = ThemeSettings(
    'ground_work',
    theme_options={
    },
    html_context={
    },
    custom_css=[
    ],
    show_copyright=True
)

Book = ThemeSettings(
    'sphinx_book_theme',
    theme_options={
        "repository_url": "https://github.com/kiwi-lang/Documentation"
    },
    html_context={
        "default_mode": "light"
    },
    custom_css=[
        'sphinx_book_theme_custom.css'
    ],
    show_copyright=True
)

CURRENT_THEME: ThemeSettings = Book
