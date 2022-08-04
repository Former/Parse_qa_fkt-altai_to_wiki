# Copyright © 2020 Alexei Bezborodov. Contacts: <AlexeiBv+fkt_py@narod.ru>
# License: Public domain: http://unlicense.org/

from bs4 import BeautifulSoup
from urllib.request import urlopen

import os; import locale;  os.environ["PYTHONIOENCODING"] = "utf-8";  myLocale=locale.setlocale(category=locale.LC_ALL, locale="ru_RU.UTF-8");

def GetStrong(a_Par):
	for content_strong in par.find_all('strong'):
		content = content_strong.string
		
		if (content):
			return content
	
	return ""

# Исходный адрес сайта
url_site = 'fct-altai.ru' # 'xn----8sba0bbi0cdm.xn--p1ai' # 'фкт-алтай.рф'
base_url_wos = 'https://' + url_site 
base_url = base_url_wos + '/'

html_doc = urlopen(base_url).read()
soup = BeautifulSoup(html_doc, from_encoding = "utf-8")

# Блоки на офф сайте
for data_block in soup.find_all('div', 'block'):
	data_key = data_block.get('data-key')
	for vo_block in data_block.find_all('a'):
		vo_url = vo_block.get('href')
		
		if (vo_url.find("qa") != -1 and vo_url.find(url_site) == -1):
			vo_url = base_url_wos + vo_url
			print("vo_url:", vo_url)
			
			# Заходим на страницу вопроса-ответа
			html_vo = urlopen(vo_url).read()
			soup_vo = BeautifulSoup(html_vo,from_encoding="utf-8")
			  
			# Считываем дату
			h1 = soup_vo.find('h1');
			print('date:', h1)
			
			date = "";
			if (h1):
				date = h1.string[20:]
			
			# Добавляем в конечный файл дату и ссылку на стенограмму
			hronometrazh = "==" + date + "==\n"
			hronometrazh += "[[" + vo_url + " стенограмма]]\n\n" #.decode('utf-8')
			
			# Берём ссылку на ютюб
			# пример того, что есть на сайте: <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/RmZvzSM5vRI?showinfo=0"
			soup_iframe = soup_vo.find('iframe', "embed-responsive-item")
			if (soup_iframe == None):
				continue
			
			yout_link = soup_iframe.get("src")
			print("yout_link:", yout_link)
			yout_link = yout_link[yout_link.rfind('/') + 1:yout_link.rfind('?')]
			print("yout_link:", yout_link)
			yout_link = "https://www.youtube.com/watch?v=" + yout_link + "&t="
			
			# Раздел с хронометражём и стенограммой
			soup_answer = soup_vo.find('div', "answer-content")
			if(soup_answer == None):
				continue
			
			# Выходной файл
			out_file = open(data_key + " - " + date + '.txt', 'w')
			
			# Цикл по всем параграфам
			for par in soup_answer.find_all('p'):
				cur_hronometrazh = ""
				
				#print "par:", par.prettify()
				
				strong = GetStrong(par)
				
				if (strong):
					print("strong:", strong)
					
				# Параграф содержит надпись "Хронометраж:" - пропускаем
				if (strong == "Хронометраж:"): # \xd0\xa5\xd1\x80\xd0\xbe\xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x82\xd1\x80\xd0\xb0\xd0\xb6\x3a  .decode('utf-8')
					print ("continue")
					continue
				
				# Параграф содержит надпись "Стенограмма:" - заканчиваем работу с текущим ВО
				if (strong == "Стенограмма:"): #  \xd0\xa1\xd1\x82\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb3\xd1\x80\xd0\xb0\xd0\xbc\xd0\xbc\xd0\xb0\x3a  .decode('utf-8')
					print ("break")
					break
				
				is_time_added = False
				for content_span in par.find_all('span'):
					content = content_span.string
					if (content != "" and content != None):
						internal_content_span = content_span.find('span')
						is_last_span = internal_content_span == None

						internal_content_strong = par.find('strong')
						is_strong = internal_content_strong != None and internal_content_strong.string != None
						
						if is_strong and not is_time_added:
							time = internal_content_strong.string.split(":")
							if (len(time) == 3):
								cur_hronometrazh += '[[' + yout_link
								cur_hronometrazh += time[0] + "h" + time[1] + "m" + time[2] + "s"
								cur_hronometrazh += " " + time[0] + ":" + time[1] + ":" + time[2]
								cur_hronometrazh += ']]'
								
								is_time_added = True
						
						if is_last_span and len(content.split(":")) != 3:
							cur_hronometrazh += content
							
				if (cur_hronometrazh == ""):
					continue
				
				cur_hronometrazh += "\n"
				print(cur_hronometrazh)
				
				hronometrazh += "# " + cur_hronometrazh
				
			hronometrazh += "\n"
			
			out_file.write(hronometrazh) # .encode('utf-8', errors='ignore')
			out_file.close()
			
			# Выходной файл единый
			out_all_in_one_file = open('all_in_one.txt', 'a')
			out_all_in_one_file.write(hronometrazh) # .encode('utf-8', errors='ignore')
			out_all_in_one_file.close()




#<p style="text-align:justify"><span style="font-size:14px"><span style="font-family:verdana,geneva,sans-serif"><span style="font-size:12px"><a href="https://youtu.be/m8Ux0bac4Vs?t=24" style="text-decoration-line: none;"><strong>00:00:24</strong></a></span><span style="background-color:transparent; color:rgb(0, 0, 0)"> Действительно ли к Мавзолею были брошены власовские флаги во время Парада Победы в июне 1945 года. Кто такой власовец. О власовских флагах. О списке трофейных знамён, отобранных на Парад Победы, утверждённый 21 июня 1945 года.</span></span></span></p>
#<p style="text-align:justify"><span style="font-size:14px"><span style="font-family:verdana,geneva,sans-serif"><a href="https://youtu.be/ViQ8vEcxqSM?t=88" style="text-decoration-line: none;"><strong>00:01:28</strong></a><span style="background-color:transparent; color:rgb(0, 0, 0)">&nbsp;Важность проведения Парада Победы в России. О предложении вместо проведения Парада раздать деньги нуждающимся. Какие цели в отношении России преследовали Первая и Вторая мiровые войны. Триколор в истории России</span></span></span></p>


