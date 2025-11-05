import json
import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def create_license(machine_id, days_valid=None, features=None):
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    if days_valid is not None:
        expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=days_valid)).isoformat() + "Z"
    else:
        expiry = "Unlimited"

    license_data = {
        "machine_id": machine_id,
        "expiry": expiry,
        "features": features or {}
    }

    payload = json.dumps(license_data, separators=(",", ":"), sort_keys=True).encode()
    signature = private_key.sign(
        payload,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    license_file = {
        "license": license_data,
        "signature": signature.hex()
    }

    filename = f"license_{machine_id.replace(':','')}.json"
    with open(filename, "w") as f:
        json.dump(license_file, f, indent=4)

    print(f"\nLicense generated successfully!")
    print(f"Machine ID: {machine_id}")
    print(f"Expiry: {expiry}")
    print(f"Saved as: {filename}")

if __name__ == "__main__":
    print("=== License Generator ===")
    machine_id = input("Enter target machine MAC address (e.g. 34:48:ED:3E:B3:93): ").strip()
    days_input = input("Enter license duration in days (press Enter for unlimited): ").strip()
    
    days_valid = int(days_input) if days_input else None
    create_license(machine_id, days_valid)
