import subprocess

def start_gunicorn():
    cmd = [
        "gunicorn",
        "--workers", "1",                     # Numero di worker
        "--timeout", "300",                   # Timeout per ogni richiesta
        "--max-requests", "200",              # Riavvio worker dopo 200 richieste
        "--chdir", "Sorting-Hat/src",         # Cartella di lavoro
        "--bind", "0.0.0.0:8888",             # Indirizzo e porta
        "wsgi:app"                            # Entry point (wsgi.py con "app")
    ]

    print("Starting Gunicorn server...")
    subprocess.run(cmd)

if __name__ == "__main__":
    start_gunicorn()
