from faker import Faker
import xmltodict
import random
import os

fake = Faker()

def generate_user_data(num_users: int, currency: str) -> dict:
    users = []
    for _ in range(num_users):
        users.append({
            "name": fake.name(),
            "last_name": fake.last_name(),
            "username": fake.user_name(),
            "date_of_birth": fake.date_of_birth(),
            "email": fake.email(),
            "password": fake.password(),
            "role": random.choice(["user", "guest"]),
            "debt": round(random.uniform(1000, 100000), 2),
            "currency": currency,
        })
    return {"root": {"user": users}}

def save_to_xml(data: dict, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    xml_data = xmltodict.unparse(data, pretty=True)
    with open(filename, "w") as file:
        file.write(xml_data)

def generate_and_save_xml(num_records=10000, currency="PLN"):
    print(f"[DEBUG] Generating XML with {num_records} records and currency {currency}")
    data = generate_user_data(num_records, currency.upper())
    save_to_xml(data, "/app/data/generated_users.xml")
    print("[DEBUG] XML successfully written to /app/data/generated_users.xml")
    return True
