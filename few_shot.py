import json
import pandas as pd
class FewShotPosts :
    def __init__(self,file_path="data\\processed_posts.json"):
        self.df = None #dataframe
        self.unique_tags = None #vairable for tags
        self.load_posts(file_path)

    def load_posts(self,file_path):
        with open(file_path , encoding = "utf-8") as f:
            posts = json.load(f) 
            df = pd.json_normalize(posts)#used to flatten nested JSON data into a tabular format (i.e., a Pandas DataFrame)
            df["length"] = df["line_count"].apply(self.categorize_length)#make a new coloumn of length in our data frame
            all_tags = df["tags"].apply(lambda x: x).sum()  #collect all tags into a single list.
            self.unique_tags = set(list(all_tags))  # convert pandas columns into list then set removes all the duplicates 
            self.df=df
    
    def categorize_length(self, line_count): #function to catogerise the length of the post 
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"
    def get_tags(self):
        return self.unique_tags
    
    def get_filtered_posts(self,length,language,tag):
        df_filtered=self.df[
            (self.df['language'] ==  language) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags: tag in tags))]
        return df_filtered.to_dict(orient="records")
if __name__== "__main__":
    fs = FewShotPosts()