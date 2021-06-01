import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from posts import models as post_models
from comments import models as comment_models

NAME = "comments"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many {NAME} do you want?",
        )

    def handle(self, *args, **options):
        number = options.get("number")

        all_users = user_models.User.objects.all()
        all_posts = post_models.Post.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            comment_models.Comment,
            number,
            {
                "post_name": lambda x: random.choice(all_posts),
                "author_name": lambda x: random.choice(all_users),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
