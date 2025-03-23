import os

def save_text_to_file(text, filename_virtual):
    """
    Saves the given text to a file, creating directories if needed.
    """
    try:
        base_path = "D:\\Python\\AiAgents\\AutoGenPoc1"
        filename = os.path.join(base_path, filename_virtual)

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        print(filename) #Added this line
        with open(filename, 'w') as file:
            file.write(text)
        print(f"Text successfully saved to '{filename}'")
    except Exception as e:
        print(f"An error occurred: {e}")
