import json

class ClothingManager():
    def __init__(self, json_path):
        self.clothing_info = json.loads(json_path)

    def __str__(self) -> str:
        return f"Numbers of unlocked clothing : {self.clothing_info['unlocked_clothing_count']}, number of available clothing :  {self.clothing_info['clothing_count']}"
    
    def get_number_of_available_clothing(self) -> int :
        return self.clothing_info['clothing_count']
    
    def get_number_of_unlocked_clothing(self) -> int :
        return self.clothing_info['unlocked_clothing_count']
    
    def clothing_to_draw(self) -> str :
        active_clothing = self.clothing_info["active_clothing"]
        return active_clothing[str(max(map(int, active_clothing.keys())))]
    
    def add_clothing(self) -> None :
        if self.clothing_info['unlocked_clothing_count'] + 1 <= self.clothing_info[''] 
        self.clothing_info['unlocked_clothing_count'] += 1 
        index = str(self.clothing_info['unlocked_clothing_count'])
        if index in self.clothing_info['available_clothing']:

