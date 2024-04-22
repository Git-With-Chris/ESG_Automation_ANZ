# Save this code in a separate file, e.g., config.py
from streamlit import config
from transformers import AutoTokenizer, T5EncoderModel

# Set maximum upload size to 100 MB
config.set_option('server.maxUploadSize', 100)
tokenizer = AutoTokenizer.from_pretrained("t5-large", suppress_warnings=True)
model = T5EncoderModel.from_pretrained("t5-large")