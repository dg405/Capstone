import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_init_records, db_drop_and_create_all, Actor, Movie, Performance, db_commit, associationupdate
import datetime

casting_assistant_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpxRmc2M2JzOTFTcmlkRjYyQnh6VyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZWRhbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTMwNjgzNjkxNDY1MTg4Nzg5NTciLCJhdWQiOlsiY2FwIiwiaHR0cHM6Ly9jb2ZmZWVkYW4uZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MjQ5OTI3OSwiZXhwIjoxNTkyNTg1Njc5LCJhenAiOiJiUU1TakxMZ3NJa3lKU29aTVpOTGJOMm1yVG5NVjRSNiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.TuFm2VwEPNwyBKewzbG0kJ0pZZGUvYkviyPQDG0qhlUkspAUkj8FDQUIR2hDSQ7o_17hnhj9kSrDTeTXYX1gCxII1neGyO8mPi_GUSIiFynkilSPXGlYtUimQqDJQ8-N5qGFwlR4Y4WkkEtuso_QkyY8EdNcNFi3gwc0Fczl498FtzM17qdKzo-qDrk_Zn05ETkh2yusLB3lH7LvIjCgIfiA13TFrSFCu8hxpfs00fq1Xg3CSrC0GcUipHCJ3WFlG5eyooVBi56QYhVvUphB_PPlBMrCNGHBjBK-OZkL5At-aDetK57wf8Ecth45kfBgcvojoD3Vl_yO_MtlOnWtTg'
casting_director_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpxRmc2M2JzOTFTcmlkRjYyQnh6VyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZWRhbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTMxMTk0ODYzNTAwODA0ODk5ODgiLCJhdWQiOlsiY2FwIiwiaHR0cHM6Ly9jb2ZmZWVkYW4uZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MjQ5OTM1OCwiZXhwIjoxNTkyNTg1NzU4LCJhenAiOiJiUU1TakxMZ3NJa3lKU29aTVpOTGJOMm1yVG5NVjRSNiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.jkcAUP2gO7teZk0E7f1CH2_mPnewoQGaiN80IzsM7mcMk_xXAbyfarph8mAUU9wS_SIrgFDejY3CppSsuOYc6fQflBJRz1I3iwoMgX3x4NlXAHdViuuFjG3gTDUJYILAmoxpZ89CFQxT9B2CTEK_EkW-kpgpXg_WTlPpnMCVysX2n03MQNvf0v7PH10TLEVycZqipRge9aVRVVwBaXQZutWQqmDhUbU0yrej_Rh5sm4yMBruKsJL9XylgiH3UqDm85sbewODGmVjndI3VAYgESr1--GdS0MbJXH0QZVXgtEIWP3mMP4EIUzq2R3v0LbiovDGVvYEn1hKFR2svGcn7g'
executive_producer_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpxRmc2M2JzOTFTcmlkRjYyQnh6VyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZWRhbi5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTM3NDMyODMzNTQ1NjMyODMyOTciLCJhdWQiOlsiY2FwIiwiaHR0cHM6Ly9jb2ZmZWVkYW4uZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MjQ5OTQwNiwiZXhwIjoxNTkyNTg1ODA2LCJhenAiOiJiUU1TakxMZ3NJa3lKU29aTVpOTGJOMm1yVG5NVjRSNiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.yYdTWhAAU1GMy8Qn4MzuYJTxo2luPXj7Xki-pKmaMUiZOp8J8ty8zj-DpGXgYkHRg67c7Jp9VlASa9_CnR1KYMIUJsmQn6RF9eHrsjIoUCT90HFk85y-QVBJWNu-_thbOLb-TvwyChYkkLpMR5xO65Oy0eQSIVjSV3zP3K9Tp3DQ0NATNVXk1Wo6A6wZTdDK-uGVTaARNhaflDfVkUp4sL2B0Fmw2wmyn7JggGNaXuXrsdjqJsY-F-E8X1CsxY_pDKs6__8F_WqDg4U8k0DAqkjNvHoScrSnnz7HLkb45Nq-gxB8zn5zXpO_qhw86_2eMLefloDLwzNjYU0RK7m8iQ'


class CapTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://postgres:password@localhost:5432/agencytest'
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        db_init_records()

        self.new_actor = {
            'name': 'Danny',
            'gender': 'Male',
            'age': 43
        }

        self.new_movie = {
            'title': 'Batman',
            'release_date': '2020-06-12',
            'actor_id': [1]
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        selection = Movie.query.filter(Movie.title == 'Batman').all()
        for movie in selection:
            movie.delete()
        selection = Actor.query.filter(Actor.name == 'Danny').all()
        for actor in selection:
            actor.delete()
        pass

    '''
    Successful Behaviour of each enpoint
    '''

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                'Authorization': executive_producer_token})

        data = res.get_json()

        selection = Actor.query.all()
        self.assertEqual(data['status'], True)
        self.assertEqual(res.status_code, 200)

    def test_post_actor(self):
        tlength = Actor.query.all()

        res = self.client().post(
            '/actors',
            headers={
                'Authorization': executive_producer_token},
            json=self.new_actor)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(Actor.query.all()), len(tlength))

    def test_patch_actor(self):
        actor = Actor(
            name='Dan',
            age=83,
            gender='Male'
        )

        actor.id = 888
        actor.insert()

        res = self.client().patch(
            '/actors/888',
            headers={
                'Authorization': executive_producer_token},
            json={
                "name": "Donny"})

        self.assertEqual(res.status_code, 200)
        actor.delete()

    def test_delete_actor(self):
        actor = Actor(
            name='Joey Tribiani',
            age=30,
            gender='Male'
        )

        actor.id = 100
        actor.insert()

        res = self.client().delete('/actors/100', headers={
            'Authorization': executive_producer_token}
        )

        self.assertEqual(res.status_code, 200)

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                'Authorization': executive_producer_token})

        data = res.get_json()

        selection = Movie.query.all()
        self.assertEqual(data['status'], True)
        self.assertEqual(res.status_code, 200)

    def test_post_movie(self):
        tlength = Movie.query.all()

        res = self.client().post(
            '/movies',
            headers={
                'Authorization': executive_producer_token},
            json=self.new_movie)

        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(Movie.query.all()), len(tlength))

    def test_patch_movie(self):
        movie = Movie(
            title='titanic',
            release_date='2018-01-02',
            actor_id=[2]
        )

        movie.id = 888
        movie.insert()

        res = self.client().patch(
            '/movies/888',
            headers={
                'Authorization': executive_producer_token},
            json={
                "title": "American Pie"})

        self.assertEqual(res.status_code, 200)
        movie.delete()

    def test_delete_movie(self):
        movie = Movie(
            title='titanic',
            release_date='2018-01-02',
            actor_id=[2]
        )

        movie.id = 100
        movie.insert()

        res = self.client().delete('/movies/100', headers={
            'Authorization': executive_producer_token}
        )

        self.assertEqual(res.status_code, 200)

    '''
    Error Behaviour of each enpoint
    '''

    def test_get_actors_404(self):
        db_drop_and_create_all()
        res = self.client().get(
            '/actors',
            headers={
                'Authorization': executive_producer_token})

        self.assertEqual(res.status_code, 404)

    def test_get_movies_404(self):
        db_drop_and_create_all()
        res = self.client().get(
            '/movies',
            headers={
                'Authorization': executive_producer_token})

        self.assertEqual(res.status_code, 404)
        db_init_records()

    def test_post_actor_400(self):
        res = self.client().post(
            '/actors',
            headers={
                'Authorization': executive_producer_token},
            json={})

        self.assertEqual(res.status_code, 400)

    def test_post_movie_400(self):
        res = self.client().post(
            '/movies',
            headers={
                'Authorization': executive_producer_token},
            json={})

        self.assertEqual(res.status_code, 400)

    def test_patch_actor_422(self):
        res = self.client().patch(
            '/actors/888',
            headers={
                'Authorization': executive_producer_token},
            json={
                "name": "Donny"})

        self.assertEqual(res.status_code, 422)

    def test_patch_movie_422(self):

        res = self.client().patch(
            '/movies/888',
            headers={
                'Authorization': executive_producer_token},
            json={
                "title": "American Pie"})

        self.assertEqual(res.status_code, 422)

    def test_delete_actor_404(self):

        res = self.client().delete('/actors/1000', headers={
            'Authorization': executive_producer_token}
        )

        self.assertEqual(res.status_code, 404)

    def test_delete_movie_404(self):

        res = self.client().delete('/movies/1000', headers={
            'Authorization': executive_producer_token}
        )

        self.assertEqual(res.status_code, 404)

    '''
    RBAC Tests
    '''

    def casting_assistant_auth_success(self):
        res = self.client().get(
            '/actors',
            headers={
                'Authorization': casting_assistant_token})

        self.assertEqual(res.status_code, 200)

    def casting_assistant_auth_fail(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': casting_assistant_token}
        )

        self.assertEqual(res.status_code, 401)

    def casting_director_auth_success(self):
        res = self.client().get(
            '/actors',
            headers={
                'Authorization': casting_director_token})

        self.assertEqual(res.status_code, 200)

    def casting_director_auth_fail(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': casting_director_token}
        )

        self.assertEqual(res.status_code, 401)

    def executive_producer_auth_success(self):
        res = self.client().get(
            '/actors',
            headers={
                'Authorization': casting_director_token})

        self.assertEqual(res.status_code, 200)

    def executive_producer_auth_success_2(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': casting_director_token}
        )

        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
