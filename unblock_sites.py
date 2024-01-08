def remove_entry_from_hosts(domain):
  hosts_path = "/etc/hosts"  # For Windows, use 'C:\\Windows\\System32\\drivers\\etc\\hosts'
  backup_path = "/etc/hosts.bak"
  entry_to_remove = f"127.0.0.1 {domain}"

  try:
      # Creating a backup of the current hosts file
      with open(hosts_path, 'r') as file:
          contents = file.readlines()
      
      with open(backup_path, 'w') as backup:
          backup.writelines(contents)

      # Removing the entry
      with open(hosts_path, 'w') as file:
          for line in contents:
              if entry_to_remove not in line:
                  file.write(line)
          print(f"Removed entry for {domain} from hosts file.")

  except PermissionError:
      print("Permission denied: Run this script with administrative privileges.")
  except Exception as e:
      print(f"An error occurred: {e}")

# Example usage
# remove_entry_from_hosts('www.example.com')