# TODO: Description of the application
"""
The application will parses the documents in the directory into section-based chunks, embed those chunks as vectors,
and store those vectors in a FAISS vector database. These documents will used by the application to answer user
questions by providing relevant portions of the document to the LLM along with the user's query and ask the LLM to use
the document content to answer the user's question.  The application will preserve a history of the interactions between
the application and the user to provide context to the model
"""
#
# Chat Response:
# - Response, if confident enough to provide one
# - Does the provided documentation address the user's query?
# - User's Sentiment in query
#
# TODO: We create a properties view, but it is not used. We may want to add it to the Admin window. I believe it sets
#  the default values for the chat sessions.
#
# TODO: Application Logic
#
# Load Documents
# Chunk Documents
# Embed Documents
# Create FAISS Index
#
# Get Query
# Embed Query
# Search Vector Database with Query Vector
#
# Create Chat History
# Add Query to Chat History
# Summarize/compress Chat History
#
# Compile Prompt
# Submit Prompt
# Parse  Response
# Evaluate Response
# Dispose of Response
# Present Response

# TODO: Business
#    - Understand commercial licensing requirements for resources used in this project
#    - Understand the legal requirements for using the OpenAI API
#
# TODO: Code
#    - Standardize the way a controller interacts with its view
#    - Maybe use Faiss w/o GPU support and w/o Conda
#    - Analyze code with Pylint, Pydeps and mypy, radon or wily
#    - Add docstrings to the components
#    - Add Logging to the components
#    - Add unit tests to the components
#
# TODO: Environment
#    - Add a setup wizard that sets up the environment and configures the application
#
# TODO: Optimization
#    - Optimize text division
#    - Optimize Index type
#    - Optimize Similarity calculation type
#    - Optimize number of results returned - User control
#    - Optimize method of assembling results into prompt
#    - Optimize prompt composition/characteristics/technique
#    - Optimize response validation
#    - Optimize nlist and nprobe for Faiss index
#
# TODO: Chatbot System
#    - Remove the OPENAI API KEY from the code and use a config file instead
#    - Backup of all Data
#    - Use a visual representation tool like Nomic to map queries against the user manual content to identify problem
#       areas
#    - Capture the questions the model had trouble answering and use them to improve the documentation
#         - Low ratings from user
#         - Low confidence from the model
#    - Personalization of the chatbot based on the user's name, role, conference, chat history, etc.
#    - Responsive to the user's mood/emotional state
#
# TODO: Properties/Configuration
#    - Model parameters: Model, temperature, top_p, n, stream, max_tokens, presence_penalty, frequency_penalty
#    - costs per token
#    - Allow the admin user to choose the level of error checking
#    - n_list, nprobe parameters for Faiss
#
# TODO: Database
#
# TODO: Document Management
#    - Inventory of documents
#    - Add new documents
#    - Remove documents
#    - Backing up of data - Directory, primary/secondary backup versions
#    - Restore previous state from backup
#    - Progress bar for documents upload
#    - Segregate the documents the user uploads into different repositories based on the user's intent.
#    - Figure out how the document parser is treating bulleted lists and numbered lists and any other special cases.
#    - Page Numbers are not working. Would need to develop a new approach to parsing .docx files to get page numbers.
#
# TODO: Semantic search
#    - Keyword/Entity Search
#    - Progress bar for parsing/embedding, indexing
#    - Figure out a way to leverage the chunk size and overlap controls and maybe the splitting methodology of this
#         script along with text_block_extractor.py to get the best of both worlds.
#    - It may make sense to add a reference to the document node that the sentence belongs to.
#    - Include headings in the chunk text
#    - Develop ways to evaluate and understand the semantic search performance
#    - Develop ways to understand the relative characteristics of the embeddings
#    - Do the first and last sentences within this node have links to the sentences in the previous and next
#         nodes?
#
# TODO: LLM
#    - Expose all behavioral parameters to the user: Model parameters, Tokenizer parameters, error checking, etc.
#
# TODO: Prompt
#    - Control over number of neighbors returned and included in the prompt
#    - Control over the prompt composition/characteristics/technique
#
# TODO: Response validation
#
# TODO: Administration of Chat Sessions
#    - View current Chat AI Context (the chat history provided as part of the prompt to the AI)
#    - Startup/Shutdown Chat
#    - Track cost of each chat session
#    - Allow the admin to set a budget for each chat session
#    - Track number of queries in each chat session
#    - Track duration of each chat session
#    - Chat Sessions Admin window
#         - Chat session ID
#         - User email address
#         - User name
#         - User organization
#         - Display the start time
#         - Display Start date of each chat session
#         - Display running duration of each chat session
#         - Display the current sentiment of the chat session
#         - Display the running cost of each chat session
#         - Display number of user queries submitted in each chat session
#         - Display the number of prompts submitted in each chat session
#         - Keywords/Topics of each chat session
#
# TODO: Individual Chat session Interface Features
#    - Chat session introduction
#         - Alert User that they are talking to an AI chatbot
#         - Alert User that the chatbot is trained on the User Manual
#         - Tell user how to reach a human
#         - Assign each chat session a unique ID and use it in API calls
#         - Get user email address at the start of each chat session
#         - Access to other means of communicating with humans for support
#         - Capture start time and date of each chat session
#    - Terminating the chat session
#         - May want to handle this like an onion so that the user launches the session, then launches it again so they
#              know they can rate the session after it ends before they start
#         - Alert User that the chat session is ending
#         - Alert User that they can rate the chat session
#         - Alert User that they can provide feedback on the chat session
#         - Alert User that they can save the chat session
#         - Alert User that they can email the chat session
#    - Chat Sessions History window
#         - History of all chat sessions
#         - Access to previous chat sessions
#         - When a chat session ends, it is moved from the Chat Sessions Admin window to the Chat Sessions History
#              window
#    - Testing Chat Session Interface
#    - User Chat session history window
#         - Memory of previous conversations with User
#         - Delete Chat session history
#         - Access to previous chat sessions (view/continue/search)
#         - Ability to save/export the chat session to file and maybe email
#         - Ability to ask the User to provide feedback on the chatbot session as a whole
#    - Chat Session
#         - Chat window
#              - Support for multiple languages
#              - Complex user input: Multiple sentences, paragraphs, carriage returns etc.
#              - Scrollable Window
#              - Expandable Window
#              - Paste into the chat window
#              - Select text in chat window
#              - Cut selected text from chat window
#              - Copy selected text from chat window
#              - Ability to edit the text in the chat window
#              - Ability to delete the text in the chat window
#              - Visual differentiation of chatbot responses from User input
#              - User control over the size of the text in the chat window
#              - Streaming chat w typing indicator
#              - Markdown or formatting options: Enables users to format text (bold, italic, etc.) for clarity.
#              - Emojis and Stickers: Allows users to express emotions through visual elements.
#              - Ability to handle links
#              - Ability to add images
#              - Ability to add code blocks w preserved formatting
#              - Ability to add lists and outlines
#              - Support for quoting previous messages
#              - Ability to add special characters
#              - Ability to add hashtags
#              - Editing: Allow users to edit their messages after sending (updating the recipient).
#              - Deleting: Allow users to delete their messages after sending (updating the recipient).
#              - Message status indicators (e.g., sent, delivered, read)
#              - Auto-correction and suggestions: Helps users in correcting typos and facilitates faster typing.
#              - Auto-complete: Helps users in completing the word they are typing based on the first few letters that
#                   they have typed.
#              - Ability to add attachments
#              - Ability to add tables
#              - Ability to add videos
#              - Ability to add audio
#              - Ability to add horizontal rules
#              - Ability to add mentions
#              - Command shortcuts: For example, users could type /help to quickly access a help menu.
#         - Chat history window
#              - Scroll the chat history window
#              - Alert User when the chatbot is not confident about the answer
#              - Ability to ask the User to provide feedback on individual answers
#              - Answers should provide reference to the User Manual section/page number
#              - Search message history
#         - Submit button
#         - End chat button
#         - Jump to the top/bottom of the chat window
#         - Restart chat button
#              - Discard session memory
#              - Empty Chat session window
#         - Access to other means of communicating with humans for support

# User clicks on "New Chat Session" button
# Chat sessions controller creates a new chat session controller, model and view
# Chat sessions controller registers itself as an observer of the chat session model
# Chat sessions controller adds the chat session controller to its list of chat sessions
# Chat session controller updates the chat session model with the info about the new chat session
# Chat session model updates its observers (chat sessions controller) with the new chat session info
# Chat sessions controller updates its model with the new chat session info
# Chat sessions model updates notifies is observer (chat sessions view) with the new chat session info
# Chat sessions view updates its list of chat sessions with the new chat session info
# The user enters a query in the chat session view and submits it to the chat session controller
# The chat session controller validates the query. If it is valid, it updates the chat session model with the query
# The chat session model updates its chat history with the new query
# The chat session model updates its observer (chat session view) with the new query
# The chat session view updates its chat history with the new query
# The chat session model embeds the query and performs a semantic search using the query
# The chat session model assembles the search result into a prompt
# The chat session passes the query and the prompt to the LLM controller
# The LLM controller submits the prompt to the LLM model
# The LLM controller updates the history of prompts
# The LLM model generates a response to the prompt
# The LLM model validates the response and iterates (with human input?) until the response is valid
# The LLM identifies when it can't answer the query using the semantic search result
# If semantic search result does not speak to the query,
#    the query is added to the list of questions that need to be answered in the documents
# The LLM model passes its response to the LLM controller
# The LLM controller updates chat controller with the response
# The LLM controller updates the Chat Session model with the response
# The Chat Session model updates its chat history with the response
# The Chat Session model notifies view of the update to its chat
# The Chat Session view updates its chat history with the response


# TODO: Dedup this list with the list above:
# TODO: Understand commercial licensing requirements for resources used in this project
# TODO: Maybe use Faiss w/o GPU support and w/o Conda
# TODO: Analyze code with Pylint, Pydeps and mypy, radon or wily
# TODO: Understand the legal requirements for using the OpenAI API
# TODO: Optimizations
# TODO: Optimize text division
# TODO: Optimize Index type
# TODO: Optimize Similarity calculation type
# TODO: Optimize number of results returned
# TODO: Optimize method of assembling results into prompt
# TODO: Optimize prompt composition/characteristics/technique
# TODO: Optimize response validation
# TODO: Develop ways to evaluate and understand the semantic search performance
# TODO: Develop ways to understand the relative characteristics of the embeddings
# TODO: Include headings in the chunk text
# TODO: Page Numbers are not working. Would need to develop a new approach to parsing .docx files to get page numbers.
# TODO: Tune nlist and nprobe for Faiss index
# TODO: Add docstrings to the components
# TODO: Add Logging to the components
# TODO: Add unit tests to the components
# TODO: Backup of all Data
# TODO: Expose all behavioral parameters to the user: Model parameters, Tokenizer parameters, error checking, etc.
# TODO: Capture the questions the model had trouble answering and use them to improve the documentation
# TODO: Use a visual representation tool like Nomic to map queries against the user manual content to identify problem
#  areas
# TODO: Add a setup wizard that sets up the environment and configures the application
# TODO: Remove the OPENAI API KEY from the code and use a config file instead
# TODO: Semantic search review/maintenance interface
# TODO: Document Management interface
#  1. Add new documents
#  2. Remove documents
#  3. Backing up of data - Directory, primary/secondary backup versions
#  4. Restore previous state from backup
#  3. Progress bar for document upload, parsing/embedding, indexing
#  4. Control over number of neighbors returned and included in the prompt
#  5. Control over the prompt composition/characteristics/technique
#  6. Startup/Shutdown Chat

# TODO: Configuration
#   1. Model parameters: Model, temperature, top_p, n, stream, max_tokens, presence_penalty, frequency_penalty
#   2. Allow the admin user to choose the level of error checking
#   3. n_list, nprobe parameters for Faiss

# TODO: Chatbot Interface Features
#  1. Text entry box
#  2. Send button
#  3. Chat history window
#  4. Scroll the chat history window
#  1. Start new chat session - Drops chat history

# TODO: Features of Chatbot:
#  1. Control over chat session Start/Restart; End/Delete
#  2. History of Chat sessions
#  3. Responsive to the user's mood/emotional state
#  4. Ability to save/export the chat session to file and maybe email
#  5. Personalization of the chatbot based on the user's name, role, conference, etc.
#  6. Memory of previous conversations with User
#  7. Access to previous chat sessions
#  8. Chat session introduction
#       - Alert User that they are talking to an AI chatbot
#       - Alert User that the chatbot is trained on the User Manual
#       - Tell user how to reach a human
#  9. Alert User when the chatbot is not confident about the answer
#  10. Access to other means of communicating with humans for support
#  11. Ability to ask the User to provide feedback on individual answers
#  12. Ability to ask the User to provide feedback on the chatbot session as a whole
#  10. Scrolling chat window
#  18. Jump to the top/bottom of the chat window
#  11. Complex user input: Multiple sentences, paragraphs, carriage returns etc.
#  12. Paste into the chat session
#  11. Copy out of the chat window with visual indication of selected text
#  12. Visual differentiation of chatbot responses from User input
#  15. Give the user control over the size of the text in the chat window
#  16. Streaming chat w typing indicator
#  17. Answers should provide reference to the User Manual section/page number
#  18. View current Chat AI Context (the chat history provided as part of the prompt to the AI)

