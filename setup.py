from keycloak import KeycloakAdmin
import sys

# Keycloak Configuration
keycloak_url = "http://localhost:8080/"
admin_username = "keycloak"
admin_password = "password"

# Configuration for new Realm, Client, and User
realm_name = "sso"
client_id = "sso-client"
username = "ruslan"
user_email = "ruslanguns@gmail.com"
user_password = "123456"
redirect_uris = ["http://localhost:3001/*", "http://localhost:3002/*", "http://localhost:3003/*"]

# Create an instance of KeycloakAdmin
keycloak_admin = KeycloakAdmin(server_url=keycloak_url,
                               username=admin_username,
                               password=admin_password,
                               realm_name="master",
                               client_id="admin-cli",
                               verify=True)

def resource_exists(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        return True
    except Exception as e:
        if 'Conflict' in str(e):
            return True
        return False

def create_or_update_realm():
    if not resource_exists(keycloak_admin.create_realm, payload={"realm": realm_name, "enabled": True}):
        print("Realm already exists. No changes made.")
    else:
        print("Realm created or updated successfully.")

def create_or_update_client():
    keycloak_admin.connection.realm_name = realm_name

    try:
        clients = keycloak_admin.get_clients()
        client = next((c for c in clients if c['clientId'] == client_id), None)

        client_config = {
            "clientId": client_id,
            "directAccessGrantsEnabled": True,
            "publicClient": True,
            "redirectUris": redirect_uris
        }

        if client:
            keycloak_admin.update_client(client_id=client['id'], payload=client_config)
            print("Client updated successfully.")
        else:
            keycloak_admin.create_client(payload=client_config)
            print("Client created successfully.")
    except Exception as e:
        print(f"Error creating or updating the client: {e}")

def create_or_update_user():
    keycloak_admin.connection.realm_name = realm_name

    try:
        users = keycloak_admin.get_users()
        user = next((u for u in users if u['username'] == username), None)

        user_config = {
            "username": username,
            "email": user_email,
            "emailVerified": True,
            "enabled": True,
            "credentials": [{"type": "password", "value": user_password, "temporary": False}]
        }

        if user:
            keycloak_admin.update_user(user_id=user['id'], payload=user_config)
            print("User updated successfully.")
        else:
            keycloak_admin.create_user(payload=user_config)
            print("User created successfully.")
    except Exception as e:
        print(f"Error creating or updating the user: {e}")

def cleanup():
    try:
        keycloak_admin.delete_realm(realm_name)
        print(f"Realm '{realm_name}' and all related resources deleted successfully.")
    except Exception as e:
        print(f"Error deleting the realm: {e}")

# Check for cleanup argument
if len(sys.argv) > 1 and sys.argv[1] == 'cleanup':
    cleanup()
else:
    create_or_update_realm()
    create_or_update_client()
    create_or_update_user()
