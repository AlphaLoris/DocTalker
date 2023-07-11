class LLM_Model:

    # Revised PromptChain class into (?) configuration settings for Model
    def __init__(self, properties):
        self.api_key = properties.get('api_key')
        self.llm_model = properties.get('llm_model')
        self.context_length = properties.get('context_length')
        self.user = properties.get('user')
        self.logit_bias = properties.get('logit_bias')
        self.temperature = properties.get('temperature')
        self.top_p = properties.get('top_p')
        self.max_tokens = properties.get('max_tokens')
        self.presence_penalty = properties.get('presence_penalty')
        self.frequency_penalty = properties.get('frequency_penalty')
        self.stream = properties.get('stream')
        self.n = properties.get('n')
        self.stop = properties.get('stop')
        self.model_list = properties.get('model_list')
        # self.prompts = []
        # self.edit_log = None
        # self.submission_log = None

    def set_model(self, llm_model):
        self.llm_model = llm_model

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_model_parameters(self, param_values):
        self.temperature = param_values.get('temperature')
        self.top_p = param_values.get('top_p')
        self.max_tokens = param_values.get('max_tokens')
        self.presence_penalty = param_values.get('presence_penalty')
        self.frequency_penalty = param_values.get('frequency_penalty')
        self.model_list = param_values.get('model_list')
        print("Model parameters set to: ", "temp: ", self.temperature, "   top_p: ", self.top_p, "   max_tokens: ",
              self.max_tokens, "   presence_penalty: ", self.presence_penalty, "   frequency_penalty: ",
              self.frequency_penalty)