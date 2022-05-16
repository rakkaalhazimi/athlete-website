# Aplikasi Pencarian Atlet berbasis Web
Aplikasi yang mendukung pencarian data atlete cabang renang pada provinsi Riau dan Kep Riau.  
<br>

# Software yang diperlukan
1. MongoDB versi 5 ke atas
2. ElasticSearch versi 8 ke atas
<br>

# Instalasi
1. Download python versi 3.8 keatas
2. Jalankan perintah
    
    ```
    pip install -r requirements.txt
    ```
3. Masukkan data atlet dengan menggunakan perintah
   
    ```
    flask insert_data athlete.jsonl
    ```

4. Ubah konfigurasi MongoDB dan ElasticSearch pada file [ini](app/config.py)
5. Bangunkan server website dengan perintah
   
    ```
    flask run
    ```

    atau

    ```
    python run.py
    ```
    
<br>

# Operasi CRUD
## Memasukkan data
```
flask insert_data <jsonl_path>
```
`jsonl_path` merupakan file yang berisikan javascript object yang dipisahkan oleh `line break` atau `\n`

<br>

## Memperbaharui data
`flask update_data --query --update --how`
contoh:
```
flask update_data --query="{\"Athlete_Name\": \"ADITHYA PRAYOGA\"}" --update="{\"Athlete_Name\": \"TENYOM KUCING\"}" --how="one"
```
keterangan:
-query: kriteria data
-update: data pengganti
-how: banyaknya data yang akan diganti (one atau many)

<br>

## Menghapus data
`flask update_data --query --update --how`
contoh:
```
flask delete_data --query="{\"Athlete_Name\": \"ADITHYA PRAYOGA\"}" --how="one"
```
keterangan:
-query: kriteria data
-how: banyaknya data yang akan dihapus (one atau many)

<br>


## Menghapus koleksi
```
flask drop_collections
```