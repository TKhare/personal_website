#!/usr/bin/env python3
import sys
import os
from datetime import datetime

INDEX_PATH = os.path.join(os.path.dirname(__file__), "index.html")

def main():
    if len(sys.argv) != 2:
        print("Usage: python add_note.py MM-DD-YYYY.html")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith(".html"):
        print("Error: filename must end with .html")
        sys.exit(1)

    date_str = filename.replace(".html", "")
    # Validate date format
    try:
        date_obj = datetime.strptime(date_str, "%m-%d-%Y")
    except ValueError:
        print("Error: date must be in MM-DD-YYYY format")
        sys.exit(1)

    # Read the existing index.html
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the UL start and end
    start_tag = "<ul>"
    end_tag = "</ul>"
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag, start_idx)
    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find <ul> block in index.html")
        sys.exit(1)

    # Extract existing links
    ul_block = content[start_idx + len(start_tag):end_idx].strip()
    links = []
    for line in ul_block.splitlines():
        line = line.strip()
        if line.startswith("<li><a"):
            # Extract the date from the href
            href_part = line.split('href="')[1].split('"')[0]
            date_part = os.path.basename(href_part).replace(".html", "")
            links.append(date_part)

    if date_str in links:
        print(f"Link for {date_str} already exists.")
        return

    # Add new date and sort descending
    links.append(date_str)
    links.sort(key=lambda d: datetime.strptime(d, "%m-%d-%Y"), reverse=True)

    # Rebuild UL content
    new_ul = "\n".join([f'      <li><a href="/journal/{d}.html">{d}</a></li>' for d in links])

    # Replace old UL block
    new_content = (
        content[:start_idx + len(start_tag)]
        + "\n" + new_ul + "\n"
        + content[end_idx:]
    )

    # Write back
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Added link for {filename} to journal/index.html")

if __name__ == "__main__":
    main()
