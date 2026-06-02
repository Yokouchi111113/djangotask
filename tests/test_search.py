from playwright.sync_api import sync_playwright

def test_playwright_import():
    assert sync_playwright is not None