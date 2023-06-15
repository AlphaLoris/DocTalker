import yaml

"""
# Load the properties from a YAML file
properties = load_properties('properties.yaml')

# Extract a property
api_key = extract_property(properties, 'API Key')

# Assign a new value to a property
assign_property(properties, 'API Key', 'New API Key Value')

# Persist the changes to the YAML file
persist_properties(properties, 'properties.yaml')
"""


def load_properties(filepath):
    try:
        with open(filepath, 'r') as file:
            properties = yaml.safe_load(file)
        return properties
    except Exception as e:
        print("Could not load properties file. Error: ", str(e))
        properties = get_properties_from_user()
        persist_properties(properties, filepath)
        return properties


def extract_property(properties, property_name):
    keys = property_name.split('.')
    val = properties
    for key in keys:
        val = val[key]
    return val

def get_properties_from_user(parent):
    properties = {}

    def submit():
        properties['API Key'] = api_key_entry.get()
        properties['Index file path'] = index_file_path_entry.get()
        # ... similar for all properties
        top.destroy()

    top = tk.Toplevel(parent)
    top.title("Enter properties")

    api_key_label = tk.Label(top, text="API Key")
    api_key_label.pack()
    api_key_entry = tk.Entry(top)
    api_key_entry.pack()

    index_file_path_label = tk.Label(top, text="Index file path")
    index_file_path_label.pack()
    index_file_path_entry = tk.Entry(top)
    index_file_path_entry.pack()

    # ... similar for all properties

    submit_button = tk.Button(top, text="Submit", command=submit)
    submit_button.pack()

    parent.wait_window(top)

    return properties


def assign_property(properties, property_name, value):
    keys = property_name.split('.')
    val = properties
    for key in keys[:-1]:
        val = val[key]
    val[keys[-1]] = value


def persist_properties(properties, filepath):
    try:
        with open(filepath, 'w') as file:
            yaml.safe_dump(properties, file)
    except Exception as e:
        print("Could not write to properties file. Error: ", str(e))
