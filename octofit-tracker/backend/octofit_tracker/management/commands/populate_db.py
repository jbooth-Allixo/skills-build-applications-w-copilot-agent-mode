from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            User(id=1, email='thundergod@mhigh.edu', name='Thor', password='thundergodpassword'),
            User(id=2, email='metalgeek@mhigh.edu', name='Tony Stark', password='metalgeekpassword'),
            User(id=3, email='zerocool@mhigh.edu', name='Steve Rogers', password='zerocoolpassword'),
            User(id=4, email='crashoverride@mhigh.edu', name='Natasha Romanoff', password='crashoverridepassword'),
            User(id=5, email='sleeptoken@mhigh.edu', name='Bruce Banner', password='sleeptokenpassword'),
        ]
        User.objects.bulk_create(users)

        # Create teams
        team = Team(id=1, name='Avengers')
        team.save()
        team.members.add(*users)

        # Create activities
        activities = [
            Activity(id=1, user=users[0], type='Cycling', duration=60),
            Activity(id=2, user=users[1], type='Crossfit', duration=120),
            Activity(id=3, user=users[2], type='Running', duration=90),
            Activity(id=4, user=users[3], type='Strength', duration=30),
            Activity(id=5, user=users[4], type='Swimming', duration=75),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(id=1, team=team, points=500),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(id=1, name='Cycling Training', description='Training for a road cycling event'),
            Workout(id=2, name='Crossfit', description='Training for a crossfit competition'),
            Workout(id=3, name='Running Training', description='Training for a marathon'),
            Workout(id=4, name='Strength Training', description='Training for strength'),
            Workout(id=5, name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))