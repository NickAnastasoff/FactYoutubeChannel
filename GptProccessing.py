from gpt4allj import Model

model = Model(path to llm .bin file)
def promptGPTJ(prompt: str, max_tokens: int=50, temp: float=.7):
    """
    Generates text with GPT4All-j.

    args: 
        prompt: String. This is the starting text to be generated off of.

    returns:
        Generated result without prompt.
    """
    response = model.generate(prompt,
               seed=-1,
               n_threads=-1,
               n_predict=max_tokens,
               top_k=40,
               top_p=0.9,
               temp=temp,
               n_batch=8)
    return response