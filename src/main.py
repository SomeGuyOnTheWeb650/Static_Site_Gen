

import os
import shutil
import logging
from extraction_function import extract_title, generate_page
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(filename="logging.log", encoding="utf-8", level=logging.DEBUG)
if len(sys.argv) == 1:
    basepath = "/"
else:
    
    basepath = sys.argv[1]

def main():
    destination_directory = "./docs/"
    source_directory = "./static/"
    if not os.path.exists(source_directory):
        logging.error("source doesn't exist")
        raise Exception("source doesn't exist")
    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)
        logging.info(f"created {destination_directory}")
    list_of_items_in_destination = os.listdir(destination_directory)
    for item in list_of_items_in_destination:
        path = os.path.join(destination_directory, item)
        if os.path.isfile(path):
            os.remove(path)
            logging.info(f"removed {path} file")
        if os.path.isdir(path):
            shutil.rmtree(path)
            logging.info(f"removed {path} dir")
    # Should be a clean public env now
    def helper(source=source_directory, destination=destination_directory):
        list_of_items_in_source = os.listdir(source)
        for item in list_of_items_in_source:
            path = os.path.join(source, item)
            if os.path.isfile(path):
                dst = os.path.join(destination, item)
                shutil.copy(path, dst)
                logging.info(f"copied {path} to {dst}")
            elif os.path.isdir(path):
                dst = os.path.join(destination, item)
                os.mkdir(dst)
                logging.info(f"created dir: {dst}")
                helper(path, dst)
    helper()

    def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
        items = os.listdir(dir_path_content)
        
        for item in items:
            
            path = os.path.join(dir_path_content, item)
            if os.path.isfile(path) and item == "index.md":
                clean = os.path.relpath(path, "./content")
                
                dst_path = os.path.join(dest_dir_path, clean)
                dst_path = dst_path.replace(".md", ".html")
                
                generate_page(path, template_path, dst_path, basepath)
            elif os.path.isdir(path):
                generate_pages_recursive(path, template_path, dest_dir_path, basepath)
                
        

    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

main()