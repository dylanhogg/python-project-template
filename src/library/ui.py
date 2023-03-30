from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from loguru import logger


def print_table(message: str, headers_list: list, split_token: str) -> str:
    # See: https://rich.readthedocs.io/en/stable/tables.html
    logger.info(f"{message=}")

    lines = message.splitlines()
    lines = [line for line in lines if len(line.split(split_token)) >= len(headers_list)]

    expected_cols = len(headers_list)
    try:
        headers = lines[0].split(split_token)  # TODO: use headers_list instead of lines[0], but do replace
        if len(headers) != expected_cols:
            logger.error(f"Error in print_table with {headers=}, {expected_cols=} != {len(headers)=}, {message=}")
            print(message)
            return message

        table = Table(show_header=True, header_style="bold blue")

        for header in headers:
            table.add_column(header.strip())
        for row in lines[1:]:
            cols = row.split(split_token)
            # if len(cols) != expected_cols:
            #     print(f"Skipping row '{row}' because {len(cols)=} != {expected_cols=}")
            #     continue
            # table.add_row(*cols)

            # HACK:
            # logger.info(f"{cols=}")
            col1 = cols[0].strip()
            col2 = split_token.join(cols[1:-1]).strip()
            col3 = cols[-1].strip()
            table.add_row(col1, col2, col3)

        console = Console()
        print("print_table:")
        console.print(table)

        return message  # TODO: return formatted table output!

    except Exception as ex:
        logger.error(f"Error in print_table with {message=}: {ex}")
        print(message)


def print_markdown(markdown: str) -> str:
    # See: https://rich.readthedocs.io/en/stable/markdown.html
    logger.info(f"{markdown=}")

    try:
        console = Console()
        md = Markdown(markdown)
        print("print_markdown:")
        console.print(md)
    except Exception as ex:
        logger.error(f"Error in print_markdown with {markdown=}: {ex}")
        print(markdown)

    return markdown
