import requests
from datetime import datetime
import smtplib
import time

MY_LAT = <INSERT-LAT>    # Your latitude as float
MY_LONG = <INSERT-LONG>   # Your longitude as float
MY_EMAIL = "<INSERT-EMAIL>"
PASSWORD = "<INSERT-PASSWORD>"
SMTP = "smtp.gmail.com"

def is_near():
    """Check is ISS is near your location"""
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])  # gets the data we want from dictionaries
    iss_longitude = float(data["iss_position"]["longitude"])    # gets the data we want from dictionaries

    #Your position is within +5 or -5 degrees of the ISS position.
    if (iss_latitude > MY_LAT + 5 or iss_latitude < MY_LAT - 5) or (iss_longitude > MY_LONG + 5 or iss_longitude <  MY_LONG - 5):
        return False    # if it's not within the distance
    else:
        return True     # if it's above me


def is_night():
    """Check if it's dark."""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # sunrise and sunset time is in 12-hour style whereas time_now is in 24-hour style
    # we have to unify this, is this case another api parameter called formatted set to 0

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])    # hour of sunrise
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])      # hour of sunset


    time_now = datetime.now().hour  # time/hour now

    if time_now >= sunset or time_now <= sunrise:   # if it's dark
        return True


while True:     # to run all over again
    time.sleep(60)      # every 60 seconds
    if is_near() and is_night():    # if ISS is above and is night
        with smtplib.SMTP(SMTP) as connection:  # send myself an email
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:ISS Overhead\n\nLook up! ISS is above you!"
            )
