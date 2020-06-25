import os
import sys
import shutil
import re
import urllib.request, urllib.error, urllib.parse
import string
from ctypes import windll
num_errors = 0

#	Saving original URL to variable
#	-------------------------------
original_file_url = "blank"
link_list = []
number_of_links = 1
while original_file_url != "":
	original_file_url = str(input("Enter URL #" + str(number_of_links) + ": ")) 	#Get URL from user
	if original_file_url != "":
		number_of_links += 1
		link_list.append(original_file_url) 	#Add current URL to list
#link_list = ["https://www.literotica.com/s/sounds-good-ch-03","https://www.literotica.com/s/a-fragile-cup-of-witchs-brew"] #Pre-setting the links
print("All the URLs" + str(link_list))

for original_file_url in link_list:
	try:
		#print("Original file URL is PRESET")
		#original_file_url = "https://www.literotica.com/s/not-quite-a-white-knight-bk-02-pt-03"
		#original_file_url = "https://www.literotica.com/s/quarantine-stinks"


		print("The original file URL is ", original_file_url)


		#	Parsing original web page
		#	-------------------------
		url_response = urllib.request.urlopen(original_file_url)
		original_web_page = url_response.read().decode("utf-8")

		#	Display the Original Web Page
		#	-----------------------------
		#print(original_web_page)

		#	Save content to file
		#	----------------------
		
		#f = open('obo-t17800628-33.html', 'wb')
		#f.write(webContent)
		#f.close
		

		#	Calculate page number
		#	--------------------------
		page_number_position_left = int(original_web_page.find('<!-- x -->'))+10
		page_number_position_right = int(original_web_page.find(' Pages:'))
		#print(page_number_position_left, ', ', page_number_position_right)
		page_number = int(original_web_page[page_number_position_left:page_number_position_right])
		print(page_number, " page(s)")

		#	Find Story Name
		#	--------------------------
		story_name_position_left = int(original_web_page.find('<title>'))+7
		story_name_position_right = int(original_web_page.find(' - Literotica.com'))
		#print(story_name_position_left, ', ', story_name_position_right)
		#story_name = str(original_web_page[story_name_position_left:story_name_position_right]).encode("utf-8").replace("\xc3\xa0", "a").replace("\\'","'").replace("/","-").replace(":","-").replace("\\","-")
		story_name = original_web_page[story_name_position_left:story_name_position_right].replace("\\'","'").replace("/","-").replace(":","-").replace("\\","")
		print(story_name)


		#	Download all the pages
		#	----------------------
		print("Downloading...")
		current_page = 0
		combined_web_pages = ''

		while (current_page < page_number):
			current_page += 1
			current_page_url = original_file_url + "?page=" + str(current_page) #create current page URL
			url_response = urllib.request.urlopen(current_page_url) #parse current web page
			current_web_page = url_response.read().decode("utf-8")
			
			current_page_content_position_left = int(current_web_page.find('<div class="b-story-body-x x-r15">'))
			current_page_content_position_right = int(current_web_page.find('<div class="b-story-stats-block">'))
			combined_web_pages += current_web_page[current_page_content_position_left:current_page_content_position_right]
			#combined_web_pages += current_web_page

		#	Process final string
		#	--------------------
		combined_web_pages = ('<html>\n<head>\n<meta charset="UTF-8">\n<title>' + story_name + '</title>\n</head>\n<body>\n<h1>' + story_name + '</h1>\n' + combined_web_pages.replace('\\n', '\n').replace("\\'","'").replace('\\t', '\t') + '\n</body>\n</html>')

		#	Save all pages as *.txt file
		#	----------------------------
		f = open(story_name + '.txt', 'wt', encoding="utf-8")
		f.write(combined_web_pages)
		f.close()

		#	Move file to Kindle
		#	-------------------
		kindle_drive_letter = ""
		for d in string.ascii_uppercase:
			if os.path.isfile(d + ':/system/version.txt'):
				kindle_drive_letter = d
				#print(d)
		print("Kindle on " + kindle_drive_letter + ":/")
		print("Moving file...")
		shutil.move(story_name + '.txt', kindle_drive_letter + ':/documents/' + story_name + '.txt')

		#	Conclusion Message
		#	------------------
		print("----")
		print("STORY DOWNLOAD COMPLETE")
		print("----")
	except Exception as e:
		print("----")
		print("ERROR DOWNLOADING THE STORY \"" + original_file_url + "\"")
		print (e)
		print("----")
		num_errors += 1
		pass
print("---------------------------------")
print("ALL DOWNLOADS COMPLETE - " + str(num_errors) + " ERROR(S)")
print("---------------------------------")
os.system("pause >nul")