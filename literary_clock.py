import os
import textwrap
import sys
import time

from datetime import datetime
from glob import glob
from random import randrange
from inky.auto import auto
display = auto()
from weather_providers import openweathermap

def format_weather_description(weather_description):
    if len(weather_description) < 20:
        return {1: weather_description, 2: ''}

    splits = textwrap.fill(weather_description, 20, break_long_words=False,
                           max_lines=2, placeholder='...').split('\n')
    weather_dict = {1: splits[0]}
    weather_dict[2] = splits[1] if len(splits) > 1 else ''
    return weather_dict

def main():

	openweathermap_apikey = os.getenv("OPENWEATHERMAP_APIKEY")
	location_lat = os.getenv("WEATHER_LATITUDE")
	location_long = os.getenv("WEATHER_LONGITUDE")

	weather_provider = openweathermap.OpenWeatherMap(
		openweathermap_apikey,
		location_lat,
		location_long,
		"imperial"
	)

	weather = weather_provider.get_weather()

	degrees = "°F"

	weather_desc = format_weather_description(weather["description"])

	output_dict = {
		'LOW_ONE': "{}{}".format(str(round(weather['temperatureMin'])), degrees),
		'HIGH_ONE': "{}{}".format(str(round(weather['temperatureMax'])), degrees),
		'ICON_ONE': weather["icon"],
		'WEATHER_DESC_1': weather_desc[1],
		'WEATHER_DESC_2': weather_desc[2]
	}


	image = Image.new(mode='1', size=(800, 480), color=255)
	iconPath = 'icons/%s.xbm' % output_dict['ICON_ONE']
	iconImage = ImageOps.invert(Image.open(iconPath).resize((64, 64)).convert('L'))
	image.paste(iconImage, (20, 5))

	now = datetime.now()
	hour_minute = now.strftime('%H%M')

	quotes_path = 'images/metadata/quote_%s_*_credits.png' % hour_minute
	quotes = glob(quotes_path)
	if len(quotes) == 0:
		now_time = now.strftime('%H:%M')
		draw_time = ImageDraw.Draw(image)
		time_font = ImageFont.truetype('Literata72pt-Regular.ttf', 144)
		draw_time.text((220, 150), now_time, font=time_font, fill=0)
	else:
		quote = quotes[randrange(0, len(quotes))]
		quoteImage = Image.open(quote).convert('1')
		image.paste(quoteImage, (0, 80))

	today = now.strftime('%a, %B, %d')
	dayFont = ImageFont.truetype('Literata72pt-Regular.ttf', 48)
	drawImage = ImageDraw.Draw(image)
	drawImage.text((250, 10), today, font=dayFont, fill=0)
	tempFont = ImageFont.truetype('Literata72pt-Regular.ttf', 24)
	temp = '%s / %s' % (output_dict['HIGH_ONE'], output_dict['LOW_ONE'])
	drawImage.text((100, 20), temp, font=tempFont, fill=0)
	drawImage.line([(0, 78), (800, 78)], fill=0, width=4)
	drawImage.line([(225, 0), (225, 78)], fill=0, width=4)
	return image

if __name__ == '__main__':
	image = main()
	try:
        display.set_border(Inky.black)
	    display.set_image(image)
        display.show()
        
	except IOError as e:
		print(e)
	
	except KeyboardInterrupt:
		time.sleep(60)
