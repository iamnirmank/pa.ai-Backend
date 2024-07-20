from transformers import AutoTokenizer, AutoModelForCausalLM

# Initialize the model and tokenizer
def init_llama_model():
    model_name = "meta-llama/Meta-Llama-3-70B" 
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = init_llama_model()

def generate_response_with_llama(input_text):
    """Generate a response using the Llama-3 model."""
    # Tokenize input
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate response
    outputs = model.generate(
        inputs["input_ids"],
        max_length=150,  # Adjust as needed
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    # Decode the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
