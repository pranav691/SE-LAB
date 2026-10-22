import json
import sqlite3
from datetime import datetime

# Global state
conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    cur = conn.cursor()
    cur.execute("CREATE TABLE patients (id TEXT, name TEXT, allergy TEXT)")
    cur.execute("INSERT INTO patients VALUES ('P1', 'Kavya', 'penicillin')")
    cur.execute("INSERT INTO patients VALUES ('P2', 'Arjun', 'none')")
    cur.execute("INSERT INTO patients VALUES ('P3', 'Meena', 'ibuprofen')")
    conn.commit()


def find_patient(name):
    cur = conn.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cur.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    if units <= 0:
        raise ValueError("Stock units must be greater than zero.")

    if batch_log is None:
        batch_log = []

    stock[drug] = {
        "units": stock.get(drug, {}).get("units", 0) + units,
        "expiry": expiry,
    }
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    if units <= 0:
        raise ValueError("Dispensing units must be greater than zero.")

    patients = find_patient(patient_name)
    if not patients:
        print("Patient not found:", patient_name)
        return False

    patient_id, allergy = patients[0]

    normalized_drug = drug.strip().casefold()
    normalized_allergy = allergy.strip().casefold()

    if normalized_allergy not in ("", "none") and (
        normalized_drug == normalized_allergy
    ):
        print("Allergy warning for", patient_name)
        return False

    if drug not in stock or stock[drug]["units"] < units:
        print("Insufficient stock for", drug)
        return False

    stock[drug]["units"] -= units
    prescriptions.append(
        {
            "patient": patient_id,
            "drug": drug,
            "units": units,
            "time": str(datetime.now()),
        }
    )
    return True


def expiring_soon(days=30):
    soon = []
    for d in stock:
        exp = datetime.strptime(stock[d]["expiry"], "%Y-%m-%d")
        if (exp - datetime.now()).days < days:
            soon.append(d)
    return soon


def export_prescriptions(file="prescriptions.json"):
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(prescriptions, output_file, indent=4)


def load_stock(file="stock.json"):
    global stock

    try:
        with open(file, "r", encoding="utf-8") as input_file:
            loaded_stock = json.load(input_file)
    except (OSError, json.JSONDecodeError):
        return

    if not isinstance(loaded_stock, dict):
        return

    stock = loaded_stock
    

def print_stock():
    print("Pharmacy Stock")
    for drug, details in stock.items():
        print(
            drug,
            "->",
            details["units"],
            "units, expires",
            details["expiry"],
        )
        

def main():
    setup_database()
    load_stock()
    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", 15, "2026-11-30")
    print("Arjun gets Amoxicillin:", dispense("Arjun", "Amoxicillin", 30))
    print("Kavya gets Penicillin:", dispense("Kavya", "Penicillin", 10))
    print("Meena gets ibuprofen:", dispense("Meena", "ibuprofen", 2))
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5))
    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())
    export_prescriptions()
    print_stock()


main()
