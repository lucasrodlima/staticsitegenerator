import os
import shutil
import sys
from functions import copy_directory_contents, generate_pages_recursive


# Main function
def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    shutil.rmtree("docs", ignore_errors=True)  # Clear the public directory
    os.makedirs("docs", exist_ok=True)
    copy_directory_contents("static", f"docs{basepath}")
    generate_pages_recursive("content", "template.html", f"docs{basepath}", basepath)


if __name__ == "__main__":
    main()
