from pathlib import Path
import re

PAGES = {
    "1 Harvey_Prompt_Library_Management_Studio.html": "resources/1_Prompt_Library.pdf",
    "2 Harvey_Build_Workflow_Automation_Studio.html": "resources/2_Workflows_Build.pdf",
    "Harvey_Teaching Materials_Walkthrough.html": "resources/3_Teaching_Materials.pdf",
}

CSS_MARKER = "/* studio-toolbar-consistency-fix */"
CSS_FIX = r'''
/* studio-toolbar-consistency-fix */
.topbar { align-items: start !important; }
.toolbar {
  align-self: start !important;
  align-items: center !important;
  align-content: flex-start !important;
}
.topbar .toolbar .btn {
  height: 42px !important;
  min-height: 42px !important;
  max-height: 42px !important;
  align-self: flex-start !important;
  white-space: nowrap;
}
'''

TOOLBAR = r'''<div class="toolbar" aria-label="Page controls">
  <a class="btn ghost" href="{source}">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><path d="M14 2v6h6"></path></svg>
    Source PDF
  </a>
  <button class="btn secondary" type="button" id="themeToggle">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 15.3A8.2 8.2 0 0 1 8.7 4a8.3 8.3 0 1 0 11.3 11.3z"></path></svg>
    Dark mode
  </button>
  <button class="btn ghost" type="button" id="printButton">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9V3h12v6"></path><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><path d="M6 14h12v7H6z"></path></svg>
    Print / PDF
  </button>
  <a class="btn ghost" href="index.html">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11l9-8 9 8"></path><path d="M5 10v10h14V10"></path></svg>
    Home
  </a>
</div>'''

# These pages intentionally use a common header pattern. The first toolbar
# contains no nested divs, so replacing through its closing div is bounded.
TOOLBAR_RE = re.compile(r'<div class="toolbar"(?:\s+aria-label="Page controls")?>.*?</div>', re.S)

for filename, source in PAGES.items():
    path = Path(filename)
    text = path.read_text(encoding="utf-8")

    if CSS_MARKER not in text:
        if "</style>" not in text:
            raise RuntimeError(f"No </style> found in {filename}")
        text = text.replace("</style>", CSS_FIX + "\n</style>", 1)

    replacement = TOOLBAR.format(source=source)
    text, count = TOOLBAR_RE.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"Expected exactly one top toolbar in {filename}; found {count}")

    path.write_text(text, encoding="utf-8")
    print(f"updated {filename}")
