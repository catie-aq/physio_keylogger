import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainApp:
    """
    Represents a simple application.
    """

    def __init__(self):
        """
        Initializes an instance of the MyApp class.
        """
        self.name = "My Application"

    def run(self):
        """
        Runs the main application loop.
        """
        while True:
            logger.info("Hello, %s", self.name)
            time.sleep(1)


def main():
    """
    Entry point of the application.
    """
    app = MainApp()
    app.run()


if __name__ == "__main__":
    main()
