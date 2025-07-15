import os
import shutil
from functions import copy_directory_contents, generate_page, generate_pages_recursive

# Main function
def main():
    shutil.rmtree("public", ignore_errors=True)  # Clear the public directory
    os.makedirs("public", exist_ok=True)
    copy_directory_contents("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
