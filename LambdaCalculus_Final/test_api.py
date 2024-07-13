import requests

url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"

payload = {
	"messages": [
		{
			"role": "user",
			"content": "hello"
		}
	],
	"system_prompt": "",
	"temperature": 0.9,
	"top_k": 5,
	"top_p": 0.9,
	"max_tokens": 256,
	"web_access": False
}
headers = {
	"x-rapidapi-key": '7claclo62bmsh79a849643890833p127bdjsn728c70c7091f',
	"x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())