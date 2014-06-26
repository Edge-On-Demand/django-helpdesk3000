from __future__ import print_function

# Make warnings throw explicit exceptions so we're forced to fix them.
import warnings
warnings.simplefilter('error', RuntimeWarning)

from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.core.urlresolvers import reverse

import six

from helpdesk.models import (
    Queue, CustomField, Ticket, User, EmailTemplate,
)

class TicketBasicsTestCase(TestCase):
    
    fixtures = ['test_data.json']
    
    def setUp(self):
        
        self.queue_public = Queue.objects.create(
            title='Queue 1',
            slug='q1',
            allow_public_submission=True,
            new_ticket_cc='new.public@example.com',
            updated_ticket_cc='update.public@example.com')
            
        self.queue_private = Queue.objects.create(
            title='Queue 2',
            slug='q2',
            allow_public_submission=False,
            new_ticket_cc='new.private@example.com',
            updated_ticket_cc='update.private@example.com')

        self.ticket_data = {
            'title': 'Test Ticket',
            'description': 'Some Test Ticket',
        }

        self.client = Client()

    def test_create_ticket_direct(self):
        email_count = len(mail.outbox)
        ticket_data = dict(queue=self.queue_public, **self.ticket_data)
        ticket = Ticket.objects.create(**ticket_data)
        self.assertEqual(ticket.ticket_for_url, "q1-%s" % ticket.id)
        self.assertEqual(email_count, len(mail.outbox))
        

    def test_create_ticket_public(self):
        email_count = len(mail.outbox)

        response = self.client.get(reverse('helpdesk_home'))
        self.assertEqual(response.status_code, 200)

        # Submit a ticket.
        post_data = {
            'title': 'Test ticket title',
            'queue': self.queue_public.id,
            'submitter_email': 'ticket1.submitter@example.com',
            'body': 'Test ticket body',
            'priority': 3,
        }
        response = self.client.post(
            reverse('helpdesk_home'), post_data, follow=True)
        last_redirect = response.redirect_chain[-1]
        last_redirect_url = last_redirect[0]
        last_redirect_status = last_redirect[1]
        
        # Ensure we landed on the "View" page.
        self.assertEqual(
            last_redirect_url.split('?')[0],
            'http://testserver%s' % reverse('helpdesk_public_view'))
            
        # Ensure submitter, new-queue + update-queue were all emailed.
#        for email in mail.outbox:
#            #print(dir(email), email.__dict__.keys())
#            print(email.subject, email.to)
        self.assertEqual(email_count+3, len(mail.outbox))
        
        email_templates = EmailTemplate.objects.filter(locale='en')
        self.assertEqual(email_templates.count(), 16)
        
        # Lookup ticket.
        t = Ticket.objects.all().order_by('-id')[0]
        
        users = User.objects.all()
        self.assertEqual(users.count(), 2)
        
        # Assign ticket.
        mail.outbox = []
        t.assigned_to = users[0]
        t.save()
        
        # Confirm a reassignment notice email was sent.
        self.assertEqual(len(mail.outbox), 1)
        #print(mail.outbox[0].body)
    
    def test_create_ticket_private(self):
        email_count = len(mail.outbox)
        post_data = {
            'title': 'Private ticket test',
            'queue': self.queue_private.id,
            'submitter_email': 'ticket2.submitter@example.com',
            'body': 'Test ticket body',
            'priority': 3,
        }

        response = self.client.post(reverse('helpdesk_home'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(email_count, len(mail.outbox))
        self.assertContains(response, 'Select a valid choice.')

    def test_create_ticket_customfields(self):
        email_count = len(mail.outbox)
        
        queue_custom = Queue.objects.create(
            title='Queue 3',
            slug='q3',
            allow_public_submission=True,
            updated_ticket_cc='update.custom@example.com')
            
        custom_field_1 = CustomField.objects.create(
            name='textfield',
            label='Text Field',
            data_type='varchar',
            max_length=100,
            ordering=10,
            required=False,
            empty_selection_list=False,
            staff_only=False)
            
        post_data = {
            'queue': queue_custom.id,
            'title': 'Ticket with custom text field',
            'submitter_email': 'ticket3.submitter@example.com',
            'body': 'Test ticket body',
            'priority': 3,
            'custom_textfield': 'This is my custom text.',
        }

        response = self.client.post(
            reverse('helpdesk_home'), post_data, follow=True)

        custom_field_1.delete()
        last_redirect = response.redirect_chain[-1]
        last_redirect_url = last_redirect[0]
        last_redirect_status = last_redirect[1]
        # Ensure we landed on the "View" page.
        self.assertEqual(
            last_redirect_url.split('?')[0],
            'http://testserver%s' % reverse('helpdesk_public_view'))
        # Ensure only two e-mails were sent - submitter & updated.
        self.assertEqual(email_count+2, len(mail.outbox))

class PublicActionsTestCase(TestCase):
    """
    Tests for public actions:
    - View a ticket
    - Add a followup
    - Close resolved case
    """
    def setUp(self):
        """
        Create a queue & ticket we can use for later tests.
        """
        
        self.queue = Queue.objects.create(
            title='Queue 1',
            slug='q',
            allow_public_submission=True,
            new_ticket_cc='new.public@example.com',
            updated_ticket_cc='update.public@example.com')
            
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            queue=self.queue,
            submitter_email='test.submitter@example.com',
            description='This is a test ticket.')

        self.client = Client()

    def test_public_view_ticket(self):
        response = self.client.get(
            '%s?ticket=%s&email=%s' % (reverse('helpdesk_public_view'),
            self.ticket.ticket_for_url, 'test.submitter@example.com'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'helpdesk/public_view_form.html')

    def test_public_close(self):
        old_status = self.ticket.status
        old_resolution = self.ticket.resolution
        resolution_text = 'Resolved by test script'

        ticket = Ticket.objects.get(id=self.ticket.id)
        
        ticket.status = Ticket.RESOLVED_STATUS
        ticket.resolution = resolution_text
        ticket.save()

        current_followups = ticket.followup_set.all().count()
        
        response = self.client.get(
            '%s?ticket=%s&email=%s&close' % (reverse('helpdesk_public_view'),
            ticket.ticket_for_url, 'test.submitter@example.com'))
        
        ticket = Ticket.objects.get(id=self.ticket.id)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'helpdesk/public_view_form.html')
        self.assertEqual(ticket.status, Ticket.CLOSED_STATUS)
        self.assertEqual(ticket.resolution, resolution_text)
        self.assertEqual(
            current_followups+1, ticket.followup_set.all().count())
        
        ticket.resolution = old_resolution
        ticket.status = old_status
        ticket.save()
