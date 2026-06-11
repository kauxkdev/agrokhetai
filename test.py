import google.generativeai as genai
genai.configure(api_key="AQ.Ab8RN6IUDgB3qrRF275wAbeuv-u8zGqrsKVdpvZ2rKbqrN0SoA")
model= genai.GenerativeModel("gemini-2.5-flash")
response=model.generate_content("hello")
print(response.text)