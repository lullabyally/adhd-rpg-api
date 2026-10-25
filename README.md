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

==================================================
DOKUMENTASI ENDPOINT REST API - ADHD RPG
==================================================

### 1. Endpoint Tambah User
- Method       : POST
- URL          : https://adhd-rpg-api.vercel.app/users
- Deskripsi    : Menambahkan pengguna baru dan membuat profil otomatis
- Headers      : Content-Type: application/json
- Request Body :
  {
    "username": "Explorer 01",
    "email": "Rawr@example.com",
    "bio": "Misi mengalahkan distraksi dan naik level!"
  }
- Response Sukses (201):
  {
    "message": "User baru berhasil dibuat!",
    "data": { "id": 1, "username": "Explorer 01", "level": 1, "total_xp": 0 }
  }
- Response Error (400):
  {
    "error": "Field username dan email wajib diisi"
  }

--------------------------------------------------

### 2. Endpoint Tambah Catatan (Thought)
- Method       : POST
- URL          : https://adhd-rpg-api.vercel.app/thoughts
- Deskripsi    : Mencatat ide/tugas baru (brain dump) sebelum dijadikan quest
- Headers      : Content-Type: application/json
- Request Body :
  {
    "user_id": 1,
    "title": "Bereskan meja belajar",
    "notes": "Fokus 20 menit"
  }
- Response Sukses (201):
  {
    "message": "Thought berhasil dicatat!",
    "data": { "id": 1, "user_id": 1, "title": "Bereskan meja belajar" }
  }
- Response Error (400):
  {
    "error": "Field title dan user_id wajib diisi"
  }

--------------------------------------------------

### 3. Endpoint Tambah Quest
- Method       : POST
- URL          : https://adhd-rpg-api.vercel.app/quests
- Deskripsi    : Membuat quest baru (reward XP dihitung otomatis: Easy=50, Medium=100, Hard=200)
- Headers      : Content-Type: application/json
- Request Body :
  {
    "user_id": 1,
    "thought_id": 1,
    "title": "Quest: Taklukkan Tugas Back End",
    "difficulty": "Hard"
  }
- Response Sukses (201):
  {
    "message": "Quest berhasil ditambahkan!",
    "data": { "id": 1, "title": "Quest: Taklukkan Tugas Back End", "difficulty": "Hard", "xp_reward": 100 }
  }

--------------------------------------------------

### 4. Endpoint Selesaikan Quest & Tambah XP
- Method       : PUT
- URL          : https://adhd-rpg-api.vercel.app/1
- Deskripsi    : Menyelesaikan quest dan otomatis menambahkan XP serta mengupdate level user
- Headers      : Content-Type: application/json
- Request Body :
  {
    "status": "completed"
  }
- Response Sukses (200):
  {
    "message": "Quest selesai! XP berhasil ditambahkan.",
    "data": { "quest_id": 1, "is_completed": true, "user_level": 2, "user_total_xp": 100 }
  }
- Response Error (404):
  {
    "error": "Quest tidak ditemukan"
  }

--------------------------------------------------

### 5. Endpoint Hapus Catatan (Thought)
- Method       : DELETE
- URL          : https://adhd-rpg-api.vercel.app/2
- Deskripsi    : Menghapus data thought berdasarkan ID
- Headers      : Content-Type: application/json
- Request Body : (Kosong)
- Response Sukses (200):
  {
    "status": "success",
    "message": "Thought berhasil dihapus!"
  }
- Response Error (404):
  {
    "error": "Thought tidak ditemukan"
  }