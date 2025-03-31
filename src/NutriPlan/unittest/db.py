import sqlite3

import os
# import database.dummy as data

# from classes.Bahan_Baku import Bahan_Baku
# from classes.Makanan import Makanan
# from classes.Resep import Resep
# from classes.Jadwal_Makanan import Jadwal_Makanan
# from classes.Daftar_Riwayat import Daftar_Riwayat
# from classes.Daftar_Belanja import Daftar_Belanja

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.data_initialized = False  # Flag to track data initialization

        if os.path.exists(db_name):
            #print("Database file '{}' already exists. Initialization skipped.".format(db_name))
            self.connect()
        else:
            self.create_database()


    def connect(self):
        self.conn = sqlite3.connect(self.db_name,check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_database(self):
        self.connect()  # Connect to the database
        self.create_all_table()  # Create all tables
        # self.init_all_data()  # Initialize all data        
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor.execute('INSERT INTO resep (id_resep, cara_membuat) VALUES (0, "dummy")')
        self.cursor.execute('INSERT INTO makanan (id_makanan, nama, deskripsi, cara_buat) VALUES (0, "dummy", "Tidak ada", 0)')
        self.cursor.execute('INSERT INTO jadwal_makanan (id_jadwal, makanan, kategori, tanggal) VALUES (100, 0, 0, 0)')

    def create_all_table(self):
        self.create_table_bahan_baku()
        self.create_table_resep()
        self.create_table_detail_resep()
        self.create_table_daftar_belanja()
        self.create_table_makanan()
        self.create_table_jadwal_makanan()
        self.create_table_daftar_riwayat()


    def create_table_makanan(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS makanan (
            id_makanan INTEGER PRIMARY KEY,
            nama TEXT,
            deskripsi TEXT,
            cara_buat INTEGER,
            FOREIGN KEY (cara_buat) REFERENCES resep(id_resep)
        )
        ''')
        self.conn.commit()
    
    def create_table_resep(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS resep (
            id_resep INTEGER PRIMARY KEY,
            cara_membuat TEXT
        )
        ''')
        self.conn.commit()
        
    def create_table_jadwal_makanan(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS jadwal_makanan (
            id_jadwal INTEGER PRIMARY KEY,
            makanan INTEGER,
            kategori TEXT,
            tanggal TEXT,
            FOREIGN KEY (makanan) REFERENCES makanan(id_makanan)
        )
        ''')
        self.conn.commit()
    def create_table_daftar_riwayat(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS daftar_riwayat (
            jadwal INTEGER PRIMARY KEY,
            catatan TEXT,
            FOREIGN KEY (jadwal) REFERENCES jadwal_makanan(id_jadwal)
        )
        ''')
        self.conn.commit()
        
    def create_table_detail_resep(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS detail_resep (
            id_resep INTEGER,
            id_bahan INTEGER,
            kuantitas TEXT,
            FOREIGN KEY (id_resep) REFERENCES resep(id_resep),
            FOREIGN KEY (id_bahan) REFERENCES bahan_baku(id_bahan),
            PRIMARY KEY (id_resep, id_bahan)
        )
        ''')
        self.conn.commit()
    
    def create_table_bahan_baku(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS bahan_baku (
            id_bahan INTEGER PRIMARY KEY,
            nama_bahan TEXT
        )
        ''')
        self.conn.commit()

    def create_table_daftar_belanja(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS daftar_belanja (
            barang INTEGER,
            kuantitas TEXT,
            sudah_dibeli BOOL,
            FOREIGN KEY (barang) REFERENCES bahan_baku(id_bahan)
        )
        ''')
        self.conn.commit()

    def get_all_data(self, table_name):
        query = "SELECT * FROM {}".format(table_name)
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def join_two_table(self,table1,table2,value1,value2):
        query = "SELECT * FROM {} INNER JOIN {} ON {}.{} = {}.{}".format(table1,table2,table1,value1,table2,value2)
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def update_data_shopping(self, table_name, column_name,condition, new_value):
        query = "UPDATE {} SET {} = {} WHERE barang = {}".format(table_name, column_name,new_value,condition)
        #print(query)
        self.cursor.execute(query)
        self.conn.commit()
        

    def insert_makanan(self, nama_makanan,deskripsi,cara_buat):
        try:
            self.cursor.execute("INSERT INTO makanan (nama,deskripsi,cara_buat) VALUES(?,?,?)", (nama_makanan,deskripsi,cara_buat))
            self.conn.commit()
        except sqlite3.Error as e:
            pass
            #print("Error inserting makanan:", e)

    def insert_jadwal_makanan(self,makanan,kategori,hari):
        try:
            self.cursor.execute("INSERT INTO jadwal_makanan (makanan,kategori,tanggal) VALUES(?,?,?)", (makanan,kategori,hari))
            self.conn.commit()
            # print("jadwal makanan inserted")
        except sqlite3.Error as e:
            # print("Error inserting jadwal makanan:", e)
            pass

    def insert_resep(self,cara_membuat):
        try:
            self.cursor.execute("INSERT INTO resep (cara_membuat) VALUES(?)", (cara_membuat,))
            self.conn.commit()
        except sqlite3.Error as e:
            pass
            #print("Error inserting rsep:", e)
    def insert_detail_resep(self,id_resep,id_bahan,kuantitas):
        try:
            self.cursor.execute("INSERT INTO detail_resep (id_resep,id_bahan,kuantitas) VALUES(?,?,?)", (id_resep,id_bahan,kuantitas))
            self.conn.commit()
        except sqlite3.Error as e:
            pass
            #print("Error inserting detail resep:", e)
    def insert_daftar_belanja(self,barang,kuantitas,sudah_dibeli):
        try:
            self.cursor.execute("INSERT INTO daftar_belanja (barang,kuantitas,sudah_dibeli) VALUES(?,?,?)", (barang,kuantitas,sudah_dibeli))
            self.conn.commit()
        except sqlite3.Error as e:
            pass
            #print("Error inserting daftar belanja:", e)
    def insert_bahan_baku(self,nama_bahan):
        try:
            self.cursor.execute("INSERT INTO bahan_baku (nama_bahan) VALUES(?)", (nama_bahan,))
            self.conn.commit()
        except sqlite3.Error as e:
            pass
            #print("Error inserting bahan baku:", e)

    def insert_daftar_riwayat(self,jadwal,catatan):
        try:
            self.cursor.execute("INSERT INTO daftar_riwayat (jadwal,catatan) VALUES(?,?)", (jadwal,catatan))
            self.conn.commit()
        except sqlite3.Error as e:
            pass
            #print("Error inserting daftar riwayat:", e)

    def  insert_daftar_belanja_by_id_makanan(self, id_makanan):
        try:
            query = f"""
            SELECT id_bahan,kuantitas 
            FROM Makanan INNER JOIN detail_resep ON Makanan.cara_buat = detail_resep.id_resep
            WHERE Makanan.id_makanan = {id_makanan}
            """
            self.cursor.execute(query)
            self.conn.commit()
            result = self.cursor.fetchall()
            if result:
                for result_entry in result:
                    id_bahan = result_entry[0]  # Get bahan baku ID
                    kuantitas = result_entry[1]
                    self.insert_daftar_belanja(id_bahan, kuantitas, 0)
                print("Inserted daftar belanja for makanan ID:", id_makanan)
            else:
                print("No data found for makanan ID:", id_makanan)
        except sqlite3.Error as e:
            print("Error inserting daftar belanja:", e)


    def fetch_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()


    def init_all_data(self):
        print("Initializing all data...")
        self.init_bahan_baku(data.bahan_baku)
        self.init_resep(data.resep)
        self.init_detail_resep(data.detail_resep)
        self.init_daftar_belanja(data.daftar_belanja)
        self.init_makanan(data.makanan)
        self.init_jadwal_makanan(data.jadwal_makanan)
        self.init_daftar_riwayat(data.daftar_riwayat)
        self.data_initialized = True  # Set flag to True after initialization

    def init_makanan(self,list):
        for x in list:
            self.insert_makanan(x[0],x[1],x[2])

    def init_detail_resep(self,list):
        for x in list:
            self.insert_detail_resep(x[0],x[1],x[2])

    def init_jadwal_makanan(self,list):
        self.conn.commit()
        for x in list:
            self.insert_jadwal_makanan(x[0],x[1],x[2])
    def init_daftar_belanja(self,list):
        for x in list:
            self.insert_daftar_belanja(x[0],x[1],x[2])
    def init_daftar_riwayat(self,list):
        for x in list:
            self.insert_daftar_riwayat(x[0],x[1])

    def init_resep(self,list):
        for x in list:
            self.insert_resep(x[0])

    def init_bahan_baku(self,list):
        for x in list:
            self.insert_bahan_baku(x[0])
    
    
    def update_daftar_riwayat(self, table_name, column_name,condition, new_value):
        # query = "UPDATE {} SET {} = '{}' WHERE jadwal = {}".format(table_name, column_name,new_value,condition)
        # #print(query)
        # self.cursor.execute(query)
        # self.conn.commit()
        query = f"UPDATE {table_name} SET {column_name} = '{new_value}' WHERE jadwal = {condition}"
        self.cursor.execute(query)
        self.conn.commit()




    #KUMPULAN FUNGSIONALITAS====================


    def join_tables(self, table1, table2, join_condition,attribute):
        query = f"""
            SELECT {attribute}
            FROM {table1} 
            INNER JOIN {table2} ON {join_condition}
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def hitung_elemen_tabel(self, table_name, condition=None):
   
        query = f"""
            SELECT COUNT(*) FROM {table_name}
        """
        if condition:
            query += f" WHERE {condition}"

        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def get_id_from_bahan(self, nama_bahan):
        query = f"SELECT id_bahan FROM bahan_baku WHERE nama_bahan = ?"
        self.cursor.execute(query, (nama_bahan,))
        result = self.cursor.fetchone()
        return result[0] if result else None



    def insert_if_not_exists(self, table_name, column_name, value):

        query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = ?"
        self.cursor.execute(query, (value,))
        count = self.cursor.fetchone()[0]

        if count > 0:
            #print(f"'{value}' already exists in table '{table_name}'. Not inserted.")
            return True
        else:
            try:
                insert_query = f"INSERT INTO {table_name} ({column_name}) VALUES (?)"
                self.cursor.execute(insert_query, (value,))
                self.conn.commit()
                #print(f"'{value}' inserted into table '{table_name}'.")
                return True
            except sqlite3.Error as e:
                #print(f"Error inserting '{value}' into table '{table_name}': {e}")
                return False
            
    def update_table_by_id(self, table_name, id_column_name, id_value, update_column_name, new_value):
        """
        Update a specific column value in a table for a given ID.

        :param table_name: Name of the table to update.
        :param id_column_name: Name of the ID column to use as the reference.
        :param id_value: Value of the ID to identify the row to update.
        :param update_column_name: Name of the column to update.
        :param new_value: New value to set in the update column.
        :return: None
        """
        try:
            query = f"""
                UPDATE {table_name}
                SET {update_column_name} = ?
                WHERE {id_column_name} = ?
            """
            self.cursor.execute(query, (new_value, id_value))
            self.conn.commit()
            #print(f"Updated {update_column_name} in table '{table_name}' where {id_column_name} = {id_value}")
        except sqlite3.Error as e:
            pass
            #print(f"Error updating {update_column_name} in table '{table_name}': {e}")


    def delete_element_by_id(self, table_name, id_column_name, id_value):
        """
        Delete an element from a table based on the given ID.

        :param table_name: Name of the table to delete from.
        :param id_column_name: Name of the ID column to use as the reference.
        :param id_value: Value of the ID to identify the row to delete.
        :return: None
        """
        try:
            query = f"DELETE FROM {table_name} WHERE {id_column_name} = ?"
            self.cursor.execute(query, (id_value,))
            self.conn.commit()
            print(f"Deleted from table '{table_name}' where {id_column_name} = {id_value}")
        except sqlite3.Error as e:
            print(f"Error deleting from table '{table_name}': {e}")
            pass

    def get_max_makanan_id(self):
        try:
            query = "SELECT MAX(id_makanan) FROM makanan"
            self.cursor.execute(query)
            result = self.cursor.fetchone()[0]
            return result if result is not None else 0
        except sqlite3.Error as e:
            #print("Error retrieving max makanan id:", e)
            return None

    def delete_detail_resep(self, id_resep, id_bahan):
        try:
            query = "DELETE FROM detail_resep WHERE id_resep = ? AND id_bahan = ?"
            self.cursor.execute(query, (id_resep, id_bahan))
            self.conn.commit()
            print(f"Deleted from detail resep where id_resep = {id_resep} and id_bahan = {id_bahan}")
        except sqlite3.Error as e:
            print(f"Error deleting from detail resep: {e}")
            pass
    
    #Page Jadwal Related ============================
    
    def get_jadwal_bulan(self, month):
        query = """
        SELECT * FROM jadwal_makanan
        WHERE SUBSTR(tanggal, 4, 2) = ?
        """
        self.cursor.execute(query, (month,))
        jadwal_tuples = self.cursor.fetchall()  
        
        jadwal_list = []
        for jadwal in jadwal_tuples:
            makanan = self.get_makanan_by_id(jadwal[1])
            jadwal_list.append(Jadwal_Makanan(jadwal[0], makanan, jadwal[2], jadwal[3]))
        return jadwal_list

    def get_all_makanan(self):
        makanan_tuples = self.get_all_data("Makanan")
        makanan_list = []
        # print(makanan_tuples)
        
        for makanan in makanan_tuples:
            makanan_list.append(Makanan(makanan[0], makanan[1], makanan[2], makanan[3]))
        return makanan_list
    
    def get_makanan_by_id(self, id_makanan):
        query = "SELECT * FROM makanan WHERE id_makanan = ?"
        self.cursor.execute(query, (id_makanan,))
        result = self.cursor.fetchone()
        return Makanan(result[0], result[1], result[2], result[3]) if result else None
    
    def get_makanan_by_id_jadwal(self, id_jadwal):
        query = "SELECT makanan FROM jadwal_makanan WHERE id_jadwal = ?"
        self.cursor.execute(query, (id_jadwal,))
        id_makanan = self.cursor.fetchone()[0]
        return self.get_makanan_by_id(id_makanan)
    
    def get_all_jadwal_makanan(self):
        jadwal_tuples = self.get_all_data("Jadwal_Makanan")
        jadwal_list = []
        
        for jadwal in jadwal_tuples:
            makanan = self.get_makanan_by_id(jadwal[1])
            jadwal_list.append(Jadwal_Makanan(jadwal[0], makanan, jadwal[2], jadwal[3]))
        return jadwal_list
    
    def jadwal_already_exists(self,  kategori, tanggal):
        query = "SELECT * FROM jadwal_makanan WHERE kategori = ? AND tanggal = ?"
        self.cursor.execute(query, (kategori, tanggal))
        return self.cursor.fetchone() is not None
    
    def get_last_id_jadwal(self):
        query = "SELECT MAX(id_jadwal) FROM jadwal_makanan"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]+1
    
    def delete_jadwal(self, id_jadwal):
        self.delete_element_by_id("jadwal_makanan", "id_jadwal", id_jadwal)
        print("Menghapus jadwal")
        
    def get_jadwal_by_id(self, id_jadwal):
        query = "SELECT * FROM jadwal_makanan WHERE id_jadwal = ?"
        self.cursor.execute(query, (id_jadwal,))
        jadwal = self.cursor.fetchone()
        jadwal_obj = Jadwal_Makanan(jadwal[0], self.get_makanan_by_id(jadwal[1]), jadwal[2], jadwal[3])
        return jadwal_obj