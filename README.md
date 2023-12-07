## Azure AD Application Management and Role Assignment Script for Check Point Management Integration

This Python script is specifically designed to gather information and prepare roles required for running the `cme_menu` script on a Check Point Management system. Its primary function is to automate the onboarding of Azure Gateways deployed in virtual WANs (vWANs) to the Check Point Management system.

### Purpose and Integration
- **Targeted Use Case**: The script sets the stage for integrating Azure Gateways with Check Point Management, facilitating automatic onboarding.
- **Preparation for `cme_menu` Execution**: It ensures all necessary prerequisites, such as application creation, role assignment, and service principal setup, are in place for the `cme_menu` script to function smoothly.

### Key Features
1. **Azure AD Application Management**: Manages Azure AD applications, crucial for granting the `cme_menu` script the access it needs.
2. **Service Principal and Secret Creation**: Sets up service principals and secrets, which are essential for secure communication between Azure and Check Point Management.
3. **Role Assignment for Access Control**: Assigns roles like 'Reader' to facilitate the right level of access for the `cme_menu` script.
4. **Managed Application Querying**: Gathers necessary details from Managed Applications in vWANs, which are pertinent to the Check Point Management integration.

### Usage in the Context of Check Point Management
1. **Initial Setup**: Before running the `cme_menu` script, execute this Python script to ensure all prerequisites are met.
2. **Providing Necessary Details**: The script will prompt for input such as Azure AD Application name and Resource Group name, which are critical for the onboarding process.
3. **Output Information**: The script will output details like Tenant ID, Client ID, and Secret, which might be required for further configuration in the Check Point Management.

### Additional Notes
- **Security**: As the script deals with sensitive information, including client secrets, ensure it is run in a secure environment with appropriate permissions.
- **Dependencies**: Requires Azure CLI and a Python environment capable of executing subprocess commands.

---

This readme enhancement clearly outlines the script's specific role in the context of Check Point Management, detailing its importance in the automated onboarding process of Azure Gateways to Check Point Management systems.
