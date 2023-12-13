import csv


# csv dosyalarını okumak için csv kütüphanesini ekledik
# TIR'ların özelliklerini tanımladık
class TIR:
    def __init__(self, plaka, ulke, tonaj_20, tonaj_30, yuk_miktari, yuk_maliyeti):
        self.plaka = plaka
        self.ulke = ulke
        self.tonaj_20 = tonaj_20
        self.tonaj_30 = tonaj_30
        self.yuk_miktari = yuk_miktari
        self.yuk_maliyeti = yuk_maliyeti

    # TIRların plakalarına göre sıralanması için kullandık
    def __lt__(self, other):
        return self.plaka < other.plaka


# Gemilerin özelliklerini tanımladık
class Gemi:
    def __init__(self, numara, kapasite, hedef_ulke):
        self.numara = numara
        self.kapasite = kapasite
        self.hedef_ulke = hedef_ulke
        self.yuk = 0
        self.yukleme = False

    # gemilerin numaralarına göre sıralanması için vkullanılır
    def __lt__(self, other):
        return self.numara < other.numara


# limanın özellikleri tanımlanır
class Liman:
    def __init__(self):
        self.tir_kuyrugu = []
        self.gemi_kuyrugu = []
        self.istif_alani_1 = []
        self.istif_alani_2 = []
        self.istif_alani_1_kapasite = 750
        self.istif_alani_2_kapasite = 750
        self.istif_alani_1_yuk = 0
        self.istif_alani_2_yuk = 0
        self.vinc = 0
        self.vinc_limit = 20
        self.t = 0

    # tırların bilgilerinin olduğu dosyadan bilgiler çekilip sıraya eklenir
    def tir_bilgisi_okuma(self):
        with open("olaylar.csv") as f:
            for tir in csv.DictReader(f):
                plaka, ulke, yirmi_ton, otuz_ton, maliyet = tir.values()
                self.tir_kuyrugu.append(tir(plaka, ulke, yirmi_ton, otuz_ton, maliyet))

    # gemilerin bilgilerinin olduğu dosyadan bilgiler çekilip sıraya eklenir
    def gemi_bilgisi_okuma(self):
        with open("gemiler.csv", "r") as f:
            for gemi in f.read().splitlines():
                numara, kapasite, hedef_ulke = gemi.split(",")
                self.gemi_kuyrugu.append(Gemi(numara, kapasite, hedef_ulke))

    # sıraya eklenmiş olan tırları sırasıyla istif alanında yük indirmeye gönderilir.
    def tir_yuk_indirme(self):
        for tir in self.tir_kuyrugu:
            print(f"{self.t}. dakikada {tir.plaka} plakalı TIR yükünü indirdi.")
            self.istif_alani_1.append(tir)
            self.istif_alani_1_yuk += tir.yuk
            if self.istif_alani_1_yuk >= self.istif_alani_1_kapasite:
                print(f"1 numaralı istif alanı dolu. ({self.istif_alani_1_yuk} ton)")
            self.t += 1

    # sıraya eklenmiş olan gemilere yükleri yükledik, yükleme sınırlarını vb. tanımladık
    def gemi_yuk_yukleme(self):
        for gemi in self.gemi_kuyrugu:
            print(f"{self.t}. dakikada {gemi.numara} numaralı gemi yükleme için hazır.")

            while gemi.yuk < gemi.kapasite * 0.95:
                # 1 numaralı istif alanından TIR çıkar
                if self.istif_alani_1:
                    tir = self.istif_alani_1.pop()
                    if tir.ulke == gemi.hedef_ulke:
                        gemi.yuk += tir.yuk
                        gemi.yukleme = True
                        print(
                            f"{self.t}. dakikada {gemi.numara} numaralı gemiye {tir.plaka} plakalı TIRın yükü yüklendi. ({tir.ulke}) ({tir.maliyet}₺)")
                    else:
                        self.istif_alani_2.append(tir)

                # 2. istiftem tırlar çıkarılır
                else:
                    tir = self.istif_alani_2.pop()
                    if tir.ulke == gemi.hedef_ulke:
                        gemi.yuk += tir.yuk
                        gemi.yukleme = True
                        print(
                            f"{self.t}. dakikada {gemi.numara} numaralı gemiye {tir.plaka} plakalı TIRın yükü yüklendi. ({tir.ulke}) ({tir.maliyet}₺)")
                    else:
                        self.istif_alani_1.append(tir)

            if not gemi.yukleme:
                print(f"{self.t}. dakikada {gemi.numara} numaralı gemi limanı terk etti. ({gemi.yuk} ton)")

            # vinç durumu güncellenir
            self.vinc += 1
            if self.vinc == self.vinc_limit:
                break


def main():
    liman = Liman()
    liman.tir_bilgisi_okuma()
    liman.gemi_bilgisi_okuma()
    liman.tir_yuk_indirme()
    liman.gemi_yuk_yukleme()


if __name__ == "__main__":
    main()