from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from pyfiglet import figlet_format
import requests
import datetime
import threading

print(figlet_format("NightCrawler"))

sitemap = []
good_urls = []
bad_urls = []
none_urls = []
base_url = "https://www.weebly.com"

start_time = datetime.datetime.now()

main_sitemap = requests.get(base_url + "/sitemap.xml")
# dsr_sitemap = requests.get(base_url + "/sitemap/city-state-make-vehicles.xml")
# ddp_sitemap = requests.get(base_url + "/sitemap-dd.xml")
# some_vehicle_sitemap = requests.get(base_url + "/sitemap-vsr-3109509.xml")


main_data = main_sitemap.text
# dsr_data = dsr_sitemap.text
# ddp_data = ddp_sitemap.text
# some_vehicles_data = some_vehicle_sitemap.text


main_soup = BeautifulSoup(main_data, 'html.parser')
# dealership_soup = BeautifulSoup(dsr_data, 'html.parser')
# ddp_soup = BeautifulSoup(ddp_data, 'html.parser')
# some_vehicle_soup = BeautifulSoup(some_vehicles_data, 'html.parser')

def sitemap_builder(xml_sitemap):
	sitemap_links = xml_sitemap.find_all("loc")
	for loc in sitemap_links:
		sitemap.append(loc.getText())
	return sitemap

def url_checker(url_status): 
	if url_status.status_code == 200: 
		good_urls.append(url)
	elif url_status.status_code == 404: 
		bad_urls.append(url_status.url)
	else: 
		none_urls.append(url_status.url)
	return good_urls, bad_urls, none_urls
	

main_links = sitemap_builder(main_soup)
# dealership_links = sitemap_builder(dealership_soup)
# ddp_links = sitemap_builder(ddp_soup)
# some_vehicle_links = sitemap_builder(some_vehicle_soup)

main_links.append(base_url + '/alexiscool')

pool = ThreadPoolExecutor(50)
futures = [pool.submit(requests.get,url) for url in main_links]
results = [r.result() for r in as_completed(futures)] 


poolForLoop = ThreadPool(20)
poolForLoop.map(url_checker, results) 
poolForLoop.close()
poolForLoop.join()


end_time = datetime.datetime.now()
total_time = end_time - start_time

print "You have checked: {0} Links!".format(len(main_links))
print("WooHoo!!!: {0} Good URL's Checked".format(len(good_urls)))
if bad_urls:
	for url in bad_urls: 
		print('Oh No!! 404: {0}'.format(url))
if none_urls:
	for url in bad_urls: 
		print('Whoops, nothing found! Check this: {0}'.format(url)) 

print "Total Time: {0}".format(total_time)
