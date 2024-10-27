from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

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
        return f"Error: {e.stderr.strip()}"
    except UnicodeDecodeError as e:
        return f"Error decoding response: {e}"

@app.route('/')
def home():
    return render_template('index.html')  # html interfesi

@app.route('/query', methods=['POST'])
def query():
    prompt = request.json.get('prompt')  # send text post
    response = query_mistral(prompt)
    return jsonify({'response': response})  # json modul 

if __name__ == "__main__":
    app.run(debug=True)
