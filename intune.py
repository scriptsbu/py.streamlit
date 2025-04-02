import paramiko

def run_command_on_remote(hostname, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

    client.close()

# Example usage
run_command_on_remote('your.remote.hostname', 'your_username', 'your_password', 'ls -la')
