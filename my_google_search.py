import json

class MyGoogleSearch:
    def __init__(self):
        self.data_file = "data.json"
        self.data = None

    def load_data(self):
        with open(self.data_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def upload_file(self, path_to_new_data):
        try:
            with open(path_to_new_data, "r") as f:
                new_data = json.load(f)
                if isinstance(new_data, list):
                    with open(self.data_file, "a") as f:
                        for item in new_data:
                            json.dump(item, f)
                elif isinstance(new_data, dict):
                    with open(self.data_file, "a") as f:
                        json.dump(new_data, f)
                else:
                    raise Exception("Invalid data format")
            return  "File uploaded successfully"
        except:
            return "Path not located"

    def remove_file(self, title):
        title = title.replace("\n", "")
        data_to_remove = next((x for x in self.data if (x["title"] and (x["title"].replace("\n", "") == title))), None)
        if not data_to_remove:
            return "File not found"
        else:
            self.data.remove(data_to_remove)
            with open(self.data_file, "w") as f:
                json.dump(self.data, f)
            return "File removed successfully"        

    def list_files(self):
        if not self.data:
            self.load_data()
        return [x["title"] for x in self.data]

    def search(self, search_query: str):
        if not self.data:
            self.load_data()
        
        search_query = set(search_query.lower().split())
        relevant_files = []

        for item in self.data:
            content = item.get("maintext", "").lower() if item.get("maintext") is not None else ""
            content_words = set(content.split())
            if search_query.issubset(content_words):
                relevant_files.append(item)

        total_files = len(relevant_files)
        if total_files >= 10:
            relevant_files = relevant_files[:10]
        
        response = f"{total_files} files were found\n" if total_files != 1 else f"{total_files} file was found\n"
        if relevant_files:
            response += '\n'.join([f"{i+1}. {file['title']}" for i, file in enumerate(relevant_files)])
        
        return response