from main import app

if __name__ == "__main__":
    # TODO Remove host and port once hosted on VPS
    app.run(host="localhost", port=5000, debug=True)