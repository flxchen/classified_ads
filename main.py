from app import create_app

app = create_app()
#ngrok http --url=casual-eternal-panther.ngrok-free.app 192.168.50.151:5000
if __name__ == "__main__":
    host="192.168.50.151"
    port=5000
    debug = True
    app.run(debug=True)