import requests
import subprocess

def generate_code_with_neural_network(task_description):
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
        return "Ошибка при обращении к нейросети."

def create_and_write_file(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Код записан в файл '{filename}'.")

def execute_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e.stderr}")

def main():
    print("Добро пожаловать! Дайте задачу нейросети.")
    task_description = input("Введите задание для нейросети: ")

    generated_code = generate_code_with_neural_network(task_description)

    if generated_code.startswith("Ошибка"):
        print(generated_code)
    else:
        
        filename = task_description.replace(" ", "_").lower() + ".py"
        
        create_and_write_file(filename, generated_code)

        print("Файл успешно создан.")
        
        if "docker" in task_description.lower():
            print("Запуск команды для создания Docker-контейнера...")
            execute_command(["docker", "build", "-t", "my_image", "."]) 
            execute_command(["docker", "run", "-d", "--name", "my_container", "my_image"])

if __name__ == "__main__":
    main()
