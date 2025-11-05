import uuid
from license_validator import verify_license

def get_machine_id():
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

license_file = f"license_{get_machine_id().replace(':', '')}.json"

if __name__ == "__main__":
    if verify_license(license_file):
        print("Running the app...")
    else:
        print("Application terminated due to invalid or expired license.")
