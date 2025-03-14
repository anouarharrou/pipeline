import psycopg2
import os
from datetime import datetime

def insert_build_record(trigram, company, version, environment, build_url, build_user, build_number, status):
    conn = None
    cursor = None
    try:
        # Database connection details (update these with your actual credentials)
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'jenkins_db'),
            user=os.getenv('DB_USER', 'jenkins_user'),
            password=os.getenv('DB_PASS', 'jenkins_password'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS build_records (
                id SERIAL PRIMARY KEY,
                trigram VARCHAR(10),
                company VARCHAR(255),
                version VARCHAR(50),
                environment VARCHAR(50),
                build_url TEXT,
                build_user VARCHAR(100),
                build_number INTEGER,
                status VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # Insert build record
        cursor.execute('''
            INSERT INTO build_records (trigram, company, version, environment, build_url, build_user, build_number, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        ''', (trigram, company, version, environment, build_url, build_user, build_number, status))
        
        conn.commit()
        print("Record inserted successfully")

    except psycopg2.DatabaseError as db_err:
        print(f"Database error: {db_err}")
    except psycopg2.OperationalError as op_err:
        print(f"Operational error: {op_err}")
    except psycopg2.InterfaceError as intf_err:
        print(f"Interface error: {intf_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    try:
        # Fetch Jenkins environment variables (these should be set in the pipeline)
        trigram = os.getenv('BUILD_TRIGRAM', 'ABC')
        company = os.getenv('COMPANY_DEPLOYED', 'MyCompany')
        version = os.getenv('VERSION_DEPLOYED', '1.0.0')
        environment = os.getenv('ENVIRONMENT', 'dev')
        build_url = os.getenv('BUILD_URL', 'http://jenkins.example.com/job/123/')
        build_user = os.getenv('BUILD_USER', 'jenkins')
        build_number = os.getenv('BUILD_NUMBER', '1')
        status = os.getenv('BUILD_STATUS', 'SUCCESS')

        insert_build_record(trigram, company, version, environment, build_url, build_user, build_number, status)
    except Exception as main_err:
        print(f"Error in main execution: {main_err}")
