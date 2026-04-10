import re

class InputClassifier:
    def __init__(self):
        self.url_pattern = re.compile(r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$', re.IGNORECASE)

    def predict_logic(self, user_input, model_handler):
        clean_input = str(user_input).strip()
        
        if self.url_pattern.match(clean_input):
            return "Fake News Detection", model_handler.predict_newspaper(clean_input)
            
        mal_keys = ['eval(', 'exec(', 'base64', 'system(', '<script>']
        if any(k in clean_input.lower() for k in mal_keys):
            return "Malware Analysis", model_handler.predict_malware_text(clean_input)

        return "Spam Filter", model_handler.predict_spam(clean_input)

input_router = InputClassifier()