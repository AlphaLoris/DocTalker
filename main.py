import logging
from controllers.application_controller import ApplicationController


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Main function
def main():
    setup_logging()
    app_controller = ApplicationController()
    app_controller.view.mainloop()


if __name__ == "__main__":
    main()
