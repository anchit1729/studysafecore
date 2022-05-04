from rest_framework.schemas.openapi import AutoSchema
from rest_framework import generics, viewsets
from .serializers import *
from .models import VisitRecord
from .models import HKUMember
from .models import Venue

"""
Author: Anchit Mishra
This class provides the ListAPIView functionality of displaying
all access for all members' entries/exits to/from all venues.
"""
class all_access_records(viewsets.ModelViewSet):
    queryset = VisitRecord.objects.all()
    serializer_class = VisitRecordSerializer

"""
Author: Ajayveer Singh
This class provides the ListAPIView functionality of listing all the close contacts.
"""
class view_close_contacts(generics.ListAPIView):
    serializer_class = HKUMemberUIDSerializer
    def get_queryset(self, **kwargs):

        from datetime import datetime, timedelta

        # UID of infected person and date of first confirmed positive test/onset of symptoms
        uid = self.kwargs['uid']
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d')

        # Get the UIDs of all the people who used the same venues on the same days as infected (within 2 day span)
        dates = [(date - timedelta(days=2)).strftime("%Y-%m-%d"), (date - timedelta(days=1)).strftime("%Y-%m-%d"), (date).strftime("%Y-%m-%d")]
        potential_close_contacts = VisitRecord.objects.filter(record_datetime__date__in = dates).values('member_uid').distinct()
        #print(potential_close_contacts)

        # stores UIDs of close contacts
        close_contacts = []

        # Pairs up 2 visit records - the entry and exit record for a student visitng a venue
        entry_exit_pairs = []

        # Process all visit records one member at a time
        for potential_close_contact in potential_close_contacts:

            # NOT GETTING RECORDS NEEDS FIX
            potential_close_contact_uid = potential_close_contact['member_uid']
            visit_record_of_potential_close_contact = VisitRecord.objects.filter(record_datetime__date__in = dates, member_uid = potential_close_contact_uid)
            #print('===========\tNani',visit_record_of_potential_close_contact)

            # for dateX in dates:
            #     temp = VisitRecord.objects.filter(member_uid = potential_close_contact)
            #     x = potential_close_contact['member_uid']
            #     print(f'TEMP {x} ====================== \t', temp)

            if visit_record_of_potential_close_contact:

                current = visit_record_of_potential_close_contact[0]
                for visit in visit_record_of_potential_close_contact.order_by('record_datetime'):
                    #print('===========\tVisit',visit)
                    if visit.access_type == 'IN':
                        current = visit
                    else:
                        #print(visit)
                        entry_exit_pairs.append(
                            {
                                'member_uid': visit.member_uid,
                                'venue_code': visit.venue_code,
                                'time_in': current.record_datetime,
                                'time_out': visit.record_datetime
                            }
                        )

                        current = None

        entry_exit_pairs_of_infected = list() #ist(filter(lambda x: x['member_uid'] == uid, entry_exit_pairs))

        for i in entry_exit_pairs:
            #print(i['member_uid'],uid, str(i['member_uid']) == str(uid))
            if str(i['member_uid']) == str(uid):
                entry_exit_pairs_of_infected.append(i)

        #print(entry_exit_pairs_of_infected)

        for entry_exit_pair in entry_exit_pairs:
            for bad_time_to_be_here in entry_exit_pairs_of_infected:
                #print(entry_exit_pair['time_in'],'\t',bad_time_to_be_here['time_out'])
                if entry_exit_pair['time_in'] < bad_time_to_be_here['time_out'] and entry_exit_pair['time_out'] > bad_time_to_be_here['time_in']:
                    overlap = min( entry_exit_pair['time_out'] - bad_time_to_be_here['time_in'], bad_time_to_be_here['time_out'] - entry_exit_pair['time_in'])
                    if overlap.seconds / 3600 > 0.5:
                        close_contacts.append(entry_exit_pair['member_uid'])


        return HKUMember.objects.filter(uid__in = close_contacts).exclude(uid=uid)



    # To-do
    # Decide on what the url looks like and how to extract parameters
    # Steps to get close contacts
    # 1. Get all access records for date-2, date-1, and date
    # 2. Group access records into IN & OUT pairs
    # 3. Find IN & OUT pairs of infected/query HKUMember
    # 4. Iterate through list of pairs and select those that overlap for more than 30 minutes




"""
Author: Shao Rui
This class provides the ListAPIview functionality of listing all venues that a
confirmed case have been to in the last 2 days
"""
class view_infected_venues(generics.ListAPIView):
    # only get the venue code of infected venues for studysafe trace consumption
    serializer_class = VenueCodeSerializer

    def get_queryset(self, **kwargs):
        from datetime import datetime, timedelta

        # UID of infected person and date of first confirmed positive test/onset of symptoms
        uid = self.kwargs['uid']
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d')

        dates = [(date - timedelta(days=2)).strftime("%Y-%m-%d"), (date - timedelta(days=1)).strftime("%Y-%m-%d"), (date).strftime("%Y-%m-%d")]
        # venues that the confirmed case has been to in the past 2 days
        infected_venues = VisitRecord.objects.filter(record_datetime__date__in = dates, member_uid = uid).values('venue_code').distinct()

        return infected_venues


"""
Author: Peng Yinglun
This class provides the ListAPIview functionality of listing all the venues in the
database, including their venue_code, location, type and all other information.
"""
class view_all_venues(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

"""
Author: Shao Rui
This class provides the ListAPIView functionality of displaying
all HKU Members' record
"""
class list_all_members(viewsets.ModelViewSet):
    queryset = HKUMember.objects.all()
    serializer_class = HKUMemberSerializer