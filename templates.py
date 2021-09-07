from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import time

os.chdir('D://web_scrapping//')
url_numbers = [str(i) for i in range(1,11)]
url = 'https://timesofindia.indiatimes.com/entertainment/latest-new-movies/english-movies?curpg='
def get_details(url, url_numbers):
	movie_titles = []
	cast_names= []
	critics_ratings = []
	avg_user_ratings = []
	movie_langues_actions = []
	movie_duration = []

	for i in url_numbers:
		print(f'{i} page information is retreiving...')
		response = requests.get(url + i)
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			titles_duration = soup.find_all('div', {'class':'FIL_right'})
			for title in titles_duration:
				try:
					name = title.find({'h3'})
					movie_titles.append(name.text.strip())
				except:
					movie_titles.append(None)

			for duration in titles_duration:
				try:
					d = duration.find({'h4'})
					movie_duration.append(d.text.strip())
				except:
					movie_duration.append(None)

			time.sleep(2)

			castnames = soup.find_all('p', {'class':'castnames_wrapper'})
			for names in castnames:
				names_list = []
				try:
					name = names.find_all({'a'})
					for n in name:
						names_list.append(n.text.strip())
				except Exception as e:
					print('Error' + e)
					cast_names.append(None)
				cast_names.append(names_list)
				print(len(names_list))
			time.sleep(2)

		print(f'{i} page is done..')

	return (movie_titles, cast_names, movie_duration)

def main():
	url_numbers = [str(i) for i in range(1,6)]
	url = 'https://timesofindia.indiatimes.com/entertainment/latest-new-movies/english-movies?curpg='
	data = get_details(url, url_numbers)
	DataFrame = pd.DataFrame({
		"Movie Names" : data[0],
		# "Cast Names" : data[1],
		"Movie duration" : data[2]
		})
	DataFrame.to_csv('movie_info.csv', index=False)


	return 'Success'

if __name__ == '__main__':
	main()


