from tiktoken import encoding_for_model, get_encoding
import os
from pdfminer.high_level import extract_text


def get_only_content_token_length(messages, model):
    str = ""

    for message in messages:
        content = message.content
        str += f"\n {content}"

    encoding = encoding_for_model(model)
    encoded = encoding.encode(str)
    return len(encoded)


def get_token_model_limit(model):
    if model == "gpt-3.5-turbo":
        return 4_096
    elif model == "gpt-3.5-turbo-0613":
        return 4_096
    elif model == "gpt-3.5-turbo-1106":
        return 4_096
    elif model == "gpt-4":
        return 8_192
    else:
        return -1


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def text_to_chuck(text, size=1000):
    chucks = []

    for t in text:
        encoding = encoding_for_model("text-embedding-ada-002")
        token_encoded = encoding.encode(t)
        current_token_size = len(token_encoded)

        start = 0
        remaining = current_token_size

        while start < remaining:
            split_encoded = token_encoded[start : start + size - 1]
            decoded = encoding.decode(split_encoded)

            # add to chucks
            chucks.append(decoded)
            start += size - 1
            remaining = current_token_size - size - 1

        if remaining > 0:
            split_encoded = token_encoded[start : start + size - 1]
            decoded = encoding.decode(split_encoded)

            # add to chucks
            chucks.append(decoded)

    return chucks


def extract_text_from_pdf(path):
    if not os.path.exists(path):
        raise Exception("Path not found.")

    with open(path, "rb") as file:
        # todo: if resume or document is more than one page, need to split into multiple pdf using pypdf2 instead
        _text = extract_text(file)
        return _text
