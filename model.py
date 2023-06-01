from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


torch_dtype = torch.bfloat16
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model_name = "bigscience/bloomz-1b7"



tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto").to(device=device)


def run(text,**kargs):
    inputs = tokenizer.encode(text=text, return_tensors="pt").to(device=device)
    outputs = model.generate(inputs,**kargs)
    return tokenizer.decode(outputs[0])



if __name__ == "__main__":
    print("model test")
    model("This is the input text.")