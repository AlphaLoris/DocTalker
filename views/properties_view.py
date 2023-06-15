
class PropertiesView:
    def __init__(self, parent):
        self.parent = parent

    def get_properties_from_user(self):
        properties = {}

        def submit():
            properties['API Key'] = api_key_entry.get()
            # ... similar for all properties
            top.destroy()

        top = tk.Toplevel(self.parent)
        top.title("Enter properties")

        api_key_label = tk.Label(top, text="API Key")
        api_key_label.pack()
        api_key_entry = tk.Entry(top)
        api_key_entry.pack()

        # ... similar for all properties

        submit_button = tk.Button(top, text="Submit", command=submit)
        submit_button.pack()

        self.parent.wait_window(top)

        return properties