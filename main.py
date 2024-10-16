from app import create_app

app = create_app()
if __name__ == "__main__":
    host="192.168.50.151"
    port=5000
    debug = True
    app.run(host,port,debug)