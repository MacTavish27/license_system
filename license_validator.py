import json
import sys
import uuid
import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import os

def get_machine_id():
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

def verify_license(license_path, public_key_path="public_key.pem"):
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        license_path = os.path.join(base_path, license_path)
        public_key_path = os.path.join(base_path, public_key_path)

        with open(license_path, "r") as f:
            data = json.load(f)

        license_data = data["license"]
        signature = bytes.fromhex(data["signature"])

        with open(public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        payload = json.dumps(license_data, separators=(",", ":"), sort_keys=True).encode()
        public_key.verify(
            signature,
            payload,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )

        if license_data["machine_id"] != get_machine_id():
            print("License not valid for this machine!")
            return False

        expiry_str = license_data.get("expiry", "Unlimited")
        if expiry_str != "Unlimited":
            expiry = datetime.datetime.fromisoformat(expiry_str.replace("Z", ""))
            if datetime.datetime.utcnow() > expiry:
                print("License expired!")
                return False

        print("License verified successfully!")
        return True

    except FileNotFoundError:
        print("License file or public key not found!")
        return False
    except ValueError:
        print("License file format is invalid!")
        return False
    except Exception as e:
        print(f"License verification failed: {e}")
        return False
