# PENTING:
# Baca Model Relational Database di draw.io dulu!!!!!!!!!!!!

# Katanya auto increment jadi id-nya ga ada
bahan_baku = [
["bawang_merah"],
["bawang_putih"],
["garam"],
["gula"],
["telur"],
["minyak"]
]

# Katanya auto increment jadi id-nya ga ada
resep = [
["1. Tuang minyak ke wajan lalu nyalakan kompor\n2. Selama menunggu minyak panas, kocok telur dan garam\n3. Jika minyak sudah panas, tuangkan telur ke wajan\n4. Tunggu hingga telur matang, lalu angkat"] 
]

# Ini ngikut auto increment-nya resep dan bahan_baku
detail_resep = [
    [1, 3, "1/4 sendok teh"],
    [1, 5, "1 butir"],
    [1, 6, "secukupnya"]
]

# Katanya auto increment jadi id-nya ga ada
makanan = [
    ["Telur Dadar", "Makanan yang selalu hadir di kala miskin", 1]
]

# Katanya auto increment jadi id-nya ga ada (yang 1 itu id_makanan, ngikut auto increment-nya makanan)
jadwal_makanan = [
    [1, "Sarapan", "12-05-2024"]
]

# Ini ngikut auto increment-nya bahan_baku
daftar_belanja = [
    [3, "1/4 sendok teh", False],
    [5, "1 butir", False],
    [6, "secukupnya", False]
]

# Ini ngikut auto increment-nya jadwal_makanan
daftar_riwayat = [
    [ 101,"Sarapan pagi ini sangat enak, telur dadar yang dimasak dengan minyak goreng sangat nikmat"]
]