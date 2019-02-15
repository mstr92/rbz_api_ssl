from rbz_api.app import app
import logging.config
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    log = logging.getLogger(__name__)
    log.error(
        "345Teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest")

    app.run(host='0.0.0.0', debug=True)
