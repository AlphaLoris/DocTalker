import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd

# TODO: track cost of each chat session
# TODO: allow the admin to set a budget for each chat session
# TODO: track number of queries in each chat session
# TODO: track duration of each chat session


class LaunchWindow(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.launch_button = None
        self.org_entry = None
        self.org_label = None
        self.name_entry = None
        self.name_label = None
        self.email_entry = None
        self.email_label = None

        self.title("Chat Session Info")
        self.geometry("250x300")

        # User email
        self.email_label = tk.Label(self, text="Email Address:")
        self.email_label.pack(padx=20, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(padx=20, pady=5)

        # User name
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack(padx=20, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(padx=20, pady=5)

        # User organization
        self.org_label = tk.Label(self, text="Organization:")
        self.org_label.pack(padx=20, pady=5)
        self.org_entry = tk.Entry(self)
        self.org_entry.pack(padx=20, pady=5)

        # Initiate Chat Session Button
        self.launch_button = tk.Button(self, text="Initiate Chat Session", command=self.controller.open_chat_session)
        self.launch_button.pack(padx=20, pady=10)


class ChatSessionsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self.configure(bg="white")  # Set the background color to white for better visibility

        # Initialize DataFrame
        self.df = pd.DataFrame(columns=[
            'Chat session ID', 'User email address', 'User name', 'User organization',
            'Start date', 'Start time', 'Duration', 'Current sentiment',
            'Cost', 'Number of user queries', 'Number of prompts', 'Keywords/Topics'
        ])

        for col in range(11):
            self.columnconfigure(col, weight=1)

        # Configure rows if necessary
        for row in range(11):
            self.rowconfigure(row, weight=1)

        # Add a simple label to the PromptsTab
        self.label = tk.Label(self, text="Chat Sessions", bg="white")
        self.label.grid(row=0, column=5, rowspan=1, columnspan=2, padx=10, pady=10)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=1, column=0, rowspan=1, columnspan=12)

        # Add a "Launch Chat Session" button to the ChatSessionsTab
        self.launch_chat_session_button = tk.Button(self, text="Launch Chat Session", width=18)
        self.launch_chat_session_button.grid(row=1, column=5, padx=10, pady=10)
        self.end_chat_session_button = tk.Button(self, text="End Chat Session", width=18)
        self.end_chat_session_button.grid(row=1, column=6, padx=10, pady=10)

        # Create a frame to hold the treeview and scrollbars
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=2, column=0, columnspan=11, rowspan=9, padx=5, pady=5, sticky='nsew')

        # Configure the frame's column and row weights (this makes them expandable)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Add a Treeview to the frame
        self.tree = ttk.Treeview(tree_frame)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Create vertical scrollbar and associate it with the Treeview
        self.yscrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.yscrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.yscrollbar.set)

        # Create horizontal scrollbar and associate it with the Treeview
        self.xscrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.xscrollbar.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=self.xscrollbar.set)

        # Hide the tree column
        self.tree.column("#0", width=0, stretch=tk.NO)

        # Define columns
        self.tree["columns"] = tuple(self.df.columns)

        # Define heading
        for index, column in enumerate(self.df.columns, start=1):
            self.tree.column(f"#{index}", anchor=tk.W, width=60)  # Reduced column width
            self.tree.heading(f"#{index}", text=column, anchor=tk.W)

        # Populate Treeview with data from DataFrame
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def set_controller(self, chat_sessions_controller):
        self.controller = chat_sessions_controller
        # Now that the controller is set, configure the launch chat session button command
        self.configure_launch_chat_session_button_command()
        self.configure_end_chat_session_button_command()

    def configure_launch_chat_session_button_command(self):
        # Set the command attribute of the launch_chat_session_button
        self.launch_chat_session_button.config(command=self.controller.initiate_chat_session)

    def configure_end_chat_session_button_command(self):
        # Set the command attribute of the end_chat_session_button
        self.end_chat_session_button.config(command=self.controller.end_chat_session)

    def update_sessions(self, chat_session_model):
        # Update the DataFrame
        index = self.df[self.df['Chat session ID'] == chat_session_model.chat_session_id].index
        if len(index) > 0:
            # Update existing row
            index = index[0]
            self.df.loc[index, 'User email address'] = chat_session_model.user_email
            self.df.loc[index, 'User name'] = chat_session_model.user_name
            self.df.loc[index, 'User organization'] = chat_session_model.user_organization
            self.df.loc[index, 'Start date'] = chat_session_model.start_date
            self.df.loc[index, 'Start time'] = chat_session_model.start_time
            self.df.loc[index, 'Duration'] = chat_session_model.duration
            self.df.loc[index, 'Current sentiment'] = chat_session_model.sentiment
            self.df.loc[index, 'Cost'] = chat_session_model.cost
            self.df.loc[index, 'Number of user queries'] = chat_session_model.query_count
            self.df.loc[index, 'Number of prompts'] = chat_session_model.prompt_count
            self.df.loc[index, 'Keywords/Topics'] = chat_session_model.keywords
        else:
            # Add new row if not existing
            new_row = pd.DataFrame([{
                'Chat session ID': chat_session_model.chat_session_id,
                'User email address': chat_session_model.user_email,
                'User name': chat_session_model.user_name,
                'User organization': chat_session_model.user_organization,
                'Start date': chat_session_model.start_date,
                'Start time': chat_session_model.start_time,
                'Duration': chat_session_model.duration,
                'Current sentiment': chat_session_model.sentiment,
                'Cost': chat_session_model.cost,
                'Number of user queries': chat_session_model.query_count,
                'Number of prompts': chat_session_model.prompt_count,
                'Keywords/Topics': chat_session_model.keywords
            }])
            self.df = pd.concat([self.df, new_row], ignore_index=True)

        # Refresh the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=list(row))



