import json
import os
from llama_cpp import Llama


def construct_info_print(model_info_dict):
    final_dict = dict()
    model_id = 0
    for model_name, model_info in model_info_dict.items():
        print(f'{model_id}: {model_name}')
        final_dict[model_id] = model_name
        model_id += 1
    return final_dict


def run_single_prompt(model_name, models_dir_, **kwargs):
    model_path_info = model_info.get(model_name)
    if model_path_info is None:
        raise KeyError(f'{model_name} does not have a model file')
    prompt = kwargs.get('prompt', 'What is a dark forest?')
    max_tokens = kwargs.get('max_tokens', 32)
    stop = kwargs.get('stop', ['Q:', '\n'])
    echo = kwargs.get('echo', True)

    publisher = model_path_info['publisher']
    path_name = model_path_info['path-name']
    file_name = model_path_info['file-name']
    file_path = os.path.join(models_dir_, publisher, path_name, file_name)
    llm = Llama(
        model_path=file_path,
    )
    output = llm(
        prompt,
        max_tokens=max_tokens,
        stop=stop,
        echo=echo
    )
    print(output)


if __name__ == '__main__':
    with open('configs.json', 'r') as f:
        configs = json.load(f)
    f.close()
    model_dir = configs['models_dir']
    model_info = configs['models']
   
    model_dict = construct_info_print(model_info)
    model_id = input('what is the model id of the model you want to try?')
    model_name = model_dict.get(int(model_id))
    if model_name is None:
        raise KeyError('the model id you selected is not available')
    run_single_prompt(model_name, model_dir)
