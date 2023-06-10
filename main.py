from controllers.application_controller import ApplicationController


# Main function
def main():
    app_controller = ApplicationController()
    app_controller.view.mainloop()


if __name__ == "__main__":
    main()
