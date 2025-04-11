from app import app

if __name__ == "__main__":
    host = '0.0.0.0'
    port = '8888'
    app.run(host,port,debug=False)
