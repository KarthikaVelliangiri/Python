#  Program Requirement	: Interact with Webservice (OpenWeatherMap API) and retrieve data (Current Weather details).
#  Author				: Karthika Vellingiri
#  Date Created		    : 25 Feb 2024

import requests as req
import json.decoder
import datetime as dt
import zipcodes
import re


def get_coordinates(search_type, search_key):
    api_key = "cec6befc54d5759598e5d8208d5e5f10"

    # pass the api parameters based on the user choice of search type
    if search_type == 'z':
        geo_url = f"https://api.openweathermap.org/geo/1.0/zip?zip={search_key}&limit=5&appid={api_key}"
    else:
        geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={search_key}&limit=5&appid={api_key}"

    try:
        # connect to the geocode api to get the LAT & LON and parse the response to JSON format
        geo_response = req.get(geo_url, timeout = 10)
        geo_response.raise_for_status()
        get_coordinate = geo_response.json()

    # catch and handle the connectivity and API response parsing exceptions
    except req.exceptions.SSLError as e:
        print(f"\033[31m\nUnable to fetch coordinates due to Certificate Error.\nPlease check the exception: {e}.\033[0m")
    except req.exceptions.ConnectionError as e:
        print(f"\033[31m\nUnable to establish connection to Geocode API to fetch the coordinates.\nPlease check the exception: {e}.\033[0m")
    except req.exceptions.Timeout as e:
        print(f"\033[31m\nUnable to fetch coordinates as the Connection timed out.\nPlease check the exception: {e}.\033[0m")
    except req.exceptions.HTTPError as e:
        print(f"\033[31m\nUnable to retrieve the Location Co-ordinates due to the API connectivity failure exception."
              f"\nPlease check the exception: {e}.\033[0m")
    except json.decoder.JSONDecodeError as e:  # to handle the exception thrown at the time of parsing the response to json using json()
        print(f"\033[31m\nUnable to read the coordinate results retrieved.\nPlease check the exception: {e}.\033[0m")
    except KeyboardInterrupt:
        print("\033[31m\nForcefully Exited by Keyboard operations.\033[0m")
    except req.exceptions.RequestException as e:
        print(f"\033[31m\nUnexpected Error occurred while trying to fetch Coordinates.\nPlease check the exception: {e}.\033[0m")

    else:
        print("\033[32m\nSuccessfully connected to Geocode API to find the location coordinates!!!\033[0m")
        if len(get_coordinate) > 0:  # check the response have data in it

            try:
                # parse the JSON list to dictionary for the API response of city search to align with ZIP search format
                if isinstance(get_coordinate, list):
                    get_coordinate = get_coordinate[0]
                lat = get_coordinate['lat']
                lon = get_coordinate['lon']
            # handle the errors that will be thrown while accessing the list to retrieve the LAT & LON details
            except (IndexError, TypeError) as e:
                print(f"\033[31m\nError while fetching the coordinate from API response.\nPlease check the exception: {e}.\033[0m")
            except Exception as e:
                print(f"\033[31m\nUnexpected Error occurred while parsing the coordinate response.\nPlease check the exception: {e}.\033[0m")
            else:
                get_weather(lat, lon, api_key)

        else:
            # When no data is retrieved by the API display error message
            print("\033[31m\nNo co-ordinates found for the location entered.\nPlease retry with the correct location.\033[0m")


def get_weather(lat, lon, api_key):
    # defining variables for future use
    unit = ''
    icon = []

    # received the preferred temperature unit from the user
    unit_type = input("\033[34m\nPlease choose the number corresponding to your preferred unit for displaying weather information,"
                      "\033[0m\n\t1 - Celsius\n\t2 - Fahrenheit\n\t3 - Kelvin\n\033[34m\nYour preference is\t:\t\033[34m")

    # assign the API parameter and the weather unit icons based on user's preference
    if unit_type == "1":
        unit = "metric"
        icon = ["°C", "meter/sec"]
    elif unit_type == "2":
        unit = "imperial"
        icon = ["°F", "miles/hour"]
    elif unit_type == "3":
        unit = "standard"
        icon = [" K", "meter/sec"]
    else:
        # display error message for incorrect output
        print("\033[31m\nEntered metric value is incorrect. Please try again.\033[0m")

    if unit != "":

        try:
            # access current weather data API to fetch the weather details
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={unit}"
            weather_response = req.get(weather_url, timeout = 10)
            weather_response.raise_for_status()
            weather_details = weather_response.json()

        # catch and handle the connectivity and API response parsing exceptions
        except req.exceptions.SSLError as e:
            print(f"\033[31m\nUnable to fetch coordinates due to Certificate Error.\nPlease check the exception: {e}.\033[0m")
        except req.exceptions.ConnectionError as e:
            print(f"\033[31m\nUnable to establish connection to fetch the coordinates.\nPlease check the exception: {e}.\033[0m")
        except req.exceptions.Timeout as e:
            print(f"\033[31m\nUnable to fetch coordinates as the Connection timed out.\nPlease check the exception: {e}.\033[0m")
        except req.exceptions.HTTPError as e:
            print(f"\033[31m\nUnable to retrieve the Location Co-ordinates due to the API connectivity failure exception."
                  f"\nPlease check the exception :{e}.\033[0m")
        except json.decoder.JSONDecodeError as e:  # to handle the exception thrown at the time of parsing the response to json using json()
            print(f"\033[31m\nUnable to read the coordinate results retrieved.\nPlease check the exception: {e}.\033[0m")
        except KeyboardInterrupt:
            print("\033[31m\nForcefully Exited by Keyboard operations.\033[0m")
        except req.exceptions.RequestException as e:
            print(f"\033[31m\nUnexpected Error occurred while trying to fetch Coordinates.\nPlease check the exception: {e}.\033[0m")

        else:
            # on successful response print the weather details to the user
            print("\033[32m\nSuccessfully connected to weather API to get the weather details!!!\033[0m")
            print_weather(weather_details, icon)


def print_weather(weather_data, icon):
    # dictionary for API response weather code and icon
    icons = {'01d':  '☀️', '01n':  '🌙', '02d':  '⛅', '02n':  '🌙⛅', '03d':  ' ☁️', '03n':  '☁️', '04d':  '☁️', '04n':  '☁️', '09d':  '🌧️',
             '09n':  '🌧️', '10d':  '🌦️', '10n':  '🌦️', '11d':  '⛈️', '11n':  '⛈️', '13d':  '❄️', '13n':  '❄️', '50d':  '🌫️', '50n':  '🌫️'}

    try:
        # extract the weather details from the API response
        location = weather_data['name'] + (f",{weather_data['sys']['country']}" if 'sys' in weather_data else '')
        temp = f"{weather_data['main']['temp']}{icon[0]}"
        feels_like = f"{weather_data['main']['feels_like']}{icon[0]}"
        low_temp = f"{weather_data['main']['temp_min']}{icon[0]}"
        high_temp = f"{weather_data['main']['temp_max']}{icon[0]}"
        pressure = f"{weather_data['main']['pressure']} hPa"
        humidity = f"{weather_data['main']['humidity']}%"
        cloud_cover = f"{weather_data['clouds']['all']}%"
        description = weather_data['weather'][0]['description']
        wind_speed = f"{weather_data['wind']['speed']} {icon[1]}"
        current_weather_icon = icons.get(weather_data['weather'][0]['icon'], "")

    # Exceptions while accessing the list and type conversions for date formatting
    except (IndexError, KeyError) as e:
        print(f"\033[31m\nUnable to fetch the weather information.\nPlease check the exception : {e}.\033[0m")
    except KeyboardInterrupt:
        print("\033[31m\nForcefully Exited by Keyboard operations.\033[0m")
    except Exception as e:
        print(f"\033[31m\nUnexpected error occurred.\nPlease check the exception : {e}.\033[0m")

    else:
        # print the weather details to the user
        print(f"\t\033[33m\nCurrent Weather status of {location} is,")
        print(f"\t{current_weather_icon}"+"{:<20} :\t{}".format("\tCurrent Temperature", temp))
        print(f"\t{current_weather_icon}"+"{:<20} :\t{}".format("\tFeels Like", feels_like))
        print("\t\033[0m\u2191\033[33m{:<20} :\t{}".format("\tHigh Temperature", high_temp))
        print("\t\033[0m\u2193\033[33m{:<20} :\t{}".format("\tLow Temperature", low_temp))
        print("\t\U0001F4A8{:<20} :\t{}".format("\tWind Speed", wind_speed))
        print("\t\U0001F4C8{:<20} :\t{}".format("\tPressure", pressure))
        print("\t\U0001F4A7{:<20} :\t{}".format("\tHumidity", humidity))
        print("\t☁️{:<20} :\t{}".format("\tCloud Cover", cloud_cover))
        print(f"\t{current_weather_icon}"+"{:<20} :\t{}".format("\tDescription", description))


def main():
    title = "\033[1m\033[34m\033[4mOpen Weather - Your Daily Dose of Weather Wisdom!!!\033[0m"
    welcome_msg = "Step outside with confidence! Welcome to our Open Weather app, your trusted companion for all things weather."
    print(f"\033[92m\n\n {title.center(150)}")
    print(f"\033[32m\n\n{welcome_msg}")

    # hard coding the country code
    country_code = "US"

    # defining the acceptable ZIP, city and state input format
    zip_pattern = re.compile(r'^[0-9]\d{4}$|^[0-9]\d{4}-\d{4}$')
    city_state_pattern = re.compile(r'^[A-Za-z ]*$')

    while True:
        # receive the lookup type from the user
        search_type = input("\033[34m\nTo continue with the Application, Please Enter \033[0m\n\tZ to lookup weather using ZIP code "
                            "\n\tC to lookup weather using City Name\033[34m\nif not, Enter\033[0m\n\tE to Exit the Application\033[34m"
                            "\n\nYourInput is\t:\t").lower()

        if search_type == 'z':
            zip_code = input("\033[34m\nEnter the ZIP code to look up for weather :   \033[0m")

            # check for the valid ZIP format and validate the ZIP code
            if re.match(zip_pattern, zip_code):
                if zipcodes.is_real(zip_code) is False:
                    print("\033[31m\nEntered is not a Valid US ZIP code. Please try again with a valid ZIP code.\033[0m")

                else:
                    # convert the 9 digit ZIP code to 5 digit code
                    if '-' in zip_code:
                        zip_code = zip_code.split('-')[0]
                    search_key = f"{zip_code},{country_code}"
                    # call geocode API to find the LAT & LON
                    get_coordinates(search_type, search_key)

            else:
                print("\033[31m\nPlease try again with correct ZIP code format(12345 or 12345-6789).\033[0m")

        elif search_type == 'c':
            city_name = input("\033[34m\nEnter the City you would like to check weather : \033[0m")

            # Validate the City name for format
            if re.match(city_state_pattern, city_name):
                city_state = input("\033[34mEnter the State Name or State Code (California/CA) in which the City is in : \033[0m")
                # Validate the State name for format
                if re.match(city_state_pattern, city_state):
                    search_key = f"{city_name},{city_state},{country_code}"
                    # call geocode API to find the LAT & LON
                    get_coordinates(search_type, search_key)
                else:
                    print("\033[31m\nOnly alphabets are allowed for State Name. Please try again with correct format.\033[0m")
            else:
                # print error message for incorrect City name format
                print("\033[31m\nOnly alphabets are allowed for City Name. Please try again with correct format.\033[0m")

        elif search_type == 'e':
            # exit the application on user request
            print("\033[92m\nThank you for making our Weather App a part of your daily routine. We hope it has been informative and helpful.\033[0m")
            exit()

        else:
            # continue with the application on invalid user input and allow to continue with the execution as preferred
            print("\033[31m\nInvalid input entered. Please try again as per the options provided.\033[0m")


if __name__ == "__main__":
    main()
