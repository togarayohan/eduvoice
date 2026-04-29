from unsloth import FastLanguageModel
import torch

# 1. Load the Base Model + Your Fine-Tuned Adapters
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "google/gemma-4-E4b-it", # The original base model
    model_adapter_file = "eduvoice_lora_final", # Path to your unzipped folder
    load_in_4bit = True, 
)

# 2. Export to GGUF for Ollama
# This performs the heavy mathematical merge and quantization
model.save_pretrained_gguf(
    "eduvoice_gguf_model", 
    tokenizer, 
    quantization_method = "q4_k_m" # Optimal for Mac/Pi performance
)
print("Merge complete! Your Ollama-ready file is in the 'eduvoice_gguf_model' folder.")