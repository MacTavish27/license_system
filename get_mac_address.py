import uuid

def get_machine_id():
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))

if __name__ == "__main__":
    print("Machine ID:", get_machine_id())
    input("\nPress Enter to exit...")   