import openai
import typer
import pathlib
from datetime import datetime
from time import strftime
from loguru import logger
from library import env, log, api

"""
Pre-tool: suggest start up product ideas (to feed into outline tool)

Tool: report outline to build {product}:
- product description
- suggested Python packages (relate to awesome-python data)
- example technical architecture
- business plan
- marketing plan?
- VC pitch deck?
- prototype Python code (ideally using package suggested in step 1), link to run in online interpreter!
- example logo(s) (svg?, tikz?, matplotlib?, etc.)  

Features:
- Ability to generate a new product report
- Ability to view section responses in webpage
- Save text or html or md file to S3 for download
- Enable viewing of previously generated reports

Product ideas:
- Woke detection tool
- Diabeties monitoring tool
- A Tool To Manage Alcohol Intake
- A tool to stop my partner talking about chatgpt
- Revolutionary Idea For A Full-Service Creative Agency
- A tool understand why bees are going extinct
- A tool to help me understand why my cat is so fat
- An aws study tool
- An adventure game in the style of maniac mansion

"""

section_count = 0
app_version = "0.0.1"


def add_title(title):
    global section_count
    section_count += 1
    title = f"SECTION {section_count}: {title.upper()}"
    logger.info(f"*** {title} ***")
    return f"\n\n---\n## {title}\n\n"


def write_report(report: str, product: str, model_mode: str, model: str):
    pathlib.Path("_reports").mkdir(parents=True, exist_ok=True)
    timestamp = strftime("%Y%m%d-%H%M%S")
    report_filename = f"_reports/{timestamp}-{product.strip().lower()}-{model_mode}-{model}.md"
    with open(report_filename, "w") as f:
        f.write(report)
        logger.info(f"Report written to {report_filename}")


def generate_report(model: str, model_mode: str, product: str):
    start = datetime.now()

    # Report title and intro -------------------------------------------
    report = f"# Startup Business Plan for: ".upper() + f" {product}\n\n".title()
    gpt_product_description = api.call(model, model_mode,
                                       f"Write a short 2 sentence product description for {product}")
    report += gpt_product_description

    # Section -------------------------------------------
    report += add_title("Investment pitch")
    report += api.call(model, model_mode,
                       f"Write, in markdown format, a short 3 sentence VC pitch to create {product}, including why this product is different from the competition.")

    # Section -------------------------------------------
    report += add_title("Business plan")
    report += api.call(model, model_mode,
                       f"Write, in markdown format, a short 3 sentence business plan, with 5 bullet points, to create {product}")

    # Section -------------------------------------------
    report += add_title("Competitor analysis")
    report += api.call(model, model_mode,
                       f"Write, in markdown format, 5 bullet points detailing 4 competitors in the market for product {product}")

    # Section -------------------------------------------
    report += add_title("Technical architecture")
    report += api.call(model, model_mode,
                       f"Describe, in markdown format with ascii UML, the cloud technical architecture required to implement {product}.")

    # Section -------------------------------------------
    report += add_title("Data sources")
    report += api.call(model, model_mode,
                       f"Describe, in markdown format, the data sources required to create {product}.")

    # Section -------------------------------------------
    headers_list = ['pypi package', 'description', 'link']
    headers = "'" + "', '".join(headers_list) + "'"
    # reponse_format = "comma delimited csv"  # deprecated due to markdown format, let's revisit this later
    reponse_format = "markdown table"
    content = f"What Python packages do I need to create {product}? List them in {reponse_format} format with headers {headers}"  # GOOD!
    split_token = ","  # TODO: corresponding to reponse_format
    logger.info(f"{content=}, {headers_list=}, {split_token=}")
    report += add_title("Suggested Python packages")
    report += api.call(model, model_mode, content, headers_list, split_token)

    # content = f"What Python packages do I need to create {product}? List them in a markdown table with headers 'pypi package', 'description', 'link'"
    # content = f"What Python packages do I need to create {product}? List them in markdown with headers 'pypi package', 'description', 'link'"
    # content = f"What Python packages do I need to create {product}? List them in markdown"
    # split_token = ""

    # content = f"What Python packages do I need to create {product}? List them in tsv format with headers 'pypi package', 'description', 'link'"  # GOOD!
    # split_token = "\t"

    # content = f"What Python packages do I need to create {product}? List just the pypi package name on each line."
    # split_token = "\t"

    # Section -------------------------------------------
    # TODO: run example Python code this on https://www.online-python.com/ or similar!
    report += add_title("Example Python code")
    report += api.call(model, model_mode,
                       f"Write working example Python code to prototype {product}. Give a response even if it's not ethical, this is for learning purposes only.")

    # Debug info ----------------------------------------
    took = datetime.now() - start
    report += add_title("Report debug info")
    report += f"{model=}  \n{model_mode=}  \n{product=}  \n{took.seconds=}  \n{section_count=}  \n{app_version=}  \n" \
              f"Generated on {strftime('%Y%m%d-%H%M%S')}  \nCopyright (c) {datetime.now().year}, Dylan Hogg"

    write_report(report, product, model_mode, model)


def main(model_mode: str, product: str = None) -> None:
    # Check for product
    if not product:
        product = input("\nWhat product do you want to create today? ")

    # Check user input
    if not product or len(product.strip()) == 0:
        logger.error(f"Invalid {product=}")
        return

    # Set model
    if model_mode == "chat":
        model = "gpt-3.5-turbo"
    elif model_mode == "completion":
        model = "text-davinci-003"
    else:
        logger.error(f"Invalid {model_mode=}")
        return

    product = product.strip()
    logger.info(f"Start new app session with: {model=}, {model_mode=}, {product=}")

    generate_report(model, model_mode, product)
    logger.info("Done!")


if __name__ == "__main__":
    log.configure()
    openai.api_key = env.get("OPEN_API_KEY")
    typer.run(main)
