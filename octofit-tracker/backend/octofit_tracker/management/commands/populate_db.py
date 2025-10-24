from django.core.management.base import BaseCommand
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Eliminar datos previos
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Crear índice único en email
        db.users.create_index([("email", 1)], unique=True)

        # Datos de ejemplo
        marvel_team = {"name": "Marvel", "members": ["Iron Man", "Spider-Man", "Captain America"]}
        dc_team = {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]}
        db.teams.insert_many([marvel_team, dc_team])

        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
        ]
        db.users.insert_many(users)

        activities = [
            {"user": "Iron Man", "activity": "Running", "duration": 30},
            {"user": "Batman", "activity": "Cycling", "duration": 45},
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {"team": "Marvel", "points": 100},
            {"team": "DC", "points": 90},
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {"user": "Spider-Man", "workout": "Push-ups", "reps": 50},
            {"user": "Wonder Woman", "workout": "Squats", "reps": 40},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data'))
