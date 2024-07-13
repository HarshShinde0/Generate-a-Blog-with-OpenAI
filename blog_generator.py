import openai
import os
import logging
from dotenv import dotenv_values
import configparser

# Setup logging
logging.basicConfig(level=logging.INFO, filename='blog_generator.log',
          format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from .env and config.ini
config_path = dotenv_values('.env')['CONFIG_FILE']
config = configparser.ConfigParser()
config.read(config_path)

# Set API key
openai.api_key = config['openai']['api_key']

def generate_blog(paragraph_topic):
  try:
    response = openai.Completion.create(
      model='gpt-3.5-turbo-instruct',
      prompt=f'Write a paragraph about the following topic: {paragraph_topic}',
      max_tokens=400,
      temperature=0.3
    )
    retrieve_blog = response.choices[0].text.strip()
    return retrieve_blog
  except Exception as e:
    logging.error(f"Error generating blog: {e}")
    return "An error occurred while generating the blog. Please try again."

def main():
  paragraphs = []
  keep_writing = True

  while keep_writing:
    answer = input('Write a paragraph? (Y for yes, anything else for no): ').strip()
    if answer.upper() == 'Y':
      paragraph_topic = input('What should this paragraph talk about? ').strip()
      paragraph = generate_blog(paragraph_topic)
      print(f"\nGenerated Paragraph:\n{paragraph}\n")
      paragraphs.append(paragraph)
    else:
      keep_writing = False

  save_to_file = input('Do you want to save the generated paragraphs to a file? (Y for yes, anything else for no): ').strip()
  if save_to_file.upper() == 'Y':
    with open('generated_blogs.txt', 'w') as file:
      for idx, para in enumerate(paragraphs, start=1):
        file.write(f"Paragraph {idx}:\n{para}\n\n")
    logging.info("Generated paragraphs saved to generated_blogs.txt")
    print("Paragraphs saved to generated_blogs.txt")

if __name__ == "__main__":
  main()