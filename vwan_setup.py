import subprocess
import json
import time


def run_azure_cli_command(command, timeout=30):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            raise Exception(f"Error running command: {result.stderr}")
        return result.stdout
    except subprocess.TimeoutExpired:
        raise Exception(f"Command timed out after {timeout} seconds")


def delete_existing_app(app_name):
    existing_apps_output = run_azure_cli_command(f"az ad app list --display-name '{app_name}' --query [].appId")
    existing_apps = json.loads(existing_apps_output)
    for app_id in existing_apps:
        run_azure_cli_command(f"az ad app delete --id {app_id}")


def main():
    # Get Tenant ID, Subscription ID
    print("Fetching Tenant ID and Subscription ID...")
    account_info = json.loads(run_azure_cli_command("az account show"))
    tenant_id = account_info['tenantId']
    subscription_id = account_info['id']

    # Prompt for the Application Name that will be checked or created
    app_name = input("Enter the Azure AD Application Name to check/create: ")

    # Check if the application already exists, if so, delete it
    print(f"Checking for existing applications named {app_name}...")
    delete_existing_app(app_name)

    # Create a new application with Reader Role access
    print("Creating a new application...")
    app_creation_output = run_azure_cli_command(f"az ad app create --display-name '{app_name}'")
    app_details = json.loads(app_creation_output)
    client_id = app_details['appId']

    # Create a service principal for the new application
    print("Creating a service principal for the new application...")
    run_azure_cli_command(f"az ad sp create --id {client_id}")

    # Create a secret for the new application
    print("Creating a secret for the new application...")
    secret_output = run_azure_cli_command(f"az ad app credential reset --id {client_id}")
    secret_details = json.loads(secret_output)
    client_secret = secret_details['password']

    # Assign Reader role to the new application
    print("Assigning Reader role to the new application...")
    scope = f"/subscriptions/{subscription_id}"
    run_azure_cli_command(f"az role assignment create --assignee {client_id} --role Reader --scope '{scope}'")

    # Prompt for the Resource Group Name where the managed app for vWAN was created
    vwan_rg_name = input("Enter the Resource Group name where the managed app for vWAN was created: ")

    managed_apps_ids = []
    managed_rg_name = None

    try:
        # Query for Managed Applications in the specified Resource Group
        managed_apps_output = run_azure_cli_command(f"az resource list --resource-group '{vwan_rg_name}' --resource-type Microsoft.Solutions/applications --query [].id", timeout=60)
        managed_apps_ids = json.loads(managed_apps_output) if managed_apps_output.strip() else []

        for app_id in managed_apps_ids:
            app_details_output = run_azure_cli_command(f"az resource show --ids {app_id} --query properties.managedResourceGroupId", timeout=60)
            app_managed_rg_full_id = json.loads(app_details_output) if app_details_output.strip() else None
            if app_managed_rg_full_id:
                # Extract just the resource group name from the full resource ID
                managed_rg_name = app_managed_rg_full_id.split("/resourceGroups/")[1]
                break
    except Exception as e:
        print(f"Error while querying for Managed Applications: {e}")

    print_results(tenant_id, subscription_id, client_id, client_secret, vwan_rg_name, managed_rg_name)


def print_results(tenant_id, subscription_id, client_id, client_secret, vwan_rg_name, managed_rg_name):
    print(f"Tenant ID: {tenant_id}")
    print(f"Client ID (Application ID): {client_id}")
    print(f"Client Secret (Secret Value): {client_secret}")
    print(f"Subscription ID: {subscription_id}")
    print(f"Managed Resource Group Name: {managed_rg_name}")
    print(f"NVA Name needs be be gathered from the UI")


if __name__ == "__main__":
    main()
