# Top 100 Movies

import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://www.empireonline.com/movies/features/best-movies-2/"
TEXT_FILE = "./movies.txt"


def load_site():
    response = requests.get(url=PAGE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    all_entries = soup.find_all(name="h3", class_="title")
    return all_entries


def sort_entries(entries):
    rank = 1
    output_text = ""
    for entry in entries[::-1]:
        line = entry.get_text()
        for i in range(1, 4):
            if line[i:i+2] == ": ":
                # split the string into separate characters
                char_list = list(line)
                # update the incorrect character
                char_list[i] = ")"
                # re-join into a string
                line = "".join(char_list)
        # try splitting and only using the title part
        try:
            title = line.split(') ')[1]
        # if not possible, e.g. there was no rank
        except IndexError:
            title = line
        # include the re-generated ranking
        output_text += f"{rank}) {title}\n"
        rank += 1
    return output_text


def save_file(text):
    # using the same encoding as the input, hard-coded to keep things simpler
    with open(file=TEXT_FILE, mode="w", encoding="ISO-8859-1") as f:
        f.write(text)


# read the site and sort the entries
sorted_list = sort_entries(load_site())
# save the text file... including it in the Github commit this time
save_file(sorted_list)
