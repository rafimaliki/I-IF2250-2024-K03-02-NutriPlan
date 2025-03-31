from classes.Jadwal_Makanan import Jadwal_Makanan

class Daftar_Riwayat:
    def __init__(self, jadwal: Jadwal_Makanan, catatan: str):
        self.jadwal = jadwal
        self.catatan = catatan