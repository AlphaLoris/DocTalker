import csv
import re
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
from packaging.version import parse as parse_version

"""
Loads an .txt file containing a list of native conda packages and a requirements.txt file containing a list of
environment packages and compares the two lists to determine which packages need to be updated or installed.
"""


def select_file(title):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title)
    return file_path


def parse_native_packages(file_path):
    native_packages = {}
    with open(file_path, 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all('td')
            name = columns[0].text
            version = columns[1].text
            in_installer = True if columns[3].find('i') else False
            native_packages[name] = (version, in_installer)
    return native_packages


def parse_environment_packages(file_path):
    env_packages = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith('#'):
                split_line = re.split('=|==', line.strip())
                if len(split_line) == 3:
                    name, version, _ = split_line
                    # Add package info to the env_packages dictionary
                    env_packages[name] = version
                else:
                    pass
    return env_packages


def compare_packages(native_packages, env_packages):
    comparison_table = [['Package', 'In Native', 'Action']]  # Add column names as the first row
    for name, version in env_packages.items():
        if name in native_packages:
            native_version, is_installed = native_packages[name]
            if is_installed and parse_version(native_version) >= parse_version(version):
                action = 'None'
            else:
                action = 'Update'
            comparison_table.append([name, 'Y', action])
        else:
            comparison_table.append([name, 'N', 'Install'])
    return comparison_table


def save_table_to_csv(table, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar='\\')
        for row in table:
            csvwriter.writerow(row)


def main():
    native_packages_file = select_file('Native Conda Packages')
    native_packages = parse_native_packages(native_packages_file)

    environment_packages_file = select_file('Virtual Environment Packages')
    env_packages = parse_environment_packages(environment_packages_file)

    comparison_table = compare_packages(native_packages, env_packages)

    output_file = filedialog.asksaveasfilename(title="Save comparison table as CSV", defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")])
    save_table_to_csv(comparison_table, output_file)


if __name__ == '__main__':
    main()
