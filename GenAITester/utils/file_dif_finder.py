import difflib

def compare_markdown_files(file1_path, file2_path):
    """
    Compares two markdown files and returns the differences.

    Args:
        file1_path (str): Path to the first markdown file.
        file2_path (str): Path to the second markdown file.

    Returns:
        str: A string containing the differences between the files, or None if an error occurs.
    """
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=file1_path, tofile=file2_path)
        return ''.join(diff)

    except FileNotFoundError:
        print("Error: One or both files not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# # Example usage:
# file1_path = 'D:\\Python\\AiAgents\\autogenpoccopy\\GenAITester\\documents\\FunctionalDocument.md'
# file2_path = 'D:\\Python\\AiAgents\\autogenpoccopy\\GenAITester\\documents\\FunctionalDocumentmodified.md'

# differences = compare_markdown_files(file1_path, file2_path)
