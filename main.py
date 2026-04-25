from etl.extract.coingecko import fetch_markets
from etl.load.upload_minio import upload_raw

def main():
    print("🚀 Memulai Uji Coba Jalur Extract -> Data Lake (MinIO)...")
    
    try:
        # 1. Tarik data dari CoinGecko
        print("Sedang menarik 250 koin teratas...")
        data_markets = fetch_markets()
        
        # 2. Upload ke MinIO
        print("Mengirim data mentah ke MinIO...")
        file_path = upload_raw(data_markets, "test_coingecko")
        
        print(f"\n✅ SUKSES BESAR! File berhasil disimpan di Data Lake pada path:")
        print(f"👉 {file_path}")
        
    except Exception as e:
        print(f"\n❌ Yaaah, ada yang nyangkut: {e}")

if __name__ == "__main__":
    main()