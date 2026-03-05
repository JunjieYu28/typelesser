"""Single navigation item for the sidebar."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

from src.constants import NavPage


class NavItem(QPushButton):
    """A sidebar navigation button that emits its associated page on click."""

    page_requested = Signal(NavPage)

    # Unicode icons as stand-ins (will be replaced with proper icons later)
    _ICONS = {
        NavPage.HOME: "\U0001F3E0",        # 🏠
        NavPage.HISTORY: "\U0001F553",      # 🕓
        NavPage.DICTIONARY: "\U0001F4D6",   # 📖
    }
    _LABELS = {
        NavPage.HOME: "首页",
        NavPage.HISTORY: "历史记录",
        NavPage.DICTIONARY: "词典",
    }

    def __init__(self, page: NavPage, parent=None):
        super().__init__(parent)
        self._page = page
        self.setText(f"  {self._ICONS.get(page, '')}  {self._LABELS.get(page, '')}")
        self.setProperty("class", "navItem")
        self.setFixedHeight(44)
        self.setCursor(self.cursor())
        self.setCheckable(False)
        self.clicked.connect(lambda: self.page_requested.emit(self._page))

    @property
    def page(self) -> NavPage:
        return self._page

    def set_active(self, active: bool) -> None:
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)
