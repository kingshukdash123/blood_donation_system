from app.db.connection import create_db_connection


def is_exist_user(phone: str):
    conn = create_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE phone=%s", (phone,))
    user = cur.fetchone()

    cur.close()
    conn.close()
    return user


def create_user_query(user):
    conn = create_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (name, phone, password_hash, role, is_verified)
        VALUES (%s, %s, %s, %s, %s)
    """, (user.name, user.phone, user.password, user.role, user.isVerified))

    conn.commit()
    user_id = cur.lastrowid

    cur.close()
    conn.close()
    return user_id


def create_hospital_profile(user_id, user):
    conn = create_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO hospitals (user_id, hospital_name, latitude, longitude, address)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, user.name, user.latitude, user.longitude, user.address))

    conn.commit()
    cur.close()
    conn.close()


def create_blood_bank_profile(user_id, user):
    conn = create_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO blood_banks (user_id, blood_bank_name, latitude, longitude, address)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, user.name, user.latitude, user.longitude, user.address))

    conn.commit()
    cur.close()
    conn.close()


def create_donor_profile(user_id, user):
    conn = create_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO donors (
            user_id, blood_group, last_donation_date,
            is_available, latitude, longitude, address
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        user.bloodGroup,
        user.lastDonationDate,
        user.isAvailable,
        user.latitude,
        user.longitude, 
        user.address
    ))

    conn.commit()
    cur.close()
    conn.close()


def fetch_user_by_phone(phone: str):
    conn = create_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE phone=%s", (phone,))
    user = cur.fetchone()

    cur.close()
    conn.close()
    return user
