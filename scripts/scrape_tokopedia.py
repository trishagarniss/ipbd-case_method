"""
File: scrape_tokopedia.py
Tujuan: Menarik data produk skincare dari Tokopedia.
Status: Tahap Kerangka Dasar (Skeleton).
"""

# TODO 1: IMPORT LIBRARY YANG DIBUTUHKAN
# Kita butuh 'asyncio' untuk menjalankan fungsi asynchronous.
# Kita butuh 'async_playwright' dari library playwright untuk mengendalikan browser.
import asyncio
from playwright.async_api import async_playwright

# TODO 2: BIKIN FUNGSI UTAMA
# Nama fungsinya harus jelas, misal 'scrape_tokopedia_skincare'.
# Wajib pakai 'async def' karena Playwright butuh waktu untuk nunggu loading web.
async def scrape_tokopedia_skincare():
    
    # Menyiapkan list kosong untuk menampung data yang nanti berhasil ditarik
    hasil_scraping = []
    
    # Membuka sesi Playwright
    async with async_playwright() as p:
        
        # TODO 3: BUKA BROWSER
        # Gunakan p.chromium.launch(). 
        # Saat tahap pembuatan dan testing, set 'headless=False' biar kamu bisa lihat browsernya jalan sendiri.
        # Nanti kalau script-nya sudah sempurna dan siap masuk VPS, baru ganti jadi 'headless=True'.
        browser = await p.chromium.launch(headless=False) 
        
        # Buka tab baru di browser tersebut
        page = await browser.new_page()
        
        # TODO 4: MASUK KE URL TARGET
        # Tentukan URL pencarian Tokopedia. 
        # Misal: url = "https://www.tokopedia.com/search?q=moisturizer"
        url = "https://www.tokopedia.com/search?q=moisturizer"
        print(f"Lagi buka Tokopedia nih: {url}")
        
        # Suruh page pergi ke URL tersebut pakai 'await page.goto(url)'
        await page.goto(url)
        
        # TODO 5: KASIH JEDA WAKTU (LOADING)
        # Website gede kaya Tokopedia butuh waktu buat nampilin gambar dan harga.
        # Gunakan 'await page.wait_for_timeout(angka_dalam_milidetik)'.
        # Kasih misal 5000 (5 detik) atau 7000 (7 detik).
        print("Nunggu webnya loading bentar...")
        await page.wait_for_timeout(7000)
        
        # TODO 6: CARI PEMBUNGKUS KOTAK PRODUK (INSPECT ELEMENT)
        # Ini bagian paling menantang!
        # Kamu harus buka Tokopedia di browser biasa -> klik kanan di salah satu produk -> Inspect.
        # Cari 'class' atau 'data-testid' yang membungkus SATU KOTAK produk secara utuh.
        # Kalau sudah ketemu, masukkan ke query_selector_all.
        # Contoh: products = await page.query_selector_all("[data-testid='divProductWrapper']")
        
        print("Mencoba mencari kotak produk...")
        products = await page.query_selector_all("[data-testid='divProductWrapper']") # <- Ini masih tebakan awal, bisa jadi harus diganti!
        
        print(f"Ketemu {len(products)} kotak produk di halaman ini.")
        
        # TODO 7: AMBIL TEKS DARI TIAP KOTAK
        # Lakukan perulangan (for loop) untuk setiap 'product' yang ditemukan.
        # Biar gak berat pas ngetes, batasi dulu ambil 5 atau 10 produk pertama.
        for product in products[:5]: 
            # Gunakan 'await product.inner_text()' untuk narik semua teks mentah di dalam kotak itu
            teks_mentah = await product.inner_text()
            
            # TODO 8: SIMPAN KE LIST
            # Masukkan teks_mentah tadi ke dalam list 'hasil_scraping' yang kita buat di atas.
            # Formatnya dibikin dictionary biar rapi.
            hasil_scraping.append({
                "platform": "Tokopedia",
                "data_mentah": teks_mentah
            })
            
        # TODO 9: TUTUP BROWSER
        # Penting! Jangan lupa tutup browser biar RAM laptopmu nggak bocor.
        await browser.close()
        
    # Mengembalikan hasil tarikan biar nanti bisa dipakai oleh file main_etl.py
    return hasil_scraping

# TODO 10: BLOK TESTING
# Bagian ini cuma dieksekusi kalau kamu me-run file ini langsung di terminal.
# Gunanya buat ngetes script kamu sendiri sebelum disambung ke file lain.
if __name__ == "__main__":
    print("--- MULAI TESTING SCRAPER TOKOPEDIA ---")
    
    # Jalankan fungsi async menggunakan asyncio.run()
    hasil = asyncio.run(scrape_tokopedia_skincare())
    
    # Tampilkan hasilnya di terminal
    print("\nIni hasil tarikannya:")
    for item in hasil:
        print(item)
        print("-" * 30)