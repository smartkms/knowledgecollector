import os
import requests
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv


load_dotenv()

client_id = os.getenv("CLIENT_ID")
tenant_id = os.getenv("TENANT_ID")
client_secret = os.getenv("CLIENT_SECRET")

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

token = credential.get_token("https://graph.microsoft.com/.default")

headers = {"Authorization": f"Bearer {token.token}", "Content-Type": "application/json"}

url = "https://graph.microsoft.com/v1.0/drive"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("API klic uspešen!")
    print(response.json())  # Prikaz podatkov (če so prisotni)
else:
    print(f"Napaka pri klicu API-ja: {response.status_code}")
    print(response.json())  # Izpiši napako, če je
