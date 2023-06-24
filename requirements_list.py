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
#    - Allow the admin user to choose the level of error checking
#    - n_list, nprobe parameters for Faiss
#
# TODO: Database
#
# TODO: Document Management
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
#    - Figure out a way to leverage the chunk size and overlap controls and maybe the splitting methodology of this
#         script along with text_block_extractor.py to get the best of both worlds
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
#
# TODO: Individual Chat session Interface Features
#    - Chat session introduction
#         - Alert User that they are talking to an AI chatbot
#         - Alert User that the chatbot is trained on the User Manual
#         - Tell user how to reach a human
#         - Assign each chat session a unique ID and use it in API calls
#         - Get user email address at the start of each chat session
#         - Access to other means of communicating with humans for support
#    - Terminating the chat session
#         - May want to handle this like an onion so that the user launches the session, then launches it again so they
#              know they can rate the session after it ends before they start
#    - Chat sessions history window
#         - Memory of previous conversations with User
#         - Delete Chat session history
#         - Access to previous chat sessions (view/continue/search)
#         - Ability to save/export the chat session to file and maybe email
#         - Ability to ask the User to provide feedback on the chatbot session as a whole
#    - Chat Session
#         - Chat window
#              - Complex user input: Multiple sentences, paragraphs, carriage returns etc.
#              - Scrollable Window
#              - Expandable Window
#              - Paste into the chat window
#              - Select text in chat window
#              - Cut selected text from chat window
#              - Copy selected text from chat window
#              - Visual differentiation of chatbot responses from User input
#              - User control over the size of the text in the chat window
#              - Streaming chat w typing indicator
#         - Chat history window
#              - Scroll the chat history window
#              - Alert User when the chatbot is not confident about the answer
#              - Ability to ask the User to provide feedback on individual answers
#              - Answers should provide reference to the User Manual section/page number
#         - Submit button
#         - End chat button
#         - Jump to the top/bottom of the chat window
#         - Restart chat button
#              - Discard session memory
#              - Empty Chat session window
#         - Access to other means of communicating with humans for support


