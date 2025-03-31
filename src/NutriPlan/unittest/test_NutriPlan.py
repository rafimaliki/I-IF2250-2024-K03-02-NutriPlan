from datetime import datetime
from db import DatabaseManager
import dummy_data

# pytest src/NutriPlan/unittest/test_NutriPlan.py

currDT = datetime.now()
currdate = currDT.strftime("%Y-%m-%d %H-%M-%S")
testDB = DatabaseManager('src/NutriPlan/unittest/testDB' + currdate + '.db')

# test initialization, berhasil
def test_read_all_data():
    bahan_baku = testDB.get_all_data("bahan_baku")
    resep = testDB.get_all_data("resep")
    detail_resep = testDB.get_all_data("detail_resep")
    makanan = testDB.get_all_data("makanan")
    jadwal_makanan = testDB.get_all_data("jadwal_makanan")
    daftar_belanja = testDB.get_all_data("daftar_belanja")
    daftar_riwayat = testDB.get_all_data("daftar_riwayat")

    assert (bahan_baku == [] and resep == [(0, "dummy")] and detail_resep == [] and makanan == [(0, "dummy", "Tidak ada", 0)] and jadwal_makanan == [(100, 0, '0', '0')] and daftar_belanja == [] and daftar_riwayat == [])

# test insert bahan baku berhasil
def test_insert_bahan_baku():
    for bahan_baku_entry in dummy_data.bahan_baku:
        testDB.insert_bahan_baku(bahan_baku_entry[0])
    assert testDB.get_all_data("bahan_baku") == [
        (1, "bawang_merah"),
        (2, "bawang_putih"),
        (3, "garam"),
        (4, "gula"),
        (5, "telur"),
        (6, "minyak")
    ]

# test insert resep berhasil
def test_insert_resep():
    print("lewat sekali saja")
    for resep_entry in dummy_data.resep:
        testDB.insert_resep(resep_entry[0])
    assert testDB.get_all_data("resep") == [
        (0, "dummy"),
        (1, "1. Tuang minyak ke wajan lalu nyalakan kompor\n2. Selama menunggu minyak panas, kocok telur dan garam\n3. Jika minyak sudah panas, tuangkan telur ke wajan\n4. Tunggu hingga telur matang, lalu angkat")
    ]

# test insert detail resep berhasil
def test_insert_detail_resep():
    print("lewat sekali saja")
    for detail_resep_entry in dummy_data.detail_resep:
        testDB.insert_detail_resep(detail_resep_entry[0], detail_resep_entry[1], detail_resep_entry[2])
    assert testDB.get_all_data("detail_resep") == [
        (1, 3, "1/4 sendok teh"),
        (1, 5, "1 butir"),
        (1, 6, "secukupnya")
    ]

# test insert makanan berhasil
def test_insert_makanan():
    print("lewat sekali saja")
    for makanan_entry in dummy_data.makanan:
        testDB.insert_makanan(makanan_entry[0], makanan_entry[1], makanan_entry[2])
    assert testDB.get_all_data("makanan") == [
        (0, "dummy", "Tidak ada", 0),
        (1, "Telur Dadar", "Makanan yang selalu hadir di kala miskin", 1)
    ]

# test insert jadwal makanan berhasil
def test_insert_jadwal_makanan():
    print("lewat sekali saja")
    for jadwal_makanan_entry in dummy_data.jadwal_makanan:
        testDB.insert_jadwal_makanan(jadwal_makanan_entry[0], jadwal_makanan_entry[1], jadwal_makanan_entry[2])
    assert testDB.get_all_data("jadwal_makanan") == [
        (100, 0, '0', '0'),
        (101, 1, "Sarapan", "Senin, 12 Mei 2024")
    ]

# test insert daftar belanja berhasil
def test_insert_daftar_belanja():
    print("lewat sekali saja")
    for daftar_belanja_entry in dummy_data.daftar_belanja:
        testDB.insert_daftar_belanja(daftar_belanja_entry[0], daftar_belanja_entry[1], daftar_belanja_entry[2])
    assert testDB.get_all_data("daftar_belanja") == [
        (3, "1/4 sendok teh", 0),
        (5, "1 butir", 0),
        (6, "secukupnya", 0)
    ]

# test insert daftar riwayat berhasil
def test_insert_daftar_riwayat():
    print("lewat sekali saja")
    for daftar_riwayat_entry in dummy_data.daftar_riwayat:
        testDB.insert_daftar_riwayat(daftar_riwayat_entry[0], daftar_riwayat_entry[1])
    assert testDB.get_all_data("daftar_riwayat") == [
        (101, "Sarapan pagi ini sangat enak, telur dadar yang dimasak dengan minyak goreng sangat nikmat")
    ]

# test delete bahan baku berhasil
def test_delete_bahan_baku_1():
    testDB.delete_element_by_id("bahan_baku", "id_bahan", 1)
    assert testDB.get_all_data("bahan_baku") == [
        (2, "bawang_putih"),
        (3, "garam"),
        (4, "gula"),
        (5, "telur"),
        (6, "minyak")
    ]

# test delete bahan baku gagal karena ditunjuk detail resep
def test_delete_bahan_baku_2():
    testDB.delete_element_by_id("bahan_baku", "id_bahan", 6)
    assert testDB.get_all_data("bahan_baku") == [
        (2, "bawang_putih"),
        (3, "garam"),
        (4, "gula"),
        (5, "telur"),
        (6, "minyak")
    ]

# test delete daftar belanja berhasil
def test_delete_daftar_belanja_1():
    testDB.delete_element_by_id("daftar_belanja", "barang", 3)
    assert testDB.get_all_data("daftar_belanja") == [
        (5, "1 butir", 0),
        (6, "secukupnya", 0)
    ]

# test delete daftar belanja berhasil
def test_delete_daftar_belanja_2():
    testDB.delete_element_by_id("daftar_belanja", "barang", 6)
    assert testDB.get_all_data("daftar_belanja") == [
        (5, "1 butir", 0)
    ]

# test delete jadwal makanan gagal karena ditunjuk daftar riwayat
def test_delete_jadwal_makanan():
    testDB.delete_element_by_id("jadwal_makanan", "id_jadwal", 101)
    assert testDB.get_all_data("jadwal_makanan") == [
        (100, 0, '0', '0'),
        (101, 1, "Sarapan", "Senin, 12 Mei 2024")
    ]

# test delete daftar riwayat berhasil
def test_delete_daftar_riwayat_1():
    testDB.delete_element_by_id("daftar_riwayat", "jadwal", 101)
    assert testDB.get_all_data("daftar_riwayat") == []

# test delete jadwal makanan berhasil
def test_delete_jadwal_makanan_2():
    testDB.delete_element_by_id("jadwal_makanan", "id_jadwal", 101)
    assert testDB.get_all_data("jadwal_makanan") == [
        (100, 0, '0', '0')
    ]

# test delete makanan berhasil
def test_delete_makanan():
    testDB.delete_element_by_id("makanan", "id_makanan", 1)
    assert testDB.get_all_data("makanan") == [
        (0, "dummy", "Tidak ada", 0)
    ]

# test delete resep gagal karena ditunjuk detail resep
def test_delete_resep():
    testDB.delete_element_by_id("resep", "id_resep", 1)
    assert testDB.get_all_data("resep") == [
        (0, "dummy"),
        (1, "1. Tuang minyak ke wajan lalu nyalakan kompor\n2. Selama menunggu minyak panas, kocok telur dan garam\n3. Jika minyak sudah panas, tuangkan telur ke wajan\n4. Tunggu hingga telur matang, lalu angkat")
    ]

# test delete detail resep berhasil
def test_delete_detail_resep_1():
    testDB.delete_detail_resep(1, 3)
    assert testDB.get_all_data("detail_resep") == [
        (1, 5, "1 butir"),
        (1, 6, "secukupnya")
    ]

# test delete detail resep berhasil
def test_delete_detail_resep_2():
    testDB.delete_detail_resep(1, 5)
    assert testDB.get_all_data("detail_resep") == [
        (1, 6, "secukupnya")
    ]

# test delete detail resep berhasil
def test_delete_detail_resep_3():
    testDB.delete_detail_resep(1, 6)
    assert testDB.get_all_data("detail_resep") == []

# test delete resep berhasil
def test_delete_resep_2():
    testDB.delete_element_by_id("resep", "id_resep", 1)
    assert testDB.get_all_data("resep") == [
        (0, "dummy")
    ]

# test delete bahan baku berhasil
def test_delete_bahan_baku_3():
    testDB.delete_element_by_id("bahan_baku", "id_bahan", 6)
    assert testDB.get_all_data("bahan_baku") == [
        (2, "bawang_putih"),
        (3, "garam"),
        (4, "gula"),
        (5, "telur")
    ]

# test update bahan baku berhasil
def test_update_bahan_baku():
    testDB.update_table_by_id("bahan_baku", "nama_bahan", "bawang_putih", "nama_bahan", "bawang_merah")
    assert testDB.get_all_data("bahan_baku") == [
        (2, "bawang_merah"),
        (3, "garam"),
        (4, "gula"),
        (5, "telur")
    ]