from .html import generate_page, copy_static, generate_pages_recursive

def main():
    copy_static()
    generate_pages_recursive("./content", "./template.html", "./public")
    # generate_page("./content/index.md", "./template.html", "./public/index.html")
main()