from classes.Bahan_Baku import Bahan_Baku

class Daftar_Belanja:
    # static list of Daftar_Belanja
    daftar_belanja = []

    def __init__(self, barang: Bahan_Baku, kuantitas: int, sudah_dibeli: bool):
        self.barang = barang
        self.kuantitas = kuantitas
        self.sudah_dibeli = sudah_dibeli
    