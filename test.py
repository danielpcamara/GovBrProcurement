# from Scraping import *

# cw = crawlers.CrawlerMaster(1, 'cmpg.oxy.elotech.com.br', 4119905, 'Ponta Grossa/PR')
# cw.do_ocr(2)
import torch
from transformers import AutoTokenizer,AutoModelForPreTraining, AutoModel

model = AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased')
tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=False)
input_ids = tokenizer.encode('Tinha uma pedra no meio do caminho.', return_tensors='pt')

with torch.no_grad():
    outs = model(input_ids)
    encoded = outs[0][0, 1:-1]

last_hidden_states = outs[0]

# Print the output features
print(last_hidden_states)