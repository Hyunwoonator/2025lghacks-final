from typing import Any
import httpx
import os
from mcp.server.fastmcp import FastMCP
import shutil
from pathlib import Path
import time
# Initialize FastMCP server
mcp = FastMCP("clarus")

#generate a function that allows claude to read the file metadata
@mcp.tool()
async def get_file_metadata(file: str):
    """Get the metadata for a file.
    
    Args:
        file: File to get the metadata for
    """
    file_stats = os.stat(file)
    return f"Size: {file_stats.st_size} bytes\nCreated: {time.ctime(file_stats.st_ctime)}\nLast modified: {time.ctime(file_stats.st_mtime)}\nLast accessed: {time.ctime(file_stats.st_atime)}"


#generate a function that sorts files in a directory by file type
@mcp.tool()
async def sort_files_into_filetypes(directory: str):
    """
    Organize files in the specified directory into subfolders based on their file extensions.
    
    Args:
        directory (str): The directory path containing files to organize
    """
    # Convert to absolute path and ensure directory exists
    directory = os.path.abspath(directory)
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    # Get all files in the directory (non-recursive)
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Track what we've processed
    processed_count = 0
    skipped_count = 0
    
    # Create folders and move files
    for file in files:
        # Skip hidden files (starting with .)
        if file.startswith('.'):
            skipped_count += 1
            continue
        
        file_path = os.path.join(directory, file)
        
        # Get the file extension (lowercase)
        _, extension = os.path.splitext(file)
        extension = extension[1:].lower()  # Remove the dot and convert to lowercase
        
        # If no extension, use "no_extension" as the folder name
        if not extension:
            folder_name = "no_extension"
        else:
            folder_name = extension
        
        # Create the target folder if it doesn't exist
        target_folder = os.path.join(directory, folder_name)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        
        # Move the file
        target_path = os.path.join(target_folder, file)
        try:
            shutil.move(file_path, target_path)
            processed_count += 1
            print(f"Moved: {file} → {folder_name}/")
        except Exception as e:
            print(f"Error moving {file}: {str(e)}")
            skipped_count += 1
    
    if skipped_count > 0:
        print(f"Skipped {skipped_count} files.")

#generate a function that allows claude to get the given file name
@mcp.tool()
async def get_file_name(file: str):
    """Get the given file name.
    
    Args:
        file: File to get the name of
    """
    return file
#generate a function that allows claude to move files
@mcp.tool()
async def move_file(file: str, destination: str):
    """Move a file to a destination.
    
    Args:
        file: File to move
        destination: Destination to move the file to
    """
    shutil.move(file, destination)
    return "File moved successfully."

#generate a function that allows claude to make folders
@mcp.tool()
async def make_folder(folder: str):
    """Make a folder.
    
    Args:
        folder: Folder to make
    """
    os.makedirs(folder)
    return "Folder made successfully."

#generate a function that allows claude to access a file
@mcp.tool()
async def access_file(file: str):
    """Access a file.
    
    Args:
        file: File to access
    """
    with open(file, "r") as f:
        return f.read()

#generate a function that allows claude to access a directory
@mcp.tool()
async def access_directory(directory: str):
    """Access a directory.
    
    Args:
        directory: Directory to access
    """
    return os.listdir(directory)

#generate a function that allows claude to change the file name
@mcp.tool()
async def change_file_name(file: str, new_name: str, directory: str):
    """Change the name of a file.
    
    Args:
        file: File to change the name of
        new_name: New name for the file
    """
    os.rename(directory + "/" + file, directory + "/" + new_name)
    return "File name changed successfully."

#generate a function that allows claude to delete a file
@mcp.tool()
async def delete_file(file: str, directory: str):
    """Delete a file.
    
    Args:
        file: File to delete
    """
    os.remove(directory + "/" + file)
    return "File deleted successfully."

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')


