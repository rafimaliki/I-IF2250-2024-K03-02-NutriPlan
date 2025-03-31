from classes.Resep import Resep

class Makanan:
    def __init__(self, id_makanan: int = None, nama: str = None, deskripsi: str = None, cara_buat: Resep = None):
        self.id_makanan = id_makanan
        self.nama = nama
        self.deskripsi = deskripsi
        self.cara_buat = cara_buat
    
    def __str__(self):
        return f"({self.id_makanan} - {self.nama} - {self.deskripsi})"
    
    def __repr__(self):
        return self.__str__()
