from rbz_api.app import app

if __name__ == "__main__":
    app.logger.error("Teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest")
    print("Teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest")
    app.run(host='0.0.0.0', debug=True)
