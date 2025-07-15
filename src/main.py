import os
import shutil
from functions import copy_directory_contents, generate_page

# Main function
def main():
    shutil.rmtree("public", ignore_errors=True)  # Clear the public directory
    os.makedirs("public", exist_ok=True)
    copy_directory_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
