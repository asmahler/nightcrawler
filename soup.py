from bs4 import BeautifulSoup
import requests
import emoji
import datetime
import threading
import grequests

sitemap = []
good_urls = []
bad_urls = []
base_url = "https://mobiledev.drivetime.com"

start_time = datetime.datetime.now()

main_sitemap = requests.get(base_url + "/sitemap/make-search.xml")
dsr_sitemap = requests.get(base_url + "/sitemap/make-model.xml")
#ddp_sitemap = requests.get(base_url + "/sitemap-dd.xml")
#some_vehicle_sitemap = requests.get(base_url + "/sitemap-vd-343.xml")


main_data = main_sitemap.text
dsr_data = dsr_sitemap.text
#ddp_data = ddp_sitemap.text
#some_vehicles_data = some_vehicle_sitemap.text


main_soup = BeautifulSoup(main_data, 'html.parser')
dealership_soup = BeautifulSoup(dsr_data, 'html.parser')
#ddp_soup = BeautifulSoup(ddp_data, 'html.parser')
#some_vehicle_soup = BeautifulSoup(some_vehicles_data, 'html.parser')

def sitemap_builder(xml_sitemap):
	sitemap_links = xml_sitemap.find_all("loc")
	for loc in sitemap_links:
		sitemap.append(loc.getText())
	return sitemap

def url_checker(url_status):
	for status in url_status:
		if status.status_code == 200:
			good_urls.append(status)
		else:
			bad_urls.append(status.url)
	return good_urls, bad_urls
			

main_links = sitemap_builder(main_soup)
dealership_links = sitemap_builder(dealership_soup)
#ddp_links = sitemap_builder(ddp_soup)
#some_vehicle_links = sitemap_builder(some_vehicle_soup)


main_links.append( base_url + '/alexiscool')

rs = (grequests.get(link) for link in main_links)

all_statuses = grequests.map(rs)

url_checker(all_statuses)

end_time = datetime.datetime.now()
total_time = end_time - start_time

print "You have checked: {0} Links!".format(len(main_links))
print emoji.emojize(":100: WooHoo!!!: {0} Good URL's Checked".format(len(good_urls)))
if bad_urls:
	for url in bad_urls: 
		print emoji.emojize(':poop: :cry: Oh No!! {0} is a 404!'.format(url)) 
print total_time


