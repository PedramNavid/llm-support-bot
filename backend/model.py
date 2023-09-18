from llama_index.llms import LlamaCPP, OpenAI
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt

def llama_model():
    model_url = 'https://huggingface.co/TheBloke/CodeLlama-13B-Instruct-GGUF/resolve/main/codellama-13b-instruct.Q6_K.gguf'
    llm = LlamaCPP(
        model_url=model_url,
        temperature=0.1,
        max_new_tokens=2000,
        context_window=3900,
        generate_kwargs={},
        model_kwargs={"n_gpu_layers": -1},
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        verbose=False,
    )
    return llm

def openai_model(model):
    return OpenAI(model=model)
