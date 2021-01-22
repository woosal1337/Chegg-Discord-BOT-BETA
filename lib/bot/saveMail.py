from simplegmail import Gmail
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime as dt
from os import path, mkdir


def create_folder(q_id):
    try:
        mkdir(q_id)
    except FileExistsError:
        pass


def extract_link(plain_message):
    message_list = plain_message.split(
        '\n')
    link = message_list[1][:-1]
    return link


def find_question_id(question_link):
    l_splitted = question_link
    l_splitted_check = question_link
    if l_splitted_check != l_splitted:
        return False
    trackid_index = l_splitted.rfind("?trackid")
    l_pure = l_splitted[:trackid_index]
    reverse_l_pure = l_pure[::-1]
    reverse_l_pure_q_index = reverse_l_pure.find("q")
    reverse_q_id = l_pure[::-1][:reverse_l_pure_q_index + 1]
    q_id = reverse_q_id[::-1]
    return q_id

class SaveMail:
    def __init__(self):
        self.start = dt.now()
        self.download_mail()

    def download_mail(self):
        gmail = Gmail()
        messages = gmail.get_unread_inbox()
        if len(messages) > 0:
            msg = messages[0]
            link = extract_link(msg.plain)
            q_id = find_question_id(link)
            create_folder(f"downloads\\{q_id}")
            full_path = path.abspath(f"downloads\\{q_id}")
            soup = BeautifulSoup(msg.html, 'html.parser')
            imgs = soup.find_all('img')
            urls = [img['src'] for img in imgs]
            for i in range(1, len(urls) - 1):
                url = urls[i]
                name = f"{full_path}/image{i}.png"
                res = get(url)
                file = open(name, "wb")
                file.write(res.content)

            f = open(f"{full_path}\\plain.txt", "a", encoding="utf-8")
            f.write("".join(msg.plain.split("\n")[1:-13]))
            f.close()
            msg.mark_as_read()
            print(dt.now() - self.start)
        else:
            pass