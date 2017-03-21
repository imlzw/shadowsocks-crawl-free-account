# python 3.0 or later
import os
import re
import urllib  
import urllib.request  
data={}  
data['wd'] = '1111'  
url_values = urllib.parse.urlencode(data)  
url = "http://www.ishadowsocks.org"  
full_url = url + url_values
data = urllib.request.urlopen(url).read()
data = data.decode('UTF-8')
lines=[]
print(len(lines))
line=''
for char in data:
	if char=='\n':
		lines.append(line)
		line = ''
	else: 
		line=line+char
read = False
configs = []
index = 0
for line in lines:
	if re.search('portfolio-item', line):
		configs.append({});
		read = True
	elif re.search('img',line):
		if read:
			index=index+1
			read = False
	if read:
		match = re.search(r'.*?IP\sAddress:(.*?)id="(.*?)">(.*?)</span>.*', line)
		if match:
			configs[index]['name'] = match.group(2)
			configs[index]['ip'] = match.group(3)
			continue
		match = re.search(r"Port.*?(\d{0,10})<.*", line)		
		if match:
			configs[index]['port'] = match.group(1)
			continue		
		match = re.search(r"Password.*id.*>(\d+)</span>", line)	
		if match:
			configs[index]['password'] = match.group(1)
			continue
		match = re.search("Method:(.*?)</h4>", line)	
		if match:
			configs[index]['method'] = match.group(1)
			continue

configinfo = ""
index=0
for config in configs:
	if config:
		configinfo = configinfo + "    {\n"
		configinfo = configinfo + "      \"server\":\""+config['ip']+"\",\n"
		configinfo = configinfo + "      \"server_port\":\""+config['port']+"\",\n"
		configinfo = configinfo + "      \"password\":\""+config['password']+"\",\n"
		configinfo = configinfo + "      \"method\":\""+config['method']+"\",\n"
		configinfo = configinfo + "      \"remarks\":\""+config['name']+"\",\n"
		configinfo = configinfo + "      \"auth\":\"false\",\n"
		if index+1 < len(configs)-1:
			configinfo = configinfo + "    },\n"
		else:
			configinfo = configinfo + "    }\n"
		index=index+1
		
		
		
os.chdir('C:\Data\ProgramGreen\Shadowsocks')
if not os.path.exists('gui-config-temp.json'):
	exit(-1)
lines = open('gui-config-temp.json').readlines()
fp = open('gui-config.json','w')
for s in lines:
	fp.write( s.replace('configs_flag',configinfo))    
fp.close()

os.system("taskkill -f -t -im Shadowsocks.exe")
os.system("start c:/Data/ProgramGreen/Shadowsocks/Shadowsocks.exe")
