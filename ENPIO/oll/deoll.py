import requests
import os
import subprocess
import paramiko

def send_task_to_ollama(task_description):
    url = "http://localhost:11434/api/generate"
    data = {
        "prompt": task_description,
        "model": "tinyllama",
        "stream": False
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get("response", "Ошибка: код не сгенерирован.")
    else:
        return "Ошибка при обращении к Ollama API."

def log_output(message, level="INFO"):
    with open("output.log", "a", encoding="utf-8") as file:
        file.write(f"{level}: {message}\n")
    print(f"{level}: {message}")

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        log_output(result.stdout)
    except subprocess.CalledProcessError as e:
        log_output(f"Ошибка выполнения команды '{command}': {e.stderr}", level="ERROR")

def connect_ssh(host, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        return ssh
    except Exception as e:
        log_output(f"Ошибка подключения по SSH: {e}", level="ERROR")
        return None

def execute_task(generated_code):
    if "create_directory" in generated_code:
        directory_name = generated_code.split("create_directory('")[1].split("')")[0]
        create_directory(directory_name)
    elif "install_nginx" in generated_code:
        log_output("Устанавливаем Nginx...")
        execute_command("sudo apt update && sudo apt install nginx -y")
        execute_command("sudo systemctl start nginx")
        execute_command("sudo systemctl enable nginx")
        log_output("Nginx установлен и запущен.")
    elif "ssh_command" in generated_code:
        # Пример для выполнения команды по SSH
        host, username, password, command = extract_ssh_info(generated_code)
        ssh = connect_ssh(host, username, password)
        if ssh:
            ssh.exec_command(command)
            ssh.close()
    else:
        log_output("Неизвестная команда, выполните вручную.")

def main():
    log_output("Добро пожаловать в DevOps AI!")
    task_description = input("Опишите задачу для нейросети: ")

    generated_code = send_task_to_ollama(task_description)
    log_output("Сгенерированная команда: " + generated_code)

    if "Ошибка" not in generated_code:
        execute_task(generated_code)
    else:
        log_output(generated_code, level="ERROR")

if __name__ == "__main__":
    main()
