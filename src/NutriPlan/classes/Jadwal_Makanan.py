from classes.Makanan import Makanan

class Jadwal_Makanan:
    def __init__(self, id_jadwal: int, makanan: Makanan, kategori: str, hari: str):
        self.id_jadwal = id_jadwal
        self.makanan = makanan
        self.kategori = kategori
        self.hari = hari
        
    def __str__(self):
        return f"({self.id_jadwal} - {self.makanan} - {self.kategori} - {self.hari})"
    
    def __repr__(self):
        return self.__str__()
    
    def getHari(self):
        return int(self.hari[0:2])
    
    def getKategori(self):
        if self.kategori == "Sarapan":
            return 1
        elif self.kategori == "Makan Siang":
            return 2
        elif self.kategori == "Makan Malam":
            return 3
        else:
            return -1
