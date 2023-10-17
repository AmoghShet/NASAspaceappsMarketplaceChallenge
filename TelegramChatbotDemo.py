import telebot
from telebot import types
import requests
import json

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('ENTER_YOUR_KEY')

# Create a dictionary to store user roles and states
user_data = {}

# Define available roles and states
ROLES = ["Seeker", "Provider"]
MAIN_MENU = "Main Menu"
SEEKER_MENU = "Seeker Menu"
PROVIDER_MENU = "Provider Menu"

# Define the API endpoints for Seeker and Provider profiles
seeker_profile_url = 'http://43.205.65.107:8081/api/v1/Seeker/search'
provider_profile_url = 'http://43.205.65.107:8081/api/v1/Provider/search'
project_search_url = 'http://43.205.65.107:8081/api/v1/Project/search'

# Define keyboard markup for the main menu with a "Back" button
main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
seeker_button = types.KeyboardButton("Seeker")
provider_button = types.KeyboardButton("Provider")
main_menu_markup.add(seeker_button, provider_button, types.KeyboardButton("Back"))

# Define keyboard markup for the Seeker menu with a "Back" button
seeker_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
seeker_profile_button = types.KeyboardButton("Profile")
seeker_back_button = types.KeyboardButton("Back")
seeker_search_projects_button = types.KeyboardButton("Search Projects")
seeker_menu_markup.row(seeker_profile_button, seeker_back_button)
seeker_menu_markup.row(seeker_search_projects_button)

# Define keyboard markup for the Provider menu with a "Back" button
provider_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
provider_profile_button = types.KeyboardButton("Profile")
provider_back_button = types.KeyboardButton("Back")
provider_review_applicants_button = types.KeyboardButton("Review Applicants")
provider_menu_markup.row(provider_profile_button, provider_back_button)
provider_menu_markup.row(provider_review_applicants_button)

# Define keyboard markup for project selection with a "Back" button
project_selection_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
select_project_button = types.KeyboardButton("Select Project")
project_selection_markup.row(select_project_button, types.KeyboardButton("Back"))

# Variable to store the user's project selection
selected_project = None

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_data[user_id] = {"role": None, "state": MAIN_MENU}
    bot.send_message(user_id, "Choose your role:", reply_markup=main_menu_markup)

@bot.message_handler(func=lambda message: message.text == "Seeker" or message.text == "Provider")
def handle_role_selection(message):
    user_id = message.chat.id
    role = message.text
    user_data[user_id]["role"] = role
    user_data[user_id]["state"] = MAIN_MENU

    if role == "Seeker":
        bot.send_message(user_id, "You selected 'Seeker' role.", reply_markup=seeker_menu_markup)
    elif role == "Provider":
        bot.send_message(user_id, "You selected 'Provider' role.", reply_markup=provider_menu_markup)

@bot.message_handler(func=lambda message: message.text == "Profile")
def handle_profile(message):
    user_id = message.chat.id
    role = user_data[user_id]["role"]

    if role == "Seeker":
        profile_url = seeker_profile_url
    elif role == "Provider":
        profile_url = provider_profile_url
    else:
        bot.send_message(user_id, "Invalid role selected.")
        return

    # Send a POST request to the API
    if role == 'Seeker':
        response = requests.post(profile_url, json={"filters": {
            "SeekerName": {
                "eq": "DemoMan"
            }
        }})
        
    if role == 'Provider':
        response = requests.post(profile_url, json={"filters": {
            "ProviderName": {
                "eq": "DemoMan"
            }
        }})

    if response.status_code == 200:
        try:
            # Parse the JSON response
            json_data = response.json()
            if role == 'Seeker':
                profilename_list = [item['SeekerName'] for item in json_data if 'SeekerName' in item]
                profilemail_list = [item['SeekerEmail'] for item in json_data if 'SeekerEmail' in item]
                profilPhoneno_list = [item['Phoneno'] for item in json_data if 'Phoneno' in item]
                profilSkills_list = [item['Skills'] for item in json_data if 'Skills' in item]

                response_text = "Data from API:\n"

                for name in profilename_list:
                    response_text += "Name: " + name + "\n"

                for mail in profilemail_list:
                    response_text += "Email: " + mail + "\n"

                for no in profilPhoneno_list:
                    response_text += "Phone: " + no + "\n"

                for skills in profilSkills_list:
                    response_text += "Skills: " + skills + "\n"
            
            if role == 'Provider':
                profilename_list = [item['ProviderName'] for item in json_data if 'ProviderName' in item]
                profilemail_list = [item['ProviderEmail'] for item in json_data if 'ProviderEmail' in item]
                profilPhoneno_list = [item['Phoneno'] for item in json_data if 'Phoneno' in item]

                response_text = "Data from API:\n"

                for name in profilename_list:
                    response_text += "Name: " + name + "\n"

                for mail in profilemail_list:
                    response_text += "Email: " + mail + "\n"

                for no in profilPhoneno_list:
                    response_text += "Phone: " + no + "\n"

            bot.reply_to(message, response_text)
        except json.JSONDecodeError:
            bot.send_message(user_id, "Error: Unable to parse JSON response from the API.")
    else:
        bot.send_message(user_id, f"Request failed with status code: {response.status_code}")

@bot.message_handler(func=lambda message: message.text == "Back")
def handle_back(message):
    user_id = message.chat.id
    user_data[user_id]["state"] = MAIN_MENU
    bot.send_message(user_id, "Back to the main menu.", reply_markup=main_menu_markup)

@bot.message_handler(func=lambda message: message.text == "Search Projects")
def handle_search_projects(message):
    user_id = message.chat.id
    response = requests.post(project_search_url, json={"filters" : {} })

    if response.status_code == 200:
        try:
            # Parse the JSON response
            json_data = response.json()

            response_text = "Available Projects:\n"
            bot.send_message(user_id, response_text)

            noofresponses = len(json_data)

            print(noofresponses)

            for n in range(noofresponses):
                projecttitle_list = [json_data[n]['ProjectTitle']]
                projectowner_list = [json_data[n]['ProjectOwner']]
                projectstartdate_list = [json_data[n]['ProjectStartDate']]
                projectmembers_list = [json_data[n]['ProjectMembers']]

                response_text = "Data from API:\n"
                for name in projecttitle_list:
                    response_text += "Name: " + name + "\n"

                for mail in projectowner_list:
                    response_text += "Email: " + mail + "\n"

                for date in projectstartdate_list:
                    response_text += "Start: " + date + "\n"

                for members in projectmembers_list:
                    response_text += "Members: " + members + "\n"

                bot.send_message(user_id, response_text)

            # Create buttons for selecting a project
            project_selection_buttons = []
            for i in range(1, noofresponses + 1):
                button_text = str(i)
                project_selection_buttons.append(types.KeyboardButton(button_text))

            # Add the project selection buttons to the keyboard markup
            project_selection_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            project_selection_markup.add(*project_selection_buttons)
            project_selection_markup.row(types.KeyboardButton("Back"))

            bot.send_message(user_id, "Choose a project (1 to " + str(noofresponses) + ")", reply_markup=project_selection_markup)

        except json.JSONDecodeError:
            bot.send_message(user_id, "Error: Unable to parse JSON response from the API.")
    else:
        bot.send_message(user_id, f"Request failed with status code: {response.status_code}")

# Handle project selection
@bot.message_handler(func=lambda message: message.text.isdigit() and selected_project is None)
def handle_project_selection(message):
    global selected_project
    selected_project = int(message.text)
    user_id = message.chat.id
    print(f"Selected Project: {selected_project}")
    user_id = message.chat.id
    response = requests.post(project_search_url, json={"filters" : {} })

    if response.status_code == 200:
        try:
            # Parse the JSON response
            json_data = response.json()

            noofresponses = len(json_data)


            projecttitle_list = [json_data[selected_project-1]['ProjectTitle']]
            projectowner_list = [json_data[selected_project-1]['ProjectOwner']]
            projectstartdate_list = [json_data[selected_project-1]['ProjectStartDate']]
            projectmembers_list = [json_data[selected_project-1]['ProjectMembers']]
            

            response_text = "You have selected:\n"
            for name in projecttitle_list:
                response_text += "Name: " + name + "\n"

            for owner in projectowner_list:
                response_text += "Owner: " + owner + "\n"

            for date in projectstartdate_list:
                response_text += "Started: " + date + "\n"

            for members in projectmembers_list:
                response_text += "Members: " + members + "\n"

            bot.send_message(user_id, response_text)

        except json.JSONDecodeError:
            bot.send_message(user_id, "Error: Unable to parse JSON response from the API.")
    else:
        bot.send_message(user_id, f"Request failed with status code: {response.status_code}")

# Handle "Back" button in project selection
@bot.message_handler(func=lambda message: message.text == "Back" and selected_project is not None)
def handle_back_in_project_selection(message):
    global selected_project
    selected_project = None
    user_id = message.chat.id
    bot.send_message(user_id, "Back to project selection.", reply_markup=project_selection_markup)

# Start the bot
bot.polling()
