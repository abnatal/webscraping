from bs4 import BeautifulSoup

class UdemyQuestionExtractor:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def has_class_starting_with(self, item, class_start):
        if not item.has_attr('class'):
            return False
            
        for class_ in item['class']:
            if class_.startswith(class_start):
                return True
        return False

    def extract_question(self):
        question = { 'question': '', 'items': [], 'answer' : [], 'comment' : '', 'errors' : [] }

        for div in self.soup.find_all('div', {'class' : 'udlite-text-sm'}):
            if self.has_class_starting_with(div, 'alert-banner--body'):
                question['comment'] += div.text
                break

        for div in self.soup.find_all('div', id='question-prompt'):
            question['question'] += div.text

        for li in self.soup.find_all('li'):
            if self.has_class_starting_with(li, 'mc-quiz-question--answer'):
                question['items'].append(li.text)
                if li.find('input') and not li.find('input').has_attr('disabled'):
                    question['answer'].append(li.text)
        return self.validate(question)

    def validate(self, question):
        question['errors'] = []

        if len(question['items']) == 0:
            question['errors'].append('No items found!');

        if len(question['answer']) == 0:
            question['errors'].append('No answers found!');

        if len(question['answer']) > 1:
            question['errors'].append('More than one answer found! It looks like the capture was made on an incorrect answer screen!');
        return question

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        html = f.read()

    q = UdemyQuestionExtractor(html)
    print(q.extract_question())
