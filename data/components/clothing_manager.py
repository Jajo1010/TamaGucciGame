import json

class ClothingManager():
    def __init__(self, json_path):
        self.json_path = json_path
        self.load_data()

    def __str__(self) -> str:
        return f"Numbers of unlocked clothing : {self.clothing_info['unlocked_clothing_count']}, number of available clothing :  {self.clothing_info['clothing_count']}"

    def load_data(self):
        with open(self.json_path, 'r') as file:
            self.clothing_info = json.load(file)

    def save_data(self):
        with open(self.json_path, 'w') as file:
            json.dump(self.clothing_info, file, indent=4)

    def get_number_of_available_clothing(self) -> int :
        return self.clothing_info['clothing_count']
    
    def get_number_of_unlocked_clothing(self) -> int :
        return self.clothing_info['unlocked_clothing_count']
    
    def clothing_to_draw(self) -> str :
        active_clothing = self.clothing_info["active_clothing"]
        return active_clothing[str(max(map(int, active_clothing.keys())))]
    
    def add_clothing(self) -> None :
        if self.clothing_info['unlocked_clothing_count'] + 1 > self.clothing_info['clothing_count']:
            return
        self.clothing_info['unlocked_clothing_count'] += 1 
        index = str(self.clothing_info['unlocked_clothing_count'])
        if index in self.clothing_info['available_clothing'] and index not in self.clothing_info['active_clothing'] :
            self.clothing_info['active_clothing'][index] = self.clothing_info['available_clothing'][index]
        self.save_data()