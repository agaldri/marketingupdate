
import os
import subprocess

def create_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Project</title>
    </head>
    <body>
        <h1>Welcome to My Project</h1>
        <p>This is a temporary page to describe my project.</p>
        <p>For inquiries, contact: myemail@example.com</p>
    </body>
    </html>
    """
    os.makedirs("website", exist_ok=True)
    with open("website/index.html", "w") as html_file:
        html_file.write(html_content)
    print("File HTML generato con successo!")

def deploy_to_netlify():
    try:
        # Comando per pubblicare il sito su Netlify
        subprocess.run(["netlify", "deploy", "--prod", "--dir", "website"], check=True)
        print("Sito pubblicato con successo su Netlify!")
    except Exception as e:
        print(f"Errore nel deployment: {e}")

def create_and_deploy_site():
    create_html()
    deploy_to_netlify()

if __name__ == "__main__":
    create_and_deploy_site()
