import httplib
from xml.etree.ElementTree import XML

weathericon = WeatherIcon()

def weather_update(self):
    conn = httplib.HTTPConnection("edos.debian.net")
    weather_url="/edos-debcheck/results/"+self.get_distro()+"/latest/"+self.get_arch()+"/weather.xml"
    conn.request("GET",weather_url)
    r1 = conn.getresponse()
    data = str()
    data = r1.read()
    weather_xml = XML(data)
    description = weather_xml.getiterator("description")[0].text
    weather = weather_xml.getiterator("index")[0].text
    total = weather_xml.getiterator('total')[0].text
    broken = weather_xml.getiterator('broken')[0].text
    url = weather_xml.getiterator('url')[0].text
    return weather


    index = weather_update()
    if index == '1':
        weathericon.set_clear()
    if index == '2':
        weathericon.set_few_clouds()
    if index == '3':
        weathericon.set_overcast()
    if index == '4':
        weathericon.set_shower()
    if index == '5':
        weathericon.set_storm()
