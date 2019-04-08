from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3

def setUp():
	browser = webdriver.Firefox()
	content = browser.get('http://bit.ly/top-mba-18')
	#To close popup window
	wait = WebDriverWait(browser, 15)
	element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tm-register-emba-modal"]/div/div/div/a')))
	browser.find_element_by_xpath('//*[@id="tm-register-emba-modal"]/div/div/div/a').click()
	return browser

def fetchProgHighlights(linkValue,browser):
	prog = []
	browser.get(linkValue)	#instead of get method wanted to run execute_script method but not done at this point of time.
	progLink =  browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[3]/div[1]/div/div/div[7]')
	data = progLink.find_elements_by_class_name('data')
	for l in range(len(data)):
		prog.append(data[l].text)
		print(prog)
		browser.back()
		wait = WebDriverWait(browser, 15)
		element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tm-register-emba-modal"]/div/div/div/a')))
		browser.find_element_by_xpath('//*[@id="tm-register-emba-modal"]/div/div/div/a').click()
	return 

def databaseSetUp(data):
	conn = sqlite3.connect('scrape.db')
	c = conn.cursor()

	c.execute('''CREATE TABLE IF NOT EXISTS University(rank TEXT,nameOfUniversity TEXT,nameOfCourse TEXT,linkProgHighlight TEXT,city TEXT,country TEXT)''')

	c.execute('''CREATE TABLE IF NOT EXISTS ProgramHighlights(startMonth TEXT,classSize TEXT,avgWorkExp TEXT,avgStudentAge TEXT,intlStudent TEXT,womenStudent TEXT,avgSalary TEXT,scholarship TEXT,accreditations TEXT)''')
	print(data)

	for i in data:
	       c.execute("INSERT INTO University (rank,nameOfUniversity,nameOfCourse,linkProgHighlight,city,country) VALUES (?, ?, ?, ?, ?, ?)",i);
	       print(i)

	conn.commit()
	conn.close()
	return 
	

def getUniversityData(browser):
	numOfPage = int(browser.find_element_by_xpath('//*[@id="qs-rankings_paginate"]/span/a[5]').text)
	data=[]
	for i in range(numOfPage):
		row = browser.find_element_by_xpath('//*[@id="qs-rankings"]/tbody')
		tr = row.find_elements_by_tag_name('tr')
		for j in range(len(tr)):
			rowData =[]
			td = tr[j].find_elements_by_tag_name('td')
			for k in range(4):
				if k == 1:
					nameCourse = (td[k].text).split('\n')
					nameCourse.remove('More')
					rowData.append(nameCourse[0])
					rowData.append(nameCourse[1])
					link = td[k].find_element_by_class_name('more')
					rowData.append(link.get_attribute('href'))
					#fetchProgHighlights(link.get_attribute('href'),browser)
					
				else:
					rowData.append(td[k].text)			
			data.append(rowData)
		if(i==4):
			break
		outer_pages = browser.find_element_by_xpath('//*[@id="qs-rankings_paginate"]/span/a['+str(i+2)+']').click()	
	return data

def main():
	browser = setUp()
	data = getUniversityData(browser)
	browser.quit()
	databaseSetUp(data)
	
if __name__ == "__main__":
    main()

