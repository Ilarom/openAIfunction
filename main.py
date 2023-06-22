import openai
import json
openai.api_key = "APIKEY"

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = [
        {
        "location": "San francisco",
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    },
    {
        "location": "New York",
        "temperature": "75",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    ]
    return json.dumps(weather_info)

################################################################################################################
def get_current_order(orderNumber):
    """Get the order details for a given order number"""
    order_list = [
        {
            "order number": "1",
            "order details": "Hamburger",
            "unit": "euro",
            "order size": "Large",
        },
        {
            "order number": "2",
            "order details": "Fries",
            "unit": "euro",
            "order size": "Medium",
        },
        {
            "order number": "3",
            "order details": "Coca cola",
            "unit": "euro",
            "order size": "Small",
        }
    ]
    return json.dumps(order_list)
####################################################################################################################################################################################################
"""
def get_current_order(orderNumber,meal):
    order_info = {
        "order number": orderNumber,
        "order details": meal,
        "unit": "euro",
        "order size": "Large",
    }
    return json.dumps(order_info)
    """
# Step 1, send model the user query and what functions it has access to
def run_conversation():
    question = input("what do you want?")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[#{"role": "system", "content": "If the customer wants to know the weather you have to ask him to give you the name of the city. If he wants to know something about his order you have to ask him for the order number. Without these informations you can't continue"},
                  {"role": "user", "content": question}],
        functions=[
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
             #try to add a second function
            {
                "name": "get_current_order",
                "description": "Get the order details of a given order number in order to send to the restaurant the missing items",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order number": {
                            "type": "string",
                            "description": "The order number, e.g. 1 or 2 "
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["euro", "dollar"]
                        }
                    },
                    "required": ["order number"]
                }
            }
        ],
        function_call="auto",
    )
    message = response["choices"][0]["message"] #this is the function name
    choices = response["choices"][0]


    # Step 2, check if the model wants to call a function
    if message.get("function_call"):
        function_name = message["function_call"]["name"]

        # Step 3, call the function
        # Note: the JSON response from the model may not be valid JSON
        if function_name == "get_current_weather":
            function_response = get_current_weather(
            location=message.get("location"),
            unit=message.get("unit"),
        )
        elif function_name == "get_current_order":
            #print("order number is: ", message.get("order number"))
            function_response = get_current_order(
            orderNumber=message.get("order number")
            #meal=message.get("order details"),
        )
        #function_response = get_current_weather(
         #   orderNumber=message.get("order number"),
          #  unit=message.get("unit"),
        #)
        
        messages = [
    # {"role": "system", "content": "If the customer wants to know the weather you have to ask him to give you the name of the city. If he wants to know something about his order you have to ask him for the order number."},
    {"role": "user", "content": question},
    message,
    {
        "role": "function",
        "name": function_name,
        "content": function_response,
    },
    ]
        print("MESSAGES 2: ", messages)
        # Step 4, send model the info on the function call and function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )
        return second_response

#response_json = run_conversation()
#only_response = response_json["choices"][0]["message"]["content"]
#print(only_response)
print(run_conversation())
#print(get_current_order("1234","euro"))
