#main code
import requests
from bs4 import BeautifulSoup
import time
import urllib3
import json, html, base64

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.indiabix.com/aptitude/problems-on-trains/"

def scrape_page(url, topic_url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, "lxml")

    questions_data = []

    question_blocks = soup.find_all('div', class_='bix-div-container')

    for block in question_blocks:
        try:
            # Get question text
            question_tag = block.find('div', class_='bix-td-qtxt')
            question = question_tag.get_text(strip=True) if question_tag else "Question not found"

            # Get options
            options = []
            option_blocks = block.find_all('div', class_='bix-td-option-val')
            for opt in option_blocks:
                # option_text = opt.get_text(strip=True)
                # options.append(option_text)
                #new code save html with text
                option_text = opt.get_text(strip=True)
                # option_html = opt.find('div', class_='bix-td-option-val')
                #encoding html
                option_html = base64.b64encode(opt.encode('utf-8')).decode('utf-8') if opt else " "
                option_object = {'option_text':option_text,'option_html':option_html}

                options.append(option_object)


            # Get correct answer
            answer_input = block.find('input', class_='jq-hdnakq')
            answer_value = answer_input['value'].strip() if answer_input else "Answer not found"

            # Getting answer description
            # Find the div with the specified class
            ans_desc_html_content = block.find('div', class_='bix-ans-description table-responsive')

            # Now `encoded_html` is a Base64 string you can save
            encoded_html = base64.b64encode(ans_desc_html_content.encode('utf-8')).decode('utf-8') if ans_desc_html_content else " "

            # print("######",encoded_html)
            print("test", {
                'question': question,
                'options': options,
                'answer': answer_value,
                #'html_desc_answer': ans_desc_html_content,
                'topic_url': topic_url,
            })
            questions_data.append({
                'question': question,
                'options': options,
                'answer': answer_value,
                'html_desc_answer': encoded_html,
                'topic_url': topic_url,
            })
        except Exception as e:

          import traceback
          traceback.print_exc()

          print(f"Error scraping a question block: {e}")
          exit()

    return questions_data

def find_next_page(soup):
    next_link = None
    links = soup.find_all('a', class_='page-link')

    for link in links:
        span = link.find('span')
        if span and span.get_text(strip=True) == 'Next':
            next_link = link
            break

    if next_link:
        return next_link['href'] if next_link['href'].startswith('http') else 'https://www.indiabix.com' + next_link['href']
    return None


def scrape_all_pages(start_url):
    all_questions = []
    current_url = start_url

    topic_url = start_url

    while current_url:
        print(f"Scraping {current_url}")
        response = requests.get(current_url, verify=False)
        soup = BeautifulSoup(response.text, "lxml")

        page_questions = scrape_page(current_url, topic_url)
        all_questions.extend(page_questions)

        next_page_url = find_next_page(soup)
        current_url = next_page_url

        time.sleep(1)

    return all_questions

# if __name__ == "__main__":

#     data = scrape_all_pages(BASE_URL)

#     # Save to JSON
#     with open('indiabix_problems_on_trains.json', 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

#     print(f"\n✅ Scraped {len(data)} questions and saved to 'indiabix_problems_on_trains.json'")
