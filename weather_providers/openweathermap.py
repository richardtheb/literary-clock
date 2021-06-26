import logging
from weather_providers.base_provider import BaseWeatherProvider


class OpenWeatherMap(BaseWeatherProvider):
    def __init__(self, openweathermap_apikey, location_lat, location_long, units):
        self.openweathermap_apikey = openweathermap_apikey
        self.location_lat = location_lat
        self.location_long = location_long
        self.units = units

    # Map OpenWeatherMap icons to local icons
    # Reference: https://openweathermap.org/weather-conditions
    def get_icon_from_openweathermap_weathercode(self, weathercode, is_daytime):

        icon_dict = {
                        200: "lightning",  # thunderstorm with light rain
                        201: "lightning",  # thunderstorm with rain
                        202: "rain_lightning",  # thunderstorm with heavy rain
                        210: "lightning",  # light thunderstorm
                        211: "lightning",  # thunderstorm
                        212: "rain_lightning",  # heavy thunderstorm
                        221: "lightning",  # ragged thunderstorm
                        230: "lightning",  # thunderstorm with light drizzle
                        231: "lightning",  # thunderstorm with drizzle
                        232: "rain_lightning",  # thunderstorm with heavy drizzle
                        300: "rain0_sun" if is_daytime else "rain1_moon",  # light intensity drizzle
                        301: "rain0_sun" if is_daytime else "rain1_moon",  # drizzle
                        302: "rain1_sun" if is_daytime else "rain1_moon",  # heavy intensity drizzle
                        310: "rain0_sun" if is_daytime else "rain1_moon",  # light intensity drizzle rain
                        311: "rain1_sun" if is_daytime else "rain1_moon",  # drizzle rain
                        312: "rain1",  # heavy intensity drizzle rain
                        313: "rain1_sun" if is_daytime else "rain1_moon",  # shower rain and drizzle
                        314: "rain1" if is_daytime else "rain1_moon",  # heavy shower rain and drizzle
                        321: "rain0",  # shower drizzle
                        500: "rain0",  # light rain
                        501: "rain1",  # moderate rain
                        502: "rain2",  # heavy intensity rain
                        503: "rain2",  # very heavy rain
                        504: "rain2",  # extreme rain
                        511: "rain_snow",  # freezing rain
                        520: "rain0_sun" if is_daytime else "rain1_moon",  # light intensity shower rain
                        521: "rain1_sun" if is_daytime else "rain1_moon",  # shower rain
                        522: "rain2",  # heavy intensity shower rain
                        531: "rain1",  # ragged shower rain
                        600: "snow_sun" if is_daytime else "snow_moon",  # light snow
                        601: "snow",  # Snow
                        602: "snow",  # Heavy snow
                        611: "snow",  # Sleet
                        612: "rain_snow",  # Light shower sleet
                        613: "rain_snow",  # Shower sleet
                        615: "rain_snow",  # Light rain and snow
                        616: "rain_snow",  # Rain and snow
                        620: "snow_sun" if is_daytime else "snow_moon",  # Light shower snow
                        621: "snow",  # Shower snow
                        622: "snow",  # Heavy shower snow
                        701: "rain0",  # mist
                        711: "rain0",  # Smoke
                        721: "rain0",  # Haze
                        731: "rain0",  # sand/ dust whirls
                        741: "rain0",  # fog
                        751: "rain0",  # sand
                        761: "rain0",  # dust
                        762: "rain0",  # volcanic ash
                        771: "wind",    # squalls
                        781: "wind",    # tornado
                        800: "sun" if is_daytime else "moon",  # clear sky
                        801: "cloud_sun" if is_daytime else "cloud_moon",  # few clouds: 11-25%
                        802: "cloud",  # scattered clouds: 25-50%
                        803: "clouds",  # broken clouds: 51-84%
                        804: "clouds",  # overcast clouds: 85-100%
                    }

        icon = icon_dict[weathercode]
        logging.debug(
            "get_icon_by_weathercode({}, {}) - {}"
            .format(weathercode, is_daytime, icon))

        return icon

    # Get weather from OpenWeatherMap One Call
    # https://openweathermap.org/api/one-call-api
    def get_weather(self):

        url = ("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly&units={}&appid={}"
               .format(self.location_lat, self.location_long, self.units, self.openweathermap_apikey))
        response_data = self.get_response_data(url)
        logging.debug(response_data)
        weather_data = response_data["daily"][0]
        logging.debug("get_weather() - {}".format(weather_data))

        # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        weather = {}
        weather["temperatureMin"] = weather_data["temp"]["min"]
        weather["temperatureMax"] = weather_data["temp"]["max"]
        weather["icon"] = self.get_icon_from_openweathermap_weathercode(weather_data["weather"][0]["id"], self.is_daytime(self.location_lat, self.location_long))
        weather["description"] = weather_data["weather"][0]["description"].title()
        logging.debug(weather)
        return weather
