import requests
from os.path import abspath, dirname

'''
请求中的body(json)标准格式：
{
  "question": "What are levels of words?",
  "documents": [
    {
      "text": "Diction Diction is the choice and use of words. The English language has a very large vocabulary: as many as 400,000 words are collected in the Oxford English Dictionary. Of course no one knows or need to use so many words. Only a small part of them are used by ordinary people fbr ordinary purposes. Students learning to write should learn to use the words that are most useful and most often used to express themselves.",
      "id": "1"
    }
  ],
  "language": "en"
}

'''


class AnswerGenerator:
    cnt = 0

    def __init__(self, source_path: str, query: str):
        self.session = requests.Session()
        self.source_path = source_path
        self.postfix = "/qnamaker/v5.0-preview.2/generateAnswer"
        self.key = "your_key_here"
        self.content_type = "application/json"
        self.end_point = "your_end_point_here"
        self.url = self.end_point + self.postfix
        self.question = query

    def set_question(self, query):
        self.question = query

    def set_source_path(self, source_path):
        self.source_path = source_path

    def main(self):
        headers = {
            "Content-Type": self.content_type,
            "Ocp-Apim-Subscription-Key": self.key,
        }
        documents = []
        with open(self.source_path, encoding='utf-8') as f:
            input = f.read()
            paras = [input[i * 5000 : i * 5000 + 5000] for i in range(0, min(len(input)//5000 + 1, 5))]
            for i in range(len(paras)):
                documents.append({"text": paras[i], "id": str(i + 1)})

        data = {
            "question": self.question,
            "documents": documents,
            "language": "en"
        }
        print(data)

        resp = self.session.post(url=self.url, headers=headers, json=data)
        ans0 = resp.json()['answers'][0]
        AnswerGenerator.cnt += 1
        with open(f'{abspath(dirname(__file__))}/answerWeek{week}.md', 'a', encoding='utf-8') as f:
            f.write(f'## Question{AnswerGenerator.cnt}: \n' + self.question + '\n\n')
            f.write(f'**Answer{AnswerGenerator.cnt}:** \n' + ans0['answer'].replace('\n', ' ') + '\n\n')
            f.write(f"Answer start at {ans0['answerStartIndex']} and end at {ans0['answerEndIndex']}\n\n\n")
            f.write(f'**AnswerSpan{AnswerGenerator.cnt}:** \n' + ans0['answerSpan']['text'] + '\n\n')
            f.write(
                f" Answer start at {ans0['answerSpan']['startIndex']} and end at {ans0['answerSpan']['endIndex']}\n\n\n\n\n\n\n")
        print(resp.text)


if __name__ == "__main__":
    week = 1

    with open(f'{abspath(dirname(__file__))}/answerWeek{week}.md', 'w', encoding='utf-8') as f:
        f.write(f'# Week{week}\n')

    if week == 1:
        # 1
        path = abspath(dirname(__file__)) + "/par7-9.text"
        question = "What are levels of words?"
        ag = AnswerGenerator(path, question)
        ag.main()

        question = "Which is preferred in academic writing?"
        ag.set_question(question)
        ag.main()

        # 2
        path = abspath(dirname(__file__)) +  "/par37-43.text"
        ag.set_source_path(path)
        ag.set_question("What are types of sentences?")
        ag.main()

        ag.set_question("What are the meanings of different types of sentences?")
        ag.main()

        ag.set_question("how to use different types of sentences?")
        ag.main()

        # 3
        path = abspath(dirname(__file__)) + "/par64-68.text"
        ag.set_source_path(path)
        ag.set_question("What are the criteria of an effective paragraph?")
        ag.main()

        ag.set_question("What are the meanings of different criteria?")
        ag.main()

        # 4
        path = abspath(dirname(__file__)) +  "/par71-72.text"
        ag.set_source_path(path)
        ag.set_question("What are the steps in writing a paragraph?")
        ag.main()



