import os

def modify_hosts_file(domain, ip_address):
    hosts_path = "/etc/hosts"  # Change this path for Windows or other OS
    backup_path = "/etc/hosts.bak"

    try:
        # Creating a backup
        with open(hosts_path, 'r') as file:
            with open(backup_path, 'w') as backup:
                backup.write(file.read())

        # Adding new entry
        with open(hosts_path, 'a') as file:
            file.write(f"\n{ip_address} {domain} # Added by Python script\n")
            print(f"Added {domain} to hosts file with IP {ip_address}")

    except PermissionError:
        print("Permission denied: Run this script with administrative privileges.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# modify_hosts_file('www.example.com', '127.0.0.1')
