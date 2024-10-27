import subprocess

def query_mistral(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt, 
            capture_output=True,
            text=True,
            encoding='utf-8', 
            check=True  
        )
        return result.stdout.strip()  
    except subprocess.CalledProcessError as e:
        print(f"error: {e.stderr.strip()}")  
        return None
    except UnicodeDecodeError as e:
        print(f"error directoino: {e}")  
        return None

def main():
    print("input txt model Mistral (in 'exit' для exit):")
    
    while True:
        user_input = input("> ")  
        if user_input.lower() == "exit": 
            print("exit programm")
            break
        
        response = query_mistral(user_input)
        
        if response: 
            print("replay Mistral:")
            print(response)

if __name__ == "__main__":
    main()
