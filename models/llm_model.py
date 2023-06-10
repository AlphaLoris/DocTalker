class LLM_Model:

    # Revised PromptChain class into (?) configuration settings for Model
    def __init__(self):
        self.name = None
        self.api_key = None
        self.selected_model = None
        self.temperature = None
        self.top_p = None
        self.max_tokens = None
        self.presence_penalty = None
        self.frequency_penalty = None
        # self.prompts = []
        # self.edit_log = None
        # self.submission_log = None

    def set_model_name(self, model_name):
        self.selected_model = model_name

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_model_parameters(self, param_values):
        self.temperature = param_values.get('temperature')
        self.top_p = param_values.get('top_p')
        self.max_tokens = param_values.get('max_tokens')
        self.presence_penalty = param_values.get('presence_penalty')
        self.frequency_penalty = param_values.get('frequency_penalty')
        print("Model parameters set to: ", "temp: ", self.temperature, "   top_p: ", self.top_p, "   max_tokens: ",
              self.max_tokens, "   presence_penalty: ", self.presence_penalty, "   frequency_penalty: ",
              self.frequency_penalty)