import sqlite3

DATABASE_FILE = "gosdb.db"  # Ganti dengan nama yang Anda inginkan

def create_database():
    """Membuat database SQLite dan tabel-tabel yang diperlukan."""

    conn = None  # Inisialisasi conn di luar blok try

    try:
        # Hubungkan ke database (atau buat jika belum ada)
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Aktifkan foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        print("Foreign key constraints diaktifkan.")

        # Buat tabel Clients
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clients (
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name VARCHAR(255) NOT NULL,
                industry VARCHAR(255),
                contact_person VARCHAR(255),
                priority INTEGER,
                satisfaction_score REAL,
                billing_address TEXT,
                shipping_address TEXT
            )
        """)
        print("Tabel 'Clients' berhasil dibuat.")

        # Buat tabel Projects
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                project_name VARCHAR(255) NOT NULL,
                description TEXT,
                start_date DATE,
                end_date DATE,
                budget REAL,
                risk_score REAL,
                status VARCHAR(50),
                estimated_profit_margin REAL,
                project_manager_id INTEGER, -- Menambahkan kolom project_manager_id
                FOREIGN KEY (client_id) REFERENCES Clients(client_id),
                FOREIGN KEY (project_manager_id) REFERENCES Resources(resource_id) -- Foreign key ke Resources
            )
        """)
        print("Tabel 'Projects' berhasil dibuat.")

        # Buat tabel Resources
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Resources (
                resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255),
                title VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(20),
                hourly_rate REAL,
                availability REAL,
                department_id INTEGER,
                team_id INTEGER,
                location VARCHAR(255),
                FOREIGN KEY (department_id) REFERENCES Departments(department_id),
                FOREIGN KEY (team_id) REFERENCES Teams(team_id)
            )
        """)
        print("Tabel 'Resources' berhasil dibuat.")

        # Buat tabel Skills
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Skills (
                skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_name VARCHAR(255) NOT NULL,
                skill_description TEXT
            )
        """)
        print("Tabel 'Skills' berhasil dibuat.")

        #Buat Tabel Departments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Departments (
                department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_name VARCHAR(255) NOT NULL,
                department_head_id INTEGER,
                FOREIGN KEY (department_head_id) REFERENCES Resources(resource_id)
            )
        """)
        print("Tabel 'Departments' berhasil dibuat.")

        #Buat Tabel Teams
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Teams(
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name VARCHAR(255) NOT NULL,
                team_lead_id INTEGER,
                FOREIGN KEY (team_lead_id) REFERENCES Resources(resource_id)
            )
        """)
        print("Tabel 'Teams' berhasil dibuat.")

        #Buat Tabel Tasks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                task_name VARCHAR(255) NOT NULL,
                description TEXT,
                estimated_hours REAL,
                actual_hours REAL,
                status VARCHAR(50),
                priority INTEGER,
                FOREIGN KEY (project_id) REFERENCES Projects(project_id)
            )
        """)
        print("Tabel 'Tasks' berhasil dibuat.")

        #Buat Tabel ResourceSkills
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ResourceSkills (
                resource_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                PRIMARY KEY (resource_id, skill_id),
                FOREIGN KEY (resource_id) REFERENCES Resources(resource_id),
                FOREIGN KEY (skill_id) REFERENCES Skills(skill_id)
            )
        """)
        print("Tabel 'ResourceSkills' berhasil dibuat.")

        #Buat Tabel ProjectSkills
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ProjectSkills (
                project_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                PRIMARY KEY (project_id, skill_id),
                FOREIGN KEY (project_id) REFERENCES Projects(project_id),
                FOREIGN KEY (skill_id) REFERENCES Skills(skill_id)
            )
        """)
        print("Tabel 'ProjectSkills' berhasil dibuat.")

        #Buat Tabel Assignments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Assignments (
                assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                resource_id INTEGER NOT NULL,
                task_id INTEGER NULL,
                start_date DATE,
                end_date DATE,
                allocated_hours REAL,
                actual_hours REAL,
                role VARCHAR(255),
                FOREIGN KEY (project_id) REFERENCES Projects(project_id),
                FOREIGN KEY (resource_id) REFERENCES Resources(resource_id),
                FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
            )
        """)
        print("Tabel 'Assignments' berhasil dibuat.")

        #Buat Tabel Costs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Costs (
                cost_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                resource_id INTEGER,
                date DATE,
                description TEXT,
                amount REAL,
                cost_type VARCHAR(255),
                FOREIGN KEY (project_id) REFERENCES Projects(project_id),
                FOREIGN KEY (resource_id) REFERENCES Resources(resource_id)
            )
        """)
        print("Tabel 'Costs' berhasil dibuat.")

        #Buat Tabel Revenues
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Revenues (
                revenue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                date DATE,
                description TEXT,
                amount REAL,
                FOREIGN KEY (project_id) REFERENCES Projects(project_id)
            )
        """)
        print("Tabel 'Revenues' berhasil dibuat.")

        # Commit perubahan
        conn.commit()
        print("Perubahan di-commit ke database.")

    except sqlite3.Error as e:
        print(f"Terjadi kesalahan SQLite: {e}")

    finally:
        if conn:
            conn.close()
            print("Koneksi ke database ditutup.")


if __name__ == "__main__":
    create_database()
