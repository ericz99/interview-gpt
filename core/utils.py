from tiktoken import encoding_for_model

def get_only_content_token_length(messages, model):
    str = ""

    for message in messages:
        content = message['content']
        str += f'\n {content}'

    encoding = encoding_for_model(model)
    encoded = encoding.encode(str)
    return len(encoded)

def get_token_model_limit(model):
    if model is 'gpt-3.5-turbo':
        return 4_096
    elif model is 'gpt-3.5-turbo-0613':
        return 4_096
    elif model is 'gpt-4':
        return 8_192
    else:
        return -1