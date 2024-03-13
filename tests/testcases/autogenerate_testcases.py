import random
from pathlib import Path
from lorem_text import lorem


def force_wordwrap(my_text: str, width: int = 80) -> str:
    """Force wordwrap text at a certain width"""
    words = my_text.split()
    lines = []
    line = []
    for word in words:
        if len(" ".join(line + [word])) <= width:
            line.append(word)
        else:
            lines.append(" ".join(line))
            line = [word]
    lines.append(" ".join(line))
    return "\n".join(lines)


def lorem_paragraphs_wrapped(
    num_paragraphs: int,
    width: int = 80,
    paragraph_sep: str = "\n\n",
    paragraph_prefix: str = "",
) -> str:
    """Generate lorem ipsum paragraphs and wordwrap them"""
    return paragraph_sep.join(
        [
            paragraph_prefix + force_wordwrap(lorem.paragraph(), width)
            for x in range(num_paragraphs)
        ]
    )


def case_01(table: str) -> str:
    num_paragraphs_before = random.randint(1, 3)
    num_paragraphs_after = random.randint(1, 3)
    paragraphs_before = lorem_paragraphs_wrapped(num_paragraphs_before)
    paragraphs_after = lorem_paragraphs_wrapped(num_paragraphs_after)
    return "\n\n".join([paragraphs_before, table, paragraphs_after])


def case_02(table: str) -> str:
    num_paragraphs_before = random.randint(1, 3)
    num_paragraphs_after = random.randint(1, 3)
    paragraphs_before = lorem_paragraphs_wrapped(
        num_paragraphs_before, paragraph_sep="\n", paragraph_prefix="    "
    )
    paragraphs_after = lorem_paragraphs_wrapped(
        num_paragraphs_after, paragraph_sep="\n", paragraph_prefix="    "
    )
    table = "".join([f"       {line}\n" for line in table.split("\n")])
    # remove the last newline
    table = table[:-1]
    return "\n".join([paragraphs_before, table, paragraphs_after])


def case_03(table: str) -> str:
    num_paragraphs_before = random.randint(1, 3)
    num_paragraphs_after = random.randint(1, 3)
    paragraphs_before = lorem_paragraphs_wrapped(
        num_paragraphs_before, paragraph_sep="\n", paragraph_prefix="\t"
    )
    paragraphs_after = lorem_paragraphs_wrapped(
        num_paragraphs_after, paragraph_sep="\n", paragraph_prefix="\t"
    )
    table = "".join([f"\t\t{line}\n" for line in table.split("\n")])
    # remove the last newline
    table = table[:-1]
    return "\n".join([paragraphs_before, table, paragraphs_after])


# Get a list of the template files,
# figure out first the path to the testcases directory
# and then glob the .txt files in the templates directory
testcases_dir = Path(__file__).parent
template_dir = testcases_dir / "templates"
table_template_files = list(template_dir.glob("*.txt"))

# initial round of testcase generation
for template_file in table_template_files:
    dest_folder = testcases_dir / template_file.stem.split("_")[0]
    dest_folder.mkdir(exist_ok=True)
    with open(template_file, "r") as f:
        table = f.read()
    testcase = case_01(table)
    testcase_file = dest_folder / f"simple01_{template_file.stem}.txt"
    with open(testcase_file, "w") as f:
        f.write(testcase)
    testcase = case_02(table)
    testcase_file = dest_folder / f"simple02_{template_file.stem}.txt"
    with open(testcase_file, "w") as f:
        f.write(testcase)
    testcase = case_03(table)
    testcase_file = dest_folder / f"simple03_{template_file.stem}.txt"
    with open(testcase_file, "w") as f:
        f.write(testcase)
