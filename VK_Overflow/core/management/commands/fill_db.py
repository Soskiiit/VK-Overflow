from datetime import datetime
from random import choice, randint

from django.core.management.base import BaseCommand

from questions.models import Answer, Question, QuestionGrade, Tag
from users.models import User


class Command(BaseCommand):
    help = 'Creates many records in database.'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Data count ratio')

    def handle(self, *args, **options):
        ratio = options['ratio']
        assert ratio >= 20, 'Use at least 20 ratio'

        users_count = ratio
        tags_count = ratio
        questions_count = 10 * ratio
        answers_count = 100 * ratio
        grades_count = 200 * ratio
        batch_size = 1000

        total_start = datetime.now()

        # Users
        start = datetime.now()
        users_to_create = [
            User(
                username=f'User {i}',
                email=f'email{i}@meow.meow',
                password='easy_password',
            ) for i in range(users_count)
        ]
        User.objects.bulk_create(users_to_create, batch_size)
        users = list(User.objects.values_list('id', flat=True))
        print(f'{users_count} users was created in {datetime.now() - start}')

        # Tags
        start = datetime.now()
        tags_to_create = [
            Tag(
                name=f'Tag {i}',
                color='grey'
            ) for i in range(tags_count)
        ]
        Tag.objects.bulk_create(tags_to_create, batch_size)
        tags = list(Tag.objects.values_list('id', flat=True))
        print(f'{tags_count} tags was created in {datetime.now() - start}')

        # Questions
        start = datetime.now()
        questions_to_create = []
        for i in range(questions_count):
            questions_to_create.append(Question(
                title=f'Question {i}',
                author_id=choice(users),
                question_text='How to bla-bla-bla?',
            ))

        Question.objects.bulk_create(questions_to_create, batch_size)
        questions = list(Question.objects.values_list('id', flat=True))
        print(f'{questions_count} questions was created in {datetime.now() - start}')

        # Вяжем теги к вопросам, в угоду производительности приходится сильно изощряться
        start = datetime.now()

        ThroughModel = Question.tags.through
        relations_to_create = []
        unique_relations = set()

        for question_id in questions:
            num_tags = randint(1, 3)
            tags_for_this_question = [choice(tags) for _ in range(num_tags)]

            for tag_id in tags_for_this_question:
                # Проверяем на уникальность
                if (question_id, tag_id) not in unique_relations:
                    relations_to_create.append(
                        ThroughModel(question_id=question_id, tag_id=tag_id)
                    )
                    unique_relations.add((question_id, tag_id))

        ThroughModel.objects.bulk_create(relations_to_create, ignore_conflicts=True)
        print(f'Tags for questions was created in {datetime.now() - start}')

        # Answers
        start = datetime.now()
        answers_to_create = [
            Answer(
                author_id=choice(users),
                question_id=choice(questions),
                answer_text='bla-bla-bla',
            ) for i in range(answers_count)
        ]
        Answer.objects.bulk_create(answers_to_create, batch_size)
        print(f'{answers_count} answers was created in {datetime.now() - start}')

        start = datetime.now()
        grades_to_create = [
            QuestionGrade(
                author_id=i,
                question_id=question_id,
                grade=choice((-1, 1))
            ) for i in range(1, 21)
            for question_id in questions
        ]
        QuestionGrade.objects.bulk_create(grades_to_create, batch_size)
        print(f'{grades_count} grades was created in {datetime.now() - start}')

        self.stdout.write(self.style.SUCCESS(
            f'All data was created successfully in {datetime.now() - total_start}'
        ))
