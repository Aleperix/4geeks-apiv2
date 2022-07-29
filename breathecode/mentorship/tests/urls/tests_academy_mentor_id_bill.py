"""
This file just can contains duck tests refert to AcademyInviteView
"""
from datetime import timedelta
import hashlib
import random
from unittest.mock import MagicMock, call, patch
from django.urls.base import reverse_lazy
from rest_framework import status
from breathecode.utils.datetime_interger import duration_to_str

from breathecode.utils.api_view_extensions.api_view_extension_handlers import APIViewExtensionHandlers
from ..mixins import MentorshipTestCase
from django.utils import timezone

UTC_NOW = timezone.now()


def format_datetime(self, date):
    if date is None:
        return None

    return self.bc.datetime.to_iso_string(date)


def get_serializer(self, mentorship_bill, mentor_profile, mentorship_service, user, data={}):
    return {
        'created_at': format_datetime(self, mentorship_bill.created_at),
        'ended_at': format_datetime(self, mentorship_bill.ended_at),
        'id': mentorship_bill.id,
        'mentor': {
            'booking_url': mentor_profile.booking_url,
            'id': mentor_profile.id,
            'service': {
                'allow_mentee_to_extend':
                mentorship_service.allow_mentee_to_extend,
                'allow_mentors_to_extend':
                mentorship_service.allow_mentors_to_extend,
                'duration':
                self.bc.datetime.from_timedelta(mentorship_service.duration),
                'id':
                mentorship_service.id,
                'language':
                mentorship_service.language,
                'max_duration':
                self.bc.datetime.from_timedelta(mentorship_service.max_duration),
                'missed_meeting_duration':
                self.bc.datetime.from_timedelta(mentorship_service.missed_meeting_duration),
                'name':
                mentorship_service.name,
                'slug':
                mentorship_service.slug,
                'status':
                mentorship_service.status,
            },
            'slug': mentor_profile.slug,
            'status': mentor_profile.status,
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'id': user.id,
                'last_name': user.last_name,
            },
        },
        'overtime_minutes': float(mentorship_bill.overtime_minutes),
        'paid_at': format_datetime(self, mentorship_bill.ended_at),
        'reviewer': {
            'email': user.email,
            'first_name': user.first_name,
            'id': user.id,
            'last_name': user.last_name,
        },
        'started_at': format_datetime(self, mentorship_bill.ended_at),
        'status': mentorship_bill.status,
        'total_duration_in_hours': float(mentorship_bill.total_duration_in_hours),
        'total_duration_in_minutes': float(mentorship_bill.total_duration_in_minutes),
        'total_price': float(mentorship_bill.total_price),
        **data,
    }


# def post_serializer(data={}):
#     return {
#         'accounted_duration': None,
#         'agenda': None,
#         'allow_billing': False,
#         'bill': None,
#         'ended_at': None,
#         'ends_at': None,
#         'id': 1,
#         'is_online': False,
#         'latitude': None,
#         'longitude': None,
#         'mentee': None,
#         'mentee_left_at': None,
#         'mentor': 1,
#         'mentor_joined_at': None,
#         'mentor_left_at': None,
#         'name': None,
#         'online_meeting_url': None,
#         'online_recording_url': None,
#         'started_at': None,
#         'starts_at': None,
#         'status': 'PENDING',
#         'summary': None,
#         **data,
#     }


def post_serializer(self, mentor_profile, mentorship_service, user, data={}):
    nxt_mnth = UTC_NOW.replace(day=28, hour=23, minute=59, second=59, microsecond=999999) + timedelta(days=4)
    ended_at = (nxt_mnth - timedelta(days=nxt_mnth.day))

    return {
        'created_at': format_datetime(self, UTC_NOW),
        'ended_at': format_datetime(self, ended_at),
        'id': 0,
        'mentor': {
            'booking_url': mentor_profile.booking_url,
            'id': mentor_profile.id,
            'service': {
                'allow_mentee_to_extend':
                mentorship_service.allow_mentee_to_extend,
                'allow_mentors_to_extend':
                mentorship_service.allow_mentors_to_extend,
                'duration':
                self.bc.datetime.from_timedelta(mentorship_service.duration),
                'id':
                mentorship_service.id,
                'language':
                mentorship_service.language,
                'max_duration':
                self.bc.datetime.from_timedelta(mentorship_service.max_duration),
                'missed_meeting_duration':
                self.bc.datetime.from_timedelta(mentorship_service.missed_meeting_duration),
                'name':
                mentorship_service.name,
                'slug':
                mentorship_service.slug,
                'status':
                mentorship_service.status,
            },
            'slug': mentor_profile.slug,
            'status': mentor_profile.status,
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'id': user.id,
                'last_name': user.last_name,
            },
        },
        'overtime_minutes': 0,
        'paid_at': None,
        'reviewer': None,
        'started_at': format_datetime(self, UTC_NOW),
        'status': 'DUE',
        'total_duration_in_hours': 0.0,
        'total_duration_in_minutes': 0.0,
        'total_price': 0.0,
        **data,
    }


def mentorship_bill_columns(data={}):
    nxt_mnth = UTC_NOW.replace(day=28, hour=23, minute=59, second=59, microsecond=999999) + timedelta(days=4)
    ended_at = (nxt_mnth - timedelta(days=nxt_mnth.day))

    return {
        'id': 0,
        'status': 'DUE',
        'status_mesage': None,
        'total_duration_in_minutes': 0.0,
        'total_duration_in_hours': 0.0,
        'total_price': -0.0,
        'overtime_minutes': 0.0,
        'academy_id': 0,
        'started_at': UTC_NOW,
        'ended_at': ended_at,
        'reviewer_id': None,
        'mentor_id': 0,
        'paid_at': None,
        **data,
    }


def get_base_number() -> int:
    return 1 if random.random() < 0.5 else -1


def append_delta_to_datetime(date):
    return date + timedelta(minutes=random.randint(0, 180))


class AcademyServiceTestSuite(MentorshipTestCase):
    """
    🔽🔽🔽 Auth
    """

    def test__post__without_auth(self):
        url = reverse_lazy('mentorship:academy_mentor_id_bill', kwargs={'mentor_id': 1})
        response = self.client.post(url)

        json = response.json()
        expected = {
            'detail': 'Authentication credentials were not provided.',
            'status_code': status.HTTP_401_UNAUTHORIZED,
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test__post__without_academy_header(self):
        model = self.bc.database.create(user=1)

        self.bc.request.authenticate(model.user)

        url = reverse_lazy('mentorship:academy_mentor_id_bill', kwargs={'mentor_id': 1})
        response = self.client.post(url)

        json = response.json()
        expected = {
            'detail': "Missing academy_id parameter expected for the endpoint url or 'Academy' header",
            'status_code': 403,
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    🔽🔽🔽 POST capability
    """

    def test__post__without_capabilities(self):
        model = self.bc.database.create(user=1)

        self.bc.request.set_headers(academy=1)
        self.bc.request.authenticate(model.user)

        url = reverse_lazy('mentorship:academy_mentor_id_bill', kwargs={'mentor_id': 1})
        response = self.client.post(url)

        json = response.json()
        expected = {
            'detail': "You (user: 1) don't have this capability: crud_mentorship_bill for academy 1",
            'status_code': 403,
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    🔽🔽🔽 POST without data
    """

    def test__post__without_data(self):
        model = self.bc.database.create(user=1, role=1, capability='crud_mentorship_bill', profile_academy=1)

        self.bc.request.set_headers(academy=1)
        self.bc.request.authenticate(model.user)

        url = reverse_lazy('mentorship:academy_mentor_id_bill', kwargs={'mentor_id': 1})
        response = self.client.post(url)

        json = response.json()
        expected = {'detail': 'not-found', 'status_code': 404}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.bc.database.list_of('mentorship.MentorshipBill'), [])

    """
    🔽🔽🔽 POST with one MentorProfile, without MentorshipSession
    """

    def test__post__with_one_mentor_profile(self):
        model = self.bc.database.create(user=1,
                                        role=1,
                                        capability='crud_mentorship_bill',
                                        mentor_profile=1,
                                        profile_academy=1)

        self.bc.request.set_headers(academy=1)
        self.bc.request.authenticate(model.user)

        url = reverse_lazy('mentorship:academy_mentor_id_bill', kwargs={'mentor_id': 1})
        response = self.client.post(url)

        json = response.json()
        expected = []

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.bc.database.list_of('mentorship.MentorshipBill'), [])

    """
    🔽🔽🔽 POST with one MentorProfile, with MentorshipSession, many cases where bill was created
    """

    @patch('django.utils.timezone.now', MagicMock(return_value=UTC_NOW))
    def test__post__with_one_mentor_profile__with_mentorship_session__allowed_statuses(self):
        statuses = ['COMPLETED', 'FAILED']

        for current in range(0, 2):
            started_at = timezone.now()
            mentorship_session = {
                'started_at': None,
                'allow_billing': True,
                'status': statuses[current],
                'started_at': started_at,
            }
            model = self.bc.database.create(user=1,
                                            role=1,
                                            capability='crud_mentorship_bill',
                                            mentor_profile=1,
                                            mentorship_session=mentorship_session,
                                            profile_academy=1)

            self.bc.request.set_headers(academy=model.academy.id)
            self.bc.request.authenticate(model.user)

            url = reverse_lazy('mentorship:academy_mentor_id_bill',
                               kwargs={'mentor_id': model.mentor_profile.id})
            response = self.client.post(url)

            json = response.json()
            expected = [
                post_serializer(self,
                                model.mentor_profile,
                                model.mentorship_service,
                                model.user,
                                data={'id': current + 1}),
            ]

            self.assertEqual(json, expected)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(self.bc.database.list_of('mentorship.MentorshipBill'), [
                mentorship_bill_columns(data={
                    'id': current + 1,
                    'mentor_id': current + 1,
                    'academy_id': current + 1,
                }),
            ])

            # teardown
            self.bc.database.delete('mentorship.MentorProfile')
            self.bc.database.delete('mentorship.MentorshipBill')

    # @patch('django.utils.timezone.now', MagicMock(return_value=UTC_NOW))
    # def test__post__with_one_mentor_profile__with_mentorship_session__with_mentorship_bill(self):
    #     started_at = timezone.now()
    #     mentorship_session = {
    #         'started_at': None,
    #         'allow_billing': True,
    #         'status': 'COMPLETED',
    #         'started_at': started_at,
    #     }
    #     mentorship_bill = {'status': 'DUE'}
    #     model = self.bc.database.create(user=1,
    #                                     role=1,
    #                                     capability='crud_mentorship_bill',
    #                                     mentor_profile=1,
    #                                     mentorship_session=mentorship_session,
    #                                     mentorship_bill=mentorship_bill,
    #                                     profile_academy=1)

    #     self.bc.request.set_headers(academy=model.academy.id)
    #     self.bc.request.authenticate(model.user)

    #     url = reverse_lazy('mentorship:academy_mentor_id_bill', kwargs={'mentor_id': model.mentor_profile.id})
    #     response = self.client.post(url)

    #     json = response.json()
    #     expected = [
    #         post_serializer(self, model.mentor_profile, model.mentorship_service, model.user, data={'id': 1}),
    #     ]

    #     self.assertEqual(json, expected)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(self.bc.database.list_of('mentorship.MentorshipBill'), [
    #         mentorship_bill_columns(data={
    #             'id': 1,
    #             'mentor_id': 1,
    #             'academy_id': 1,
    #         }),
    #     ])
