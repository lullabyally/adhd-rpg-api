# ADHD RPG - Backend REST API

**Nama:** Lubna Hanna Kamalia  
**NIM:** 21114012610074  
**Learning Labs:** Backend Development  
**Teknologi:** Python (Flask), SQLAlchemy ORM, Supabase (PostgreSQL), Vercel Serverless  

---

## 📌 Deskripsi Proyek
**ADHD RPG** adalah REST API untuk aplikasi gamifikasi produktivitas yang dirancang membantu pengguna mengelola tugas sehari-hari layaknya bermain game RPG.

Fitur utama backend ini meliputi:
1. **Brain Dump / Thoughts:** Mencatat berbagai ide, distraksi, atau tugas yang sedang dipikirkan pengguna.
2. **Quest Conversion:** Mengonversi catatan thought menjadi misi (*quest*) dengan tingkat kesulitan tertentu (*Easy, Medium, Hard*).
3. **Reward & Leveling System:** Menghitung perolehan XP secara otomatis berdasarkan tingkat kesulitan misi dan menaikkan level karakter pemain setelah misi diselesaikan.
4. **User Profile & Badges:** Menyimpan progres petualangan pengguna serta pencapaian yang diperoleh.

---

## 🌐 Tautan Proyek (Deployment & Repository)
* **URL Deployment API (Vercel):** [suspicious link removed]
* **URL Repository GitHub:** [suspicious link removed]

---

## 🗄️ Skema Database (5 Tabel Berelasi)
Database dibangun di atas cloud PostgreSQL (Supabase) dengan 5 tabel yang saling terhubung menggunakan *Foreign Key*:

1. **`users`**: Menyimpan akun pengguna, total XP, dan level karakter.
2. **`profiles`**: Menyimpan detail profil tambahan, gelar petualang, dan streak harian (Relasi *One-to-One* dengan `users`).
3. **`thoughts`**: Menyimpan catatan tugas/ide awal pengguna (Relasi *One-to-Many* dengan `users`).
4. **`quests`**: Menyimpan misi aktif, tingkat kesulitan, reward XP, dan status penyelesaian (Relasi *One-to-Many* dengan `users` dan relasi opsional dengan `thoughts`).
5. **`badges`**: Menyimpan lencana penghargaan yang berhasil diraih pengguna (Relasi *One-to-Many* dengan `users`).

### Diagram ERD (Entity Relationship Diagram)

         profiles  (1:1)  ──────  users
                                    │ (1:N)
                     ┌──────────────┼──────────────┐
                     ▼              ▼              ▼
                 thoughts         quests         badges
                     │              ▲
                     └─ (0..1 : N) ─┘

---

## 🚀 Dokumentasi Pemanggilan Endpoint API

### 1. Health Check
* **Method:** `GET`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Memeriksa apakah API berjalan aktif.
* **Headers:** `Content-Type: application/json`
* **Response Sukses (200 OK):**
```json
{
  "status": "success",
  "message": "Selamat datang di API ADHD RPG Backend!"
}
```

---

### 2. Pengecekan Database Supabase
* **Method:** `GET`
* **URL:** `https://adhd-rpg-api.vercel.app/db-check`
* **Deskripsi:** Memeriksa koneksi langsung dari server Vercel ke database PostgreSQL Supabase.
* **Headers:** `Content-Type: application/json`
* **Response Sukses (200 OK):**
```json
{
  "status": "success",
  "database": "Terhubung ke Supabase!"
}
```

---

### 3. Tambah User Baru
* **Method:** `POST`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Mendaftarkan pengguna baru dan otomatis menginisialisasi profil awal.
* **Headers:** `Content-Type: application/json`
* **Request Body:**
```json
{
  "username": "petualang_lubna",
  "email": "lubna@example.com",
  "bio": "Misi mengalahkan distraksi dan naik level!"
}
```
* **Response Sukses (201 Created):**
```json
{
  "message": "User baru berhasil dibuat!",
  "data": {
    "id": 1,
    "username": "petualang_lubna",
    "email": "lubna@example.com",
    "level": 1,
    "total_xp": 0
  }
}
```
* **Response Error (400 Bad Request):**
```json
{
  "error": "Field username dan email wajib diisi"
}
```

---

### 4. Ambil Seluruh Data User
* **Method:** `GET`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Mengambil daftar seluruh pengguna terdaftar.
* **Response Sukses (200 OK):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "username": "petualang_lubna",
      "level": 1,
      "total_xp": 0
    }
  ]
}
```

---

### 5. Ambil Profil User Berdasarkan ID
* **Method:** `GET`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Menampilkan data profil karakter pengguna beserta gelar petualang.
* **Response Sukses (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "username": "petualang_lubna",
    "level": 1,
    "total_xp": 0,
    "title": "Pemula"
  }
}
```
* **Response Error (404 Not Found):**
```json
{
  "error": "User tidak ditemukan"
}
```

---

### 6. Tambah Catatan Thought (Brain Dump)
* **Method:** `POST`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Menyimpan catatan ide atau tugas pengguna.
* **Headers:** `Content-Type: application/json`
* **Request Body:**
```json
{
  "user_id": 1,
  "title": "Bereskan meja belajar dan buku",
  "notes": "Fokus 20 menit tanpa membuka media sosial"
}
```
* **Response Sukses (201 Created):**
```json
{
  "message": "Thought berhasil dicatat!",
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "Bereskan meja belajar dan buku"
  }
}
```

---

### 7. Ambil Seluruh Thought
* **Method:** `GET`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Menampilkan seluruh daftar thought yang tersimpan.
* **Response Sukses (200 OK):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Bereskan meja belajar dan buku",
      "notes": "Fokus 20 menit tanpa membuka media sosial",
      "status": "active"
    }
  ]
}
```

---

### 8. Hapus Thought
* **Method:** `DELETE`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Menghapus catatan thought berdasarkan ID.
* **Response Sukses (200 OK):**
```json
{
  "status": "success",
  "message": "Thought berhasil dihapus!"
}
```
* **Response Error (404 Not Found):**
```json
{
  "error": "Thought tidak ditemukan"
}
```

---

### 9. Tambah Quest Baru
* **Method:** `POST`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Menambahkan misi baru (reward XP dihitung otomatis sesuai difficulty: Easy = 50 XP, Medium = 100 XP, Hard = 200 XP).
* **Headers:** `Content-Type: application/json`
* **Request Body:**
```json
{
  "user_id": 1,
  "thought_id": 1,
  "title": "Quest: Taklukkan Meja Belajar",
  "difficulty": "Medium"
}
```
* **Response Sukses (201 Created):**
```json
{
  "message": "Quest berhasil ditambahkan!",
  "data": {
    "id": 1,
    "title": "Quest: Taklukkan Meja Belajar",
    "difficulty": "Medium",
    "xp_reward": 100
  }
}
```

---

### 10. Ambil Seluruh Quest
* **Method:** `GET`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Menampilkan daftar seluruh quest yang tersedia.
* **Response Sukses (200 OK):**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "Quest: Taklukkan Meja Belajar",
      "difficulty": "Medium",
      "is_completed": false
    }
  ]
}
```

---

### 11. Selesaikan Quest (Update XP & Level)
* **Method:** `PUT`
* **URL:** `[suspicious link removed]`
* **Deskripsi:** Mengubah status quest menjadi selesai, menambahkan XP reward ke user, dan menaikkan level user secara otomatis.
* **Headers:** `Content-Type: application/json`
* **Request Body:**
```json
{
  "status": "completed"
}
```
* **Response Sukses (200 OK):**
```json
{
  "message": "Quest selesai! XP berhasil ditambahkan.",
  "data": {
    "quest_id": 1,
    "is_completed": true,
    "user_level": 2,
    "user_total_xp": 100
  }
}
```

---

## 💻 Cara Menjalankan Proyek Secara Lokal

1. **Clone Repository GitHub:**
   ```bash
   git clone [suspicious link removed]
   cd adhd-rpg-api
   ```

2. **Buat dan Aktifkan Virtual Environment:**
   * **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Environment Variable (`.env`):**
   Buat file `.env` di direktori utama proyek:
   ```env
   FLASK_DEBUG=True
   PORT=5000
   DATABASE_URL=postgresql+psycopg2://postgres:PASSWORD_KAMU@db.xxxx.supabase.co:5432/postgres
   ```

5. **Jalankan Aplikasi:**
   ```bash
   python run.py
   ```
   Aplikasi lokal akan berjalan pada `[suspicious link removed]`.

---

## 🧪 Bukti Pengujian API (Testing Evidence)
Pengujian seluruh endpoint CRUD dilakukan menggunakan ekstensi **Thunder Client** langsung pada domain publik Vercel (`[suspicious link removed]`).

Bukti riwayat pengujian tersimpan pada:
* Folder **`docs/`** (kumpulan gambar tangkapan layar respon HTTP status 200, 201).
* File export koleksi: **`thunder-collection.json`**.