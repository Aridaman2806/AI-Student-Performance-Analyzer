import google.generativeai as genai
genai.configure(api_key="AIzaSyD7XxcyJY-0A1EFyUafoPqymWPuAzMoBbQ")
for m in genai.list_models():
    print(m.name)