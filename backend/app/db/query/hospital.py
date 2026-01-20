from app.db.connection import create_db_connection
from app.schema.hospital import CreateBloodRequest


def createBloodRequest(bloodRequestDetails: CreateBloodRequest):
    conn = None
    curr = None

    try:
        conn = create_db_connection()
        curr = conn.cursor(dictionary=True)

        query = """
        INSERT INTO blood_requests
        (hospital_id, blood_group, units_required, status, blood_bank_id)
        VALUES (%s, %s, %s, %s, %s)
        """

        curr.execute(query, (
            bloodRequestDetails.hospitalId,
            bloodRequestDetails.bloodGroup,
            bloodRequestDetails.unitsRequired,
            bloodRequestDetails.status,
            bloodRequestDetails.bloodBankId
        ))

        conn.commit()

        return {
            "message": "Blood request created successfully",
            "request_id": curr.lastrowid
        }

    except Exception as e:
        raise e

    finally:
        if curr:
            curr.close()
        if conn:
            conn.close()
