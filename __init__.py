from flask import Flask
from xml.etree import ElementTree as etree
from urllib.request import urlopen
import requests
from lxml import html
import json
class food:
    def __init__(self,name,description,date,link):
        self.name = name
        self.date = date
        self.place = ""
        self.mealtime = description[description.find(":")+1:description.find(";")].strip()
        self.preferences = []
        self.contains = []
        description = description.split(";")
        for pref_contains in description:
            if "Preferences" in pref_contains:
                self.preferences = pref_contains[pref_contains.find(":") + 1:].strip().split(",")
            elif "Contains" in pref_contains:
                self.contains = pref_contains[pref_contains.find(":") + 1:].strip().split(",")
        self.find_place(link)
    def find_place(self,link):
        page = requests.get(link)
        tree = html.fromstring(page.content)
        self.place = tree.xpath("//*[@id='block-eatatstate-content']/div/article/div/div[3]/div[2]/div")[0].text
    def __str__(self):
        return "name: {}\nmealtime: {}\npreferences: {}\ncontains: {}\ndate: {}\nplace: {}"\
            .format(self.name,self.mealtime,self.preferences,self.contains,self.date,self.place)

def get_caf_food(rss_caf):
    food_list = []
    url_ = urlopen(rss_caf)
    url_read = url_.read()
    url_.close()
    url_root = etree.fromstring(url_read)
    items = url_root.findall('channel/item')
    for item in items:
        food_item = food(item.find("title").text, item.find("description").text, item.find("pubDate").text, \
                         item.find("link").text)
        food_list.append(food_item)
    return food_list

'''
{
    "shaw": {
        "Lunch": {
            "Wok": [
                "Jasmine Rice"
            ],
            "Breadbox": [
                "Cheese Pizza"
            ],
            "Garden": [
                "Moroccan Chickpea Soup"
            ],
            "Main": [
                "Ancho Cherry BBQ Sauce"
            ]
        },
        "Breakfast": {
            "Platform": [
                "Peaches and Cream Oatmeal",
                "Hard Cooked Eggs",
                "Congee with Ginger and Scallions",
                "Seasoned Diced Potatoes",
                "Egg and Cheese Muffin",
                "Sausage Patties",
                "Scrambled Eggs"
            ]
        }
    }
}

'''
def create_json(food_list,menu):
    food_meal_time = {}
    for each_food_meal in food_list:
        if each_food_meal.mealtime not in food_meal_time:
            food_meal_time[each_food_meal.mealtime] = {each_food_meal.place:[each_food_meal.name]}
        else:
            #ex: if breakfast in food_meal_time but "boilingpoint" is not
            if each_food_meal.place not in food_meal_time[each_food_meal.mealtime]:
                food_meal_time[each_food_meal.mealtime][each_food_meal.place] =[each_food_meal.name]
            else:
                food_meal_time[each_food_meal.mealtime][each_food_meal.place].append(each_food_meal.name)

    return  {menu:food_meal_time}


json_akers = create_json(get_caf_food('https://eatatstate.msu.edu/menu/The%20Edge%20at%20Akers/all/all/rss.xml'),"The Edge at Akers")
json_brody = create_json(get_caf_food('https://eatatstate.msu.edu/menu/Brody%20Square/all/all/rss.xml'),"Brody Square")
json_case = create_json(get_caf_food('https://eatatstate.msu.edu/menu/South%20Pointe%20at%20Case/all/all/rss.xml'),"South Pointe at Case")
json_holden = create_json(get_caf_food('https://eatatstate.msu.edu/menu/Holden%20Dining%20Hall/all/all/rss.xml'), "Holden Dining Hall")
json_landon = create_json( get_caf_food('https://eatatstate.msu.edu/menu/Heritage%20Commons%20at%20Landon/all/all/rss.xml'),"Heritage Commons at Landon")
json_riverwalk = create_json(get_caf_food('https://eatatstate.msu.edu/menu/Riverwalk%20Market%20at%20Owen/all/all/rss.xml'),"Riverwalk Market at Owen")
json_shaw = create_json(get_caf_food('https://eatatstate.msu.edu/menu/The%20Vista%20at%20Shaw/all/all/rss.xml'),"The Vista at Shaw")
json_snyder = create_json(get_caf_food('https://eatatstate.msu.edu/menu/The%20Gallery%20at%20Snyder%20Phillips/all/all/rss.xml'),"The Gallery at Snyder Phillips")
json_wilson = create_json(get_caf_food('https://eatatstate.msu.edu/menu/Wilson%20Dining%20Hall/all/all/rss.xml'), "Wilson Dining Hall")
export_json = {}
export_json.update(json_akers)
export_json.update(json_brody)
export_json.update(json_case)
export_json.update(json_holden)
export_json.update(json_landon)
export_json.update(json_riverwalk)
export_json.update(json_shaw)
export_json.update(json_snyder)
export_json.update(json_wilson)

app = Flask(__name__)
@app.route('/')
def homepage():
    return json.dumps(export_json,indent=4)

if __name__ == "__main__":
    app.run()



