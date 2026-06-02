"""
Gradescope-compatible plain text format
"""

from html.parser import HTMLParser
from docx import Document


class _StripHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self):
        return ''.join(self._parts).strip()


def _strip_html(html_text):
    if not html_text:
        return ''
    parser = _StripHTML()
    parser.feed(html_text)
    return parser.get_text()


def write_file(data, outfile=None):
    lines = []
    q_num = 1

    for assessment in data['assessment']:
        for question in assessment['question']:
            q_type = question.get('question_type', '')
            q_text = _strip_html(question.get('text', ''))

            lines.append(f"{q_num}. {q_text}")

            if 'answer' in question:
                for answer in question['answer']:
                    if not answer.get('display', True):
                        continue
                    text = _strip_html(answer.get('text', ''))
                    correct = answer.get('correct', False)

                    if q_type == 'true_false_question':
                        marker = '[*]' if correct else '[ ]'
                    else:
                        marker = '[x]' if correct else '[ ]'

                    lines.append(f"{marker} {text}")

            lines.append('')
            q_num += 1

    output = '\n'.join(lines)

    if outfile:
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(output)
    else:
        print(output)


def write_docx(data, outfile):
    lines = []
    q_num = 1

    for assessment in data['assessment']:
        for question in assessment['question']:
            q_type = question.get('question_type', '')
            q_text = _strip_html(question.get('text', ''))
            lines.append(f"{q_num}. {q_text}")

            if 'answer' in question:
                for answer in question['answer']:
                    if not answer.get('display', True):
                        continue
                    text = _strip_html(answer.get('text', ''))
                    correct = answer.get('correct', False)
                    marker = '[*]' if (q_type == 'true_false_question' and correct) else ('[x]' if correct else '[ ]')
                    lines.append(f"{marker} {text}")

            lines.append('')
            q_num += 1

    doc = Document()
    for line in lines:
        doc.add_paragraph(line)
    doc.save(outfile)
