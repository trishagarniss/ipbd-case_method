"""
File: scrape_shopee.py
Tujuan: Menarik data produk skincare dari Shopee.
Status: Tahap Kerangka Dasar (Skeleton).
"""

# TODO 1: IMPORT LIBRARY
# Sama persis kayak Tokped, kita butuh asyncio dan async_playwright
import asyncio
from playwright.async_api import async_playwright

# TODO 2: BIKIN FUNGSI UTAMA
# Kasih nama yang jelas, misal 'scrape_shopee_skincare'. Wajib pakai 'async def'.
async def scrape_shopee_skincare():
    
    # Siapkan keranjang (list) buat nampung datanya nanti
    hasil_scraping = []
    
    # Buka sesi Playwright
    async with async_playwright() as p:
        
        # TODO 3: BUKA BROWSER
        # Tetap pakai headless=False dulu biar kelihatan proses loading dan scroll-nya.
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # TODO 4: MASUK KE URL TARGET (SHOPEE)
        url = "https://shopee.co.id/search?keyword=moisturizer"
        print(f"Lagi buka Shopee nih: {url}")
        
        await page.goto(url)
        
        # TODO 5: KASIH JEDA AWAL
        # Shopee kadang agak berat pas pertama buka, kasih waktu loading 5 detik.
        print("Nunggu loading halaman depan...")
        await page.wait_for_timeout(5000)
        
        # TODO 6: TRIK SCROLL BAWAH (LAZY LOADING)
        # Ini WAJIB buat Shopee. Kalau nggak di-scroll, data di bawah bakal kosong.
        print("Mulai scroll ke bawah pelan-pelan biar harganya muncul...")
        # Scroll sejauh 1500 pixel ke bawah
        await page.mouse.wheel(0, 1500) 
        # Kasih jeda 3 detik biar gambarnya selesai dimuat setelah di-scroll
        await page.wait_for_timeout(3000)
        
        # TODO 7: CARI PEMBUNGKUS KOTAK PRODUK (INSPECT ELEMENT)
        # Buka Chrome biasa -> buka Shopee -> Inspect Element.
        # Biasanya Shopee pakai elemen kaya 'div[data-sqe="item"]' atau 'a[data-sqe="link"]'.
        # Kalau udah ketemu nama class atau atributnya, masukkan ke query_selector_all.
        print("Mencoba mencari kotak produk...")
        products = await page.query_selector_all("div[data-sqe='item']") # <- Ini masih tebakan, wajib kamu cek lagi!
        
        print(f"Ketemu {len(products)} kotak produk di halaman ini.")
        
        # TODO 8: AMBIL TEKS DARI TIAP KOTAK
        # Ambil 5 produk pertama dulu buat testing
        for product in products[:5]:
            
            teks_mentah = await product.inner_text()
            
            # TODO 9: SIMPAN KE LIST
            # Masukkan ke list dengan label platform Shopee
            hasil_scraping.append({
                "platform": "Shopee",
                "data_mentah": teks_mentah
            })
            
        # TODO 10: TUTUP BROWSER
        await browser.close()
        
    # Kembalikan hasilnya
    return hasil_scraping

# Blok Testing Lokal
if __name__ == "__main__":
    print("--- MULAI TESTING SCRAPER SHOPEE ---")
    
    # Jalankan fungsinya
    hasil = asyncio.run(scrape_shopee_skincare())
    
    # Tampilkan di terminal
    print("\nIni hasil tarikannya:")
    for item in hasil:
        print(item)
        print("-" * 30)