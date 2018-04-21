import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'research.settings')
django.setup()

from main_app.models import Author, Creation
from faker import Faker

fake = Faker()

languages = ['Монгол', 'English']

fake_profession = ['Химийн инженер', 'Нано, биотехнологийн инженер', 'Хүрээлэн буй орчны мэргэжилтэн',
                   'Үйлдвэрлэлийн автоматжуулалт', 'Барилгын инженер',
                   'Цахилгааны инженер', 'Механик инженер',
                   'Программ хангамж', 'Эмч', 'Багш', 'Цагдаа', 'Маркетингийн менежер']

fake_university = ['Анагаахын шинжлэх ухааны үндэсний их сургууль', 'Үндэсний батлан хамгаалахын их сургууль',
                   'Монгол улсын Боловсролын их сургууль', 'Монгол улсын их сургууль', 'Удирдлагын академи',
                   'Хөдөө аж ахуйн их сургууль', 'Хууль сахиулахын их сургууль',
                   'Шинжлэх ухаан, технологийн их сургууль']


def add_author():
    author = Author.objects.get_or_create(first_name=fake.first_name_female(),
                                          last_name=fake.last_name_male(),
                                          profession=random.choice(fake_profession),
                                          graduated_school=random.choice(fake_university),
                                          about=fake.paragraphs(nb=3, ext_word_list=None),
                                          rank=fake.word(ext_word_list=None))[0]
    author.save()

    return author


def populate(length=20):
    for i in range(length):
        author = add_author()

        creation = Creation.objects.get_or_create(
            author=author, title=fake.sentence(), co_authors=fake.name(),
            type=fake.job(), category=fake.word(), subclass=fake.word(), overview=fake.paragraph(nb_sentences=3),
            keyword=fake.word(), created_date=fake.date(pattern="%Y-%m-%d", end_datetime=None),
            language=random.choice(languages), price=fake.zipcode(), num_of_page=fake.zipcode(),
            uploaded_date=fake.date(pattern="%Y-%m-%d", end_datetime=None))


if __name__ == '__main__':
    populate(20)
