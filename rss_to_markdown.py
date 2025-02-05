import feedparser
import os
from datetime import datetime

# RSS feed URL
rss_url = "https://www.reddit.com/r/InternetDrama/new/.rss"

# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Debugging: Print feed status
if feed.bozo:
    print("Error fetching the RSS feed.")
    exit()

print(f"Found {len(feed.entries)} entries in the RSS feed.")

# Ensure the content/posts directory exists
output_dir = "content/posts"
os.makedirs(output_dir, exist_ok=True)

def sanitize_filename(title):
    """Sanitize title for use in a valid filename."""
    return title.lower().replace(' ', '-').replace('/', '').replace('"', '').replace('?', '').replace('<', '').replace('>', '')

def write_frontmatter(filename, title, date, content, link):
    """Write the frontmatter and content to the markdown file."""
    try:
        with open(filename, "w") as f:
            f.write(f"---\n")
            f.write(f"title: \"{title}\"\n")  # Ensure escaping special characters in title
            f.write(f"date: {date}\n")
            f.write(f"summary: \"{content[:100]}...\"\n")  # Optional: add a summary for the post
            f.write(f"tags: [\"drama\", \"internet\", \"reddit\"]\n")  # Optional: add default tags
            f.write(f"categories: [\"InternetDrama\"]\n")  # Optional: set categories
            f.write(f"draft: false\n")
            f.write(f"---\n")
            f.write(f"{content}\n")
            f.write(f"[Read more]({link})\n")
        print(f"Created: {filename}")
    except Exception as e:
        print(f"Error writing file {filename}: {e}")

# Create or update Markdown files for each entry
for entry in feed.entries:
    title = entry.title
    link = entry.link
    date = datetime.now().strftime("%Y-%m-%d")
    content = entry.summary if "summary" in entry else ""

    # Generate a safe filename
    filename = f"{output_dir}/{date}-{sanitize_filename(title)}.md"

    # Check if the file already exists (for updates)
    if os.path.exists(filename):
        print(f"Updating existing file: {filename}")
    else:
        print(f"Creating new file: {filename}")

    # Write the frontmatter and content
    write_frontmatter(filename, title, date, content, link)

