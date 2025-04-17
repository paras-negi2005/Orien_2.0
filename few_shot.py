import json
import pandas as pd
import os  # To handle cross-platform file paths

class FewShotPosts:
    # Constructor that takes the file path to load posts from
    def __init__(self, file_path=None):
        self.df = None  # DataFrame to store posts
        self.unique_tags = None  # To store unique tags from the posts
        
        # If no file path is provided, use the default one
        if file_path is None:
            file_path = os.path.join("data", "processed_posts.json")
        
        self.load_posts(file_path)  # Load posts from the given file path

    # Method to load posts from a JSON file
    def load_posts(self, file_path):
        try:
            # Try opening the file and reading JSON content
            with open(file_path, encoding="utf-8") as f:
                posts = json.load(f)  # Load the posts from the JSON file
                
                # Normalize JSON to a Pandas DataFrame (flatten nested JSON data)
                df = pd.json_normalize(posts)
                
                # Add a new column "length" based on line_count and categorize it
                df["length"] = df["line_count"].apply(self.categorize_length)
                
                # Extract all tags into a single list and remove duplicates
                all_tags = df["tags"].apply(lambda x: x).sum()  # Flatten the tags
                self.unique_tags = set(list(all_tags))  # Remove duplicates by converting to set
                
                # Store the DataFrame in the class
                self.df = df
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found. Please check the path.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from '{file_path}'. Please check the file format.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # Method to categorize posts based on their line count
    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"
    
    # Method to get the unique tags
    def get_tags(self):
        return self.unique_tags
    
    # Method to get filtered posts based on specific criteria (length, language, tag)
    def get_filtered_posts(self, length, language, tag):
        # Filter the DataFrame based on the conditions provided
        df_filtered = self.df[
            (self.df['language'] == language) &  # Filter by language
            (self.df['length'] == length) &  # Filter by length category
            (self.df['tags'].apply(lambda tags: tag in tags))  # Filter by tag
        ]
        
        # Return the filtered posts as a list of dictionaries
        return df_filtered.to_dict(orient="records")

# Main block to run the script
if __name__ == "__main__":
    # Create an instance of FewShotPosts with the default file path
    fs = FewShotPosts()

    # Example: Get filtered posts for language "Python", length "Medium", and tag "AI"
    filtered_posts = fs.get_filtered_posts(length="Medium", language="Python", tag="AI")
    
    # Print the filtered posts
    print(filtered_posts)
