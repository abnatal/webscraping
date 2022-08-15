import re
import sys
import os
from enum import Enum, auto

class ReadingStatus(Enum):
    READING_QUESTION = auto()
    READING_ITEMS = auto()     
    READING_ANSWER = auto()

def read_lines(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

def save_cvs_file(basename, questions):
    with open(basename + '.csv', 'w') as f:
        for key in questions:
            question = questions[key]
            a = '<b>' + question['question'] + '</b><br /><br />' + '<br /><br />'.join(question['items'])
            b = question['answer'].replace('.','.<br /><br />')
            f.write('"{}","{}","#imported #{}"\n'.format(a.replace('"', '""'), b.replace('"', '""'), basename))

def main(filename):
    basename, _ = os.path.splitext(filename)
    questions = {}
    for line in read_lines(filename):
        line = line.strip().strip('\r')
        if not line:
            continue

        is_question = re.match(r'^\d+\. ', line)
        if is_question:
            question_number = int(is_question.group(0).strip().strip('.'))
            if not question_number in questions:
                status = ReadingStatus.READING_QUESTION
                questions[question_number] = { 'question' : line, 'items' : [], 'answer' : '' }
            else:
                status = ReadingStatus.READING_ANSWER
                questions[question_number]['answer'] = line
            continue

        if re.match(r'^[A-Z]*\. ', line):
            status = ReadingStatus.READING_ITEMS
            questions[question_number]['items'].append(line)
            continue

        if status == ReadingStatus.READING_QUESTION:
            questions[question_number]['question'] += ' ' + line

        if status == ReadingStatus.READING_ITEMS:
            questions[question_number]['items'][-1] += ' ' + line

        if status == ReadingStatus.READING_ANSWER:
            questions[question_number]['answer'] += ' ' + line

    print(questions)
    save_cvs_file(basename, questions)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <filename>')
        sys.exit(1)

    main(sys.argv[1])
