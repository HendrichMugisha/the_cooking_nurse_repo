import asyncio
from playwright.async_api import async_playwright

async def check_page(page, url, name):
    print(f"\n--- Checking {name} at {url} ---")
    errors = []
    
    # Catch console errors
    page.on("pageerror", lambda exc: errors.append(f"Uncaught exception: {exc}"))
    page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type in ["error", "warning"] else None)

    response = await page.goto(url)
    if not response or response.status >= 400:
        print(f"[!] HTTP Error: {response.status if response else 'No Response'}")
    else:
        print(f"[OK] Page loaded with status 200")
        
    # Wait for network idle
    try:
        await page.wait_for_load_state("networkidle", timeout=5000)
    except:
        pass

    # Check for empty content
    content = await page.content()
    if len(content) < 500:
        print("[!] Warning: Page content seems too short/empty.")

    # Check for broken links
    links = await page.locator("a").all()
    broken_links = 0
    for link in links:
        href = await link.get_attribute("href")
        if href and (href.startswith("http") or href.startswith("/")) and href != "#":
            # Just collect them, checking them all takes too long, but we can report how many links exist
            pass
    print(f"[OK] Found {len(links)} links on the page.")

    # Check for any visible error toasts or messages
    error_alerts = await page.locator(".bg-error-container, .text-error").all_inner_texts()
    if error_alerts:
        print(f"[!] Found potential error UI elements: {error_alerts[:2]}")

    if errors:
        print(f"[!] Console/JS issues found:")
        for e in errors[:5]:
            print(f"    - {e}")
    else:
        print("[OK] No console errors detected.")

async def main():
    base_url = "http://127.0.0.1:8000"
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(channel="msedge", headless=True)
        except Exception:
            browser = await p.chromium.launch(headless=True)
        
        print("\n==========================================")
        print("  DESKTOP BROWSER CHECK (1920x1080)")
        print("==========================================")
        context_desktop = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page_desktop = await context_desktop.new_page()
        
        pages_to_check = [
            ("/", "Home Page"),
            ("/shop/", "Shop Page"),
            ("/classes/", "Classes Timetable"),
            ("/cart/", "Shopping Cart"),
            ("/users/dashboard/", "Customer Dashboard"),
        ]
        
        for path, name in pages_to_check:
            await check_page(page_desktop, f"{base_url}{path}", name)
            
        print("\n==========================================")
        print("  MOBILE BROWSER CHECK (390x844 - iPhone 12)")
        print("==========================================")
        context_mobile = await browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        )
        page_mobile = await context_mobile.new_page()
        
        for path, name in pages_to_check:
            await check_page(page_mobile, f"{base_url}{path}", name)
            
        await browser.close()
        print("\nBrowser check completed.")

if __name__ == "__main__":
    asyncio.run(main())
