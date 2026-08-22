import os
import glob
import re
import subprocess

try:
    import markdown
except ImportError:
    markdown = None


def render_markdown_to_html(md_text):
    """Converts raw Markdown text into styled HTML content."""
    if markdown:
        return markdown.markdown(
            md_text, extensions=["extra", "fenced_code", "tables"]
        )

    # Basic fallback converter if markdown library is missing
    lines = md_text.split("\n")
    html_lines = []
    in_list = False

    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("- ") or line.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line[2:]}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            # Bold conversion
            line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
            html_lines.append(f"<p>{line}</p>")

    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def build_site():
    """Converts all output/*.md files to output/*.html and creates output/index.html."""
    os.makedirs("output", exist_ok=True)
    md_files = glob.glob("output/*.md")

    articles = []

    for filepath in md_files:
        filename = os.path.basename(filepath)
        html_filename = filename.replace(".md", ".html")
        title = filename.replace(".md", "").replace("-", " ").title()

        with open(filepath, "r", encoding="utf-8") as f:
            md_content = f.read()

        body_html = render_markdown_to_html(md_content)

        full_page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.7; color: #222; background-color: #f9f9fb; }}
        .container {{ background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        a {{ color: #2563eb; text-decoration: none; font-weight: 600; }}
        a:hover {{ text-decoration: underline; }}
        h1, h2, h3 {{ color: #0f172a; margin-top: 1.5em; }}
        .nav-back {{ display: inline-block; margin-bottom: 20px; text-decoration: none; color: #64748b; font-size: 0.9rem; }}
        .cta-button {{ display: inline-block; background: #2563eb; color: #fff !important; padding: 12px 24px; border-radius: 6px; margin: 20px 0; text-decoration: none; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #e2e8f0; padding: 10px; text-align: left; }}
        th {{ background-color: #f1f5f9; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="nav-back">← Back to Articles</a>
        {body_html}
    </div>
</body>
</html>"""

        with open(
            os.path.join("output", html_filename), "w", encoding="utf-8"
        ) as f:
            f.write(full_page_html)

        articles.append((html_filename, title))

    # Generate Index Homepage
    links_html = "".join(
        [
            f'<li><a href="{href}">{t}</a></li>\n'
            for href, t in sorted(articles)
        ]
    )

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Revenue Agent - Latest Reviews</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; background-color: #f9f9fb; color: #1e293b; }}
        .container {{ background: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 12px 0; padding: 12px; border: 1px solid #e2e8f0; border-radius: 6px; transition: all 0.2s; }}
        li:hover {{ background-color: #f8fafc; border-color: #cbd5e1; }}
        a {{ color: #2563eb; text-decoration: none; font-size: 1.1rem; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Latest Product Reviews & Tech Guides</h1>
        <ul>
            {links_html}
        </ul>
    </div>
</body>
</html>"""

    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("📄 Built output/index.html and updated HTML article pages.")


def publish_to_amplify(filepath=None):
    try:
        build_site()
        print("🐙 Stage, commit, and push updates to GitHub...")
        subprocess.run(["git", "add", "output/"], check=True)
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "feat: generate HTML pages and index homepage",
            ],
            check=True,
        )
        subprocess.run(["git", "push"], check=True)
        print("🚀 Pushed to GitHub! AWS Amplify will publish the new layout.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git push failed or no changes to commit: {e}")
        return False


def publish_article(filepath=None):
    return publish_to_amplify(filepath)