
#  C:\Users\glenn\anaconda3\envs\doc_talker_faiss

# Layer 1: Data Ingestion Layer (Layered Architecture and Strategy Patterns)
class DataIngestion:
    def __init__(self, docx_converter_strategy, text_chunker_strategy, embedding_generator_strategy):
        self.docx_converter = docx_converter_strategy
        self.text_chunker = text_chunker_strategy
        self.embedding_generator = embedding_generator_strategy

    def process_docx_files(self, docx_files):
        for docx_file in docx_files:
            text_data = self.docx_converter.convert_docx_to_text(docx_file)
            chunks = self.text_chunker.chunk_text(text_data)
            for chunk in chunks:
                embedding = self.embedding_generator.generate_embedding(chunk)
                QdrantDBAdapter().persist(chunk)

        SearchIndex.get_instance().create_index()


# Layer 2: Storage Layer (Adapter and Singleton Patterns)
class QdrantDBAdapter:
    _instance = None

    @staticmethod
    def get_instance():
        if QdrantDBAdapter._instance is None:
            QdrantDBAdapter._instance = QdrantDBAdapter()
        return QdrantDBAdapter._instance

    def persist(self, embedding, metadata):
        # Persist embedding and metadata in QdrantDB
        pass


# Layer 3: Semantic Search Layer (Singleton Pattern)
class SearchIndex:
    _instance = None

    @staticmethod
    def get_instance():
        if SearchIndex._instance is None:
            SearchIndex._instance = SearchIndex()
        return SearchIndex._instance

    def create_index(self):
        # Create index of embeddings
        pass

    def search(self, user_input):
        # Perform semantic search on the embeddings in the database
        return search_results


# Layer 4: Presentation Layer (MVC and Observer Patterns)
class ChatbotView:
    def display(self, response):
        # Display chatbot response
        pass

    def get_user_input(self):
        # Get user input
        return user_input


class ChatbotModel:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, user_input):
        for observer in self.observers:
            observer.update(user_input)


class ChatbotController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.register_observer(self)

    def update(self, user_input):
        search_results = SearchIndex.get_instance().search(user_input)
        response = self.generate_response(search_results)
        self.view.display(response)

    def generate_response(self, search_results):
        # Return relevant content to the user based on the search results
        return response


def main():
    # Initialize the application and set up the chatbot
    view = ChatbotView()
    model = ChatbotModel()
    controller = ChatbotController(model, view)

    # Check if data is available
    docx_files = get_docx_files() # Attempt to identify the index
    if docx_files:
        ingestion = DataIngestion(DOCXConverter(), TextChunker(), EmbeddingGenerator())
        ingestion.process_docx_files(docx_files)

    # Chat loop
    while True:
        user_input = view.get_user_input()
        model.notify_observers(user_input)


if __name__ == "__main__":
    main()
