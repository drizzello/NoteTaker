import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import certifi

"""from bs4 import BeautifulSoup
import pickle


# URL of the proxy list page
url = "https://www.socks-proxy.net/"  # Replace with the specific URL you're using

# Send a GET request to the page
response = requests.get(url)
if response.status_code == 200:
   soup = BeautifulSoup(response.content, "html.parser")
    
   # Find the table that contains proxy information
   table = soup.find("table")
    
   # Extract headers (optional)
   headers = [th.text for th in table.find_all("th")]

   # Extract table rows (IP, port, country, anonymity)
   proxies = []
   counter = 0
   for index, row in enumerate(table.find_all("tr")[1:]):
      if counter <= 20:
         counter +=1
         print(index)
         cols = row.find_all("td")
         if len(cols) > 1:
               ip_address = cols[0].text.strip()
               port = cols[1].text.strip()
               country = cols[3].text.strip()
               https = cols[6].text.strip()
               proxies.append({"IP": ip_address, "Port": port, "Country": country, "HTTPS": https})
      else:
          break
               # Convert to DataFrame
   print(proxies)
   
   with open('proxies.pkl', 'wb') as f:
      pickle.dump(proxies, f, pickle.HIGHEST_PROTOCOL)

   with open('proxies.pkl', 'rb') as f:
      map_dict = pickle.load(f)

   print("*****************")
   for i in map_dict:
      proxies = {'https': i, 'http': i}
      
   print(proxies)
   print("*****************")
   # Save to CSV file

   proxy_list = {proxy['IP']: proxy['Port'] for proxy in map_dict}
    
   for ip, port in proxy_list.items():
        #for proxy in proxy_list:
      try:
         # Prepare proxies for the request
         proxies = {'https': f"http://{ip}:{port}", 'http': f"http://{ip}:{port}"}
         response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
         if response.status_code == 200:
            print("Proxy is working!")
      except Exception as e:
         print(e)
   print("Proxy list updated and saved as proxies.pkl!")
else:
   print(f"Failed to access the page. Status code: {response.status_code}")
"""


"""response = requests.get(
    "https://www.youtube.it",
    proxies={
        "http": "http://16947ba98ee240fe8630f7ac961a41bc:@api.zyte.com:8011/",
        "https": "http://16947ba98ee240fe8630f7ac961a41bc:@api.zyte.com:8011/",
    },
    verify='/Users/daviderizzello/Downloads/zyte-ca.crt' 
)
print(response.text)
"""
"""# Test the proxy
try:
    response = requests.get("https://www.youtube.com/", proxies=proxy, timeout=10)
    if response.status_code == 200:
        print("Proxy is working!")
    else:
        print(f"Proxy responded with status code: {response.status_code}")
except Exception as e:
    print(f"Proxy test failed: {e}")
"""


# Create a requests.Session object
session = requests.Session()

# Set the certificate for HTTPS verification
session.verify = "/Users/daviderizzello/Downloads/zyte-ca.crt"
"""

# Set the proxies
proxies = {
    "http": "http://16947ba98ee240fe8630f7ac961a41bc:@api.zyte.com:8011/",
    "https": "http://16947ba98ee240fe8630f7ac961a41bc:@api.zyte.com:8011/",
}


# Test the session by making a GET request
#response = session.get("https://www.youtube.it")
#print(response.text)

# Fetch YouTube transcript using the configured session
formatter = TextFormatter()
transcript = YouTubeTranscriptApi.get_transcript("FYc209d7LTo", languages=['it'], proxies=proxies)


# Format the transcript if needed
# transcript = YouTubeTranscriptApi.get_transcript("FYc209d7LTo", languages=['it'], proxies=proxies)
formatted_text = formatter.format_transcript(transcript)

print(formatted_text)
