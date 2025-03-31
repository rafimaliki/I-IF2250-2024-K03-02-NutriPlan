from classes.Bahan_Baku import Bahan_Baku

class Resep:
    def __init__(self, id_resep: int, bahan: Bahan_Baku, kuantitas: int, cara_membuat: str):
        self.id_resep = id_resep
        self.bahan = bahan
        self.kuantitas = kuantitas
        self.cara_membuat = cara_membuat