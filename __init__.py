from aqt import mw
from aqt.qt import QAction
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QSplitter, QToolBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Class for the sidebar panel with ChatGPT browser
class GPTSidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout settings
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Embedded browser
        self.browser = QWebEngineView(self)
        self.browser.setUrl(QUrl("https://chat.openai.com/"))  # Load ChatGPT page
        layout.addWidget(self.browser)

def create_action(toolbar, text, callback):
    # Creates a button on the toolbar
    action = QAction(text, toolbar)
    action.triggered.connect(callback)
    toolbar.addAction(action)
    return action

def setup_toolbar(sidebar):
    # Creates a toolbar with buttons
    toolbar = QToolBar("ChatGPT Toolbar", sidebar)
    toolbar.setStyleSheet("padding: 2px; background-color: white;")

    # List of buttons with functions
    actions = [
        ("⟵", sidebar.browser.back),
        ("⟶", sidebar.browser.forward),
        ("⟳", sidebar.browser.reload),
        ("＋", lambda: sidebar.browser.setZoomFactor(sidebar.browser.zoomFactor() + 0.1)),
        ("－", lambda: sidebar.browser.setZoomFactor(sidebar.browser.zoomFactor() - 0.1))
    ]

    # Adds buttons to the toolbar
    for text, callback in actions:
        create_action(toolbar, text, callback)

    # Adds a label with the title
    label = QLabel("     ChatGPT     ", toolbar)
    label.setStyleSheet("font-weight: bold; margin-left: 10px; margin-right: 10px;")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    toolbar.addWidget(label)

    return toolbar

def open_chat_sidebar():
    # Creates a sidebar with the ChatGPT browser
    if not hasattr(mw, "chat_sidebar"):
        splitter = QSplitter(Qt.Orientation.Horizontal, mw)
        splitter.addWidget(mw.centralWidget())
        mw.chat_sidebar = GPTSidebar(mw)
        splitter.addWidget(mw.chat_sidebar)
        splitter.setSizes([1000, 600])
        mw.setCentralWidget(splitter)

        toolbar = setup_toolbar(mw.chat_sidebar)
        mw.chat_sidebar.layout().insertWidget(0, toolbar)
    else:
        # Hides or shows the sidebar
        mw.chat_sidebar.setVisible(not mw.chat_sidebar.isVisible())

def init_addon():
    # Adds an option to the Anki menu
    action = QAction("ChatGPT", mw)
    action.triggered.connect(open_chat_sidebar)
    mw.menuBar().addAction(action)

init_addon()

