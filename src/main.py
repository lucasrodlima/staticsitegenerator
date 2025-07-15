from functions import copy_directory_contents, generate_page

# Main function
def main():
    copy_directory_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
