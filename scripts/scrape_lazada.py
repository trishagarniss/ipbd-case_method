"""
File: scrape_lazada.py
Tujuan: Menarik data produk skincare dari Lazada.
Status: Tahap Kerangka Dasar (Skeleton).
"""

import asyncio
from playwright.async_api import async_playwright

async def scrape_lazada_skincare():
    
    hasil_scraping = []
    
    async with async_playwright() as p:
        
        # TODO 1: BUKA BROWSER
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # TODO 2: URL TARGET (LAZADA)
        url = "https://www.lazada.co.id/catalog/?q=moisturizer"
        print(f"Lagi buka Lazada nih: {url}")
        
        await page.goto(url)
        
        # TODO 3: JEDA LOADING
        # Lazada lumayan berat, kasih waktu loading yang cukup
        print("Nunggu loading halaman Lazada...")
        await page.wait_for_timeout(6000)
        
        # TODO 4: SCROLL TIPIS-TIPIS
        # Lazada kadang butuh scroll sedikit biar produk di bawahnya ikut ke-render
        print("Scroll tipis biar gambar muncul...")
        await page.mouse.wheel(0, 800)
        await page.wait_for_timeout(2000)
        
        # TODO 5: CARI PEMBUNGKUS KOTAK PRODUK (INSPECT ELEMENT)
        # Buka Lazada di Chrome biasa -> Inspect Element.
        # Biasanya Lazada pakai atribut seperti data-qa-locator="product-item"
        print("Mencoba mencari kotak produk...")
        products = await page.query_selector_all('[data-qa-locator="product-item"]') # <- Ini tebakan awal
        
        print(f"Ketemu {len(products)} kotak produk di halaman ini.")
        
        # TODO 6: AMBIL TEKS MENTAH
        for product in products[:5]:
            teks_mentah = await product.inner_text()
            
            hasil_scraping.append({
                "platform": "Lazada",
                "data_mentah": teks_mentah
            })
            
        # TODO 7: TUTUP BROWSER
        await browser.close()
        
    return hasil_scraping

# Blok Testing Lokal
if __name__ == "__main__":
    print("--- MULAI TESTING SCRAPER LAZADA ---")
    hasil = asyncio.run(scrape_lazada_skincare())
    
    print("\nIni hasil tarikannya:")
    for item in hasil:
        print(item)
        print("-" * 30)