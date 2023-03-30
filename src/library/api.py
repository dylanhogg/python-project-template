import openai
from loguru import logger
from library import env, log, ui


def _completion_model(content: str, model: str):
    # /v1/completions
    # text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001, davinci, curie, babbage, ada

    # Generate a response
    completion = openai.Completion.create(
        engine=model,
        prompt=content,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response


def _chat_model(content: str, model: str):
    # /v1/chat/completions
    # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
    messages = [
        {"role": "system", "content": "You are an helpful expert developer."},
        {"role": "user", "content": content}
    ]
    chat = openai.ChatCompletion.create(model=model, messages=messages)
    # type(chat) = openai.openai_object.OpenAIObject
    return chat


def reduced_markdown_headings(markdown):
    return markdown \
        .replace("###### ", "##### ") \
        .replace("##### ", "#### ") \
        .replace("#### ", "### ") \
        .replace("### ", "#### ") \
        .replace("## ", "### ") \
        .replace("# ", "## ")


def call(model: str, model_mode: str, content: str, headers_list: list = None, split_token: str = None) -> str:
    # https://platform.openai.com/docs/models/gpt-3-5
    # https://platform.openai.com/docs/model-index-for-researchers

    if model_mode.lower() == "chat":
        response = _chat_model(content, model)
        response = response.choices[0].message.content
        logger.info(response)
        if "markdown" in content:
            reduced_heading_response = reduced_markdown_headings(response)
            return ui.print_markdown(reduced_heading_response)
        elif "csv" in content:
            logger.warning("console only, deprecated")
            return ui.print_table(response, headers_list, split_token)
        else:
            return response.replace("\n", "\n  ")

            # elif model_mode.lower() == "completion":
    #     # TODO: not tested well...
    #     model = "text-davinci-003"
    #     logger.debug(f"{model=}")
    #     response = _completion_model(content, model)
    #     # logger.info(type(response))
    #     logger.debug(response)
    #     print(response + "\n")
    #     # print(response)

    else:
        logger.error(f"Unknown {model_mode=}")
        raise NotImplementedError(f"Unknown {model_mode=}")
