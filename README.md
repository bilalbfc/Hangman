# Hesaplama-temelli-adamAsmaca-Oyunu
Hesaplamanın entegre edildiği python tarafında geliştirilen adam asmaca oyunu
# 🧠 Calc & Hang: Hesaplama Temelli Adam Asmaca

## 🎯 Proje Açıklaması

**Calc & Hang**, klasik Adam Asmaca oyununu hesaplama ve karar verme mekanikleriyle birleştiren bir Python konsol oyunudur. Oyunun temel amacı, sadece kelime tahmini yapmak değil, aynı zamanda matematiksel işlemlerle ** (Bonus) kullanarak** oynanışı stratejik hale getirmektir.

## ✨ Temel Özellikler

Bu projeyi diğer Adam Asmaca oyunlarından ayıran ana özellikler şunlardır:

### 1. Hesap Makinesi 
Oyuncular, ana menüden erişilebilen bir matematik işlem (toplama, çıkarma, çarpma, bölme) çözme seçeneğine sahiptir.
* **Doğru Cevap:** Oyuncuya **Bonus puanı** kazandırır ve kelimedeki bilinmeyen **rastgele bir harfi açar** (ipucu).
* **Yanlış Cevap:** Oyuncunun skorundan puan düşülür ve **bir hata hakkı** kaybedilir.
Bu mekanizma, "Hesaplama Temelli" konseptini uygulamaktadır.

### 2. Kapsamlı Oyun Yönetimi
* **Kategoriler:** Hayvanlar, Meyveler ve Teknolojiler kategorilerinden rastgele kelime seçimi.
* **Sınıf Yapısı:** Oyun mantığı, `Hangman` sınıfı içinde OOP (Nesne Yönelimli Programlama) prensipleriyle düzenlenmiştir.
* **Skor Takibi:** Oyuncu skorları `scores.json` dosyasına kaydedilir ve en yüksek 5 skor listelenir.

### 3. Kullanıcı Deneyimi (UX)
* **Hata Kontrolü:** Tahminlerde veya isim girişinde geçersiz değerler (uzunluk/tip) için özel `CountError` ve `ValueError` istisnaları kullanılır.
* **Görsel:** `colorama` kütüphanesi ile renkli çıktı (Yeşil Başarı, Kırmızı Hata vb.) ve ASCII sanatıyla Adam Asmaca figürünün güncel durumu gösterilir.

## ⚙️ Kurulum ve Çalıştırma

### Gereksinimler

Bu projeyi çalıştırmak için Python 3.x ve aşağıdaki kütüphane gereklidir:
'pip install colorama'

##Projeyi Klonlama
git clone [https://github.com/bilalbfc/Hangman.git](https://github.com/bilalbfc/Hangman.git)
cd Hesaplama-Temelli-Adam-Asmaca

##Oyunu Başlatma
python adamAsmaca.py

##Projedeki Bazı Fonksiyon ve Metotlar
*selectedRandomWord->"Yeni bir tur başlatır, rastgele kelime ve kategori seçer."
*letterGuessing->"Harf tahminini kontrol eder, skor ve hata sayısını günceller."
*calculator->Matematik problemi sunar ve doğru cevapta bonus/ipucu verir.
*openRandomLetter->Kelimede rastgele bir bilinmeyen harfi açar (Hesap makinesi bonusu).
*writeToFile/writeScores->Skorları scores.json dosyasına okur/yazar.
