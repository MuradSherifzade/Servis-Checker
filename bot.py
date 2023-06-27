from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json

app = Client("my_bot", api_id="ur_api_id", api_hash="ur_api_id", bot_token="ur_bot_token")
# my.telegram.org & t.me/BotFather

ADMIN_USER_ID = "ur_id"

with open("services.json") as file:
     services = json.load(file)["services"]

with open('log.txt', 'r') as file:
            lines = file.readlines()
            last_10_lines = lines[-11:]
            last_10_lines_str = ''.join(last_10_lines)

@app.on_message(filters.command("start"))
def start(client, message):
    if message.from_user.id == ADMIN_USER_ID:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Services", callback_data="services")]
        ])
        message.reply_text("Hello admin!", reply_markup=keyboard)
    else:
        message.reply_text("u re not admin")


@app.on_callback_query()
def callback_query_handler(client, callback_query):
    data = callback_query.data

    if data == "services":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📍 All Services", callback_data="all")],
            [InlineKeyboardButton("📍 Active Services", callback_data="active")]
        ])
        callback_query.message.edit_text("**📍 Services**\n\nUse the buttons below to see the available and active services.", reply_markup=keyboard)
    
    elif data == "all":
        buttons = []
        for idx, service in enumerate(services):
            buttons.append([InlineKeyboardButton(service["serviceName"], callback_data=f"service_{idx}")])
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="services")])
        keyboard = InlineKeyboardMarkup(buttons)
        
        callback_query.message.edit_text("Services:", reply_markup=keyboard)

    elif data.startswith("service_"):
            index = int(data.split("_")[1])
            service = services[index]

            with open('log.txt', 'r') as file:
                lines = file.readlines()
                last_10_lines = lines[-11:]
                last_10_lines_str = ''.join(last_10_lines)

            status = "open ✅" if service["serviceStatus"] else "close ❌"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Change", callback_data=f"toggle_{index}")],
                [InlineKeyboardButton("🔙 Back", callback_data="all")]
            ])
            callback_query.message.edit_text(f"{service['serviceName']}\n**Status:** {status}\n\n**📃 Log:**\n```{last_10_lines_str}```", reply_markup=keyboard)

    elif data.startswith("toggle_"):
            index = int(data.split("_")[1])
            services[index]["serviceStatus"] = not services[index]["serviceStatus"]       

            with open("services.json", "w") as file:
                json.dump({"services": services}, file)
            with open('log.txt', 'r') as file:
                lines = file.readlines()
                last_10_lines = lines[-11:]
                last_10_lines_str = ''.join(last_10_lines)

            service = services[index]
            status = "open ✅" if service["serviceStatus"] else "close ❌"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Change", callback_data=f"toggle_{index}")],
                [InlineKeyboardButton("🔙 Back", callback_data="all")]
            ])

            callback_query.message.edit_text(f"{service['serviceName']}\n**Status:** {status}\n\n**📃 Log:**\n```{last_10_lines_str}```", reply_markup=keyboard)

    elif data == "active":
        with open("services.json") as file:
            servicesX = json.load(file)["services"]
        message_text = "\n".join(f"• {service['serviceName']}" for service in servicesX if service['serviceStatus'])
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("♻ Update", callback_data="active")],
            [InlineKeyboardButton("🔙 Back", callback_data="services")]
        ])
        callback_query.message.edit_text(message_text, reply_markup=keyboard)
    
    elif data == "start":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🧑‍💻 About", callback_data="about")],
            [InlineKeyboardButton("🌐 Services", callback_data="services")]
        ])
        callback_query.message.edit_text("Hello admin!", reply_markup=keyboard)

    elif data == "delete":
        callback_query.message.delete()

app.run()
