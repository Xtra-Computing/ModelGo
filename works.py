"""
Define the base concept of licensed material (work).
"""

import logging, copy
from collections import defaultdict, namedtuple
from tabulate import tabulate

"""
Record the warnings, errors and conflicts during analysis of work
"""
Evn = namedtuple('Event', ['type', 'info'])
class EVENT(object):

    PERSONAL_OPEN_POLICY = Evn('policy', 'The desired release scenario of $WNAME$ is for PERSONAL')
    SHARE_OPEN_POLICY = Evn('policy', 'The desired release scenario of $WNAME$ is for FREE SHARING')
    SELL_OPEN_POLICY = Evn('policy', 'The desired release scenario of $WNAME$ is for SELLING')

    LICENSE_TYPE_MISMATCH_WARNING = Evn('licenses warning', 'License $LNAME$ is NO suitable for $WNAME$ ($WTYPE$) licensing')
    LICENSE_DISCLOSE_SELF_WARNING = lambda work_name, license_name: Evn('licenses warning', f"Work {work_name} must remain OPEN SOURCE (raw) or provide a READABLE COPY of source code according to license {license_name}")
    LICENSE_NO_FOUND_ERROR = lambda path : Evn("licenses error", f"License $LNAME$ could NOT be located in the parser file {path}")
    LICENSE_SHARING_PROHIBITED_ERROR = lambda work_name, license_name: Evn("licenses error", f"Work {work_name} CONNOT BE SHARED due to the prohibition of license {license_name}")
    
    MIXWORKS_NO_FOUND_WARNING = Evn('analysis warning', 'Work $WNAME$ does NOT have mixworks as expected')
    MULTIPLE_COPYLEFT_ERROR = lambda copylefts: Evn("analysis error", f"Work $WNAME$ has a license conflict as it involves multiple copyleft licenses: {', '.join([l.license_name for l in copylefts])}")
    
    RIGHT_NO_GRANT_WARNING = lambda work_name, right_name: Evn('rights warning', f'Work {work_name} does NOT EXPLICITLY grant you the right to {right_name.upper()}')
    RIGHT_NO_GRANT_ERROR = lambda work_name, right_name: Evn('rights error', f'Work {work_name} does NOT grant you the right to {right_name.upper()}')
    
    STATE_CHANGES = lambda work_name, license_name: Evn("restriction", f"Work $WNAME$ must STATE the CHANGES according to {license_name} of {work_name}")
    INCLUDE_LICENSE = lambda work_name, license_name: Evn("restriction", f"Work $WNAME$ must RETAIN the ORIGINAL LICENSE file according to {license_name} of {work_name}")
    INCLUDE_NOTICE = lambda work_name, license_name: Evn("restriction", f"Work $WNAME$ must RETAIN all NOTICE files (e.g. copyright, patent, trademark, and attribution) from the source form of {work_name} according to {license_name}")
    INCLUDE_ORIGINAL = lambda work_name, license_name: Evn("restriction", f"Work $WNAME$ must include the copies of the original work or the instructions to obtain copies of {work_name} according to {license_name}")
    INCLUDE_USE_RESTRICTION = lambda work_name, license_name: Evn("restriction", f"Work $WNAME$ must comply with the USE restriction terms according to {license_name} of {work_name}")
    INCLUDE_RUNTIME_RESTRICTION = lambda work_name, license_name: Evn("restriction", f"Work $WNAME$ must comply with the RUNTIME restriction terms according to {license_name} of {work_name}")

class Work(object):
    def __init__(self, name:str, type:str, form:str, license_name:str='TBD'):
        self.name = name
        self.type = type # software/data/model or mix (mix of works with different type)
        self.form = form # raw/binary/saas
        self.license_name = license_name # MIT, Apache-2.0, Unlicense
        self.assigned_license_name = None # Manual assigned license for this work, call analysis of license parser to take effect
        self.license = None # Need license parser to assign a license instance
        
        """
        Bundle of Works:
        +---------------++---------------+
        |   mixwork1    ||   Mixwork2    |
        +---------------++---------------+     
        """

        self.mixworks = [] # list of (works, usage), this work contain a bundle of works
        self.subworks = [] # list of (work, usage), subworks are input of this work and will be released with this work
        self.auxworks = [] # list of (work, usage), aux works will not be released with this work

        self.relied_works = [] # All relied works for this work
        
        self.caution = []
        
        # Assign 'License' instance for this work
        #self.license = self.parse_license(license_name)
        #self.parser.work_type_check(self.license, self.type)

    def set_license(self, license):
        # Assign or Reset 'License' instance to this work
        self.license = license
        self.license_name = license.short_id
    
    def is_include_mixworks(self):
        if len(self.mixworks) > 0: # At least one mixworks
            return True
        return False

    def is_registered(self):
        if self.license is None:
            return False
        return True
    
    def is_relied_work(self, work):
        if work in self.mixworks + self.subworks + self.auxworks:
            return True
        return False

    def add_event(self, event):
        if isinstance(event, list):
            self.caution += event
        if isinstance(event, Evn):
            self.caution.append(event)

    def has_relied_work(self, exclude=[]):
        coverage = []
        for _type, _works in zip(['aux', 'mix', 'sub'], [self.auxworks, self.mixworks, self.subworks]):
            if _type not in exclude:
                coverage = coverage + _works
        if len(coverage) > 0:
            return True
        return False
    
    def assign_license(self, assigned_license_name:str):
        if assigned_license_name:
            self.assigned_license_name = assigned_license_name
            return True
        return False
    
    # Recursion, you can exclude 'aux', 'mix', 'sub' works
    def find_relied_works(self, exclude=[]) -> list:
        relied_works = []
        coverage = []
        for _type, _works in zip(['aux', 'mix', 'sub'], [self.auxworks, self.mixworks, self.subworks]):
            if _type not in exclude:
                coverage = coverage + _works
        
        for work, usage in coverage:
            if work.has_relied_work(exclude):
                # Recursively find the relied works
                relied_works += work.find_relied_works(exclude) + [(work, usage)] # Insert new found works from left
            else:
                relied_works += [(work, usage)] 
        return relied_works
    
    # The relied works exlcude aux works will be share with this work (subworks, mixworks and this work)
    def find_shared_works(self):
        return self.find_relied_works(exclude=['aux'])
    
    # Find all mixworks of this work
    def find_mixworks(self):
        return self.find_relied_works(exclude=['aux', 'sub'])
    
    # ??? Removal of redundancies, priority of work retained: mixworks > subworks > auxworks
    # deduplicate event???
    def deduplicate_relied_works(self, exclude=[]):
        all_relied_works = {
            'mix' : self.find_relied_works(exclude=['aux', 'sub']),
            'sub' : self.find_relied_works(exclude=['aux', 'mix']),
            'aux' : self.find_relied_works(exclude=['mix', 'sub'])
        }
        return
    
    # Return the name of open policy by searching from the events in self.caution
    def find_open_policy(self):
        # Search the open policy information
        _open_policy_event = [EVENT.PERSONAL_OPEN_POLICY, EVENT.SHARE_OPEN_POLICY, EVENT.SELL_OPEN_POLICY]
        _open_policy_name = ['Personal Use', 'Share', 'Sell']
        #opevent, opname = None, None
        opevent = self.filter_events_by_type('policy')
        if opevent:
            opname = None
            for _policy, _name in zip(_open_policy_event, _open_policy_name):
                if opevent[0] == _policy: # Only compare the first open policy event
                    opname = _name
                    break
            if opname:
                return opevent[0], opname
        return None, None # It will return None if the open policy is no found
    
    # Filter the events in self.caution by its type
    def filter_events_by_type(self, type):
        finds = []
        for _event in self.caution:
            if type.casefold() in _event.type.casefold():
                finds.append(_event)
        return finds
    
    def replace_placeholder(self, event_string:str):
        for old, new in zip(['$WNAME$', '$WTYPE$', '$LNAME$'], [self.name, self.type, self.license_name]):
            event_string = event_string.replace(old, new)
        return event_string


    # Summary of this work, including license information, conflicts and restrictions
    def summary(self):
        # The basic information of this work
        work_data = [
            ["Work Name",       self.name],
            ["Type & Form",     self.type.title() + ', ' + self.form.title()],
            ["License Name",    self.license.short_id],
            ["Relied Works",    ', '.join([w.name for w,_ in self.find_relied_works()])]
        ]

        # Search the open policy information
        opevent, opname = self.find_open_policy()
        if opname is None:
            logging.warning(f"Didn't find the open policy of Work {self.name}")
        else:
            print(f"{self.replace_placeholder(opevent.info)}.")
        
        warnings, errors, restrictions = self.filter_events_by_type('warning'), self.filter_events_by_type('error'), self.filter_events_by_type('restriction')
        remove_duplicate_events = lambda events: [e for i, e in enumerate(events) if e not in events[:i]]
        warnings, errors, restrictions  = remove_duplicate_events(warnings), remove_duplicate_events(errors), remove_duplicate_events(restrictions) # Remove the duplicate events
        restrictions_data = []
        for events in [warnings, errors, restrictions]:
            for idx, e in enumerate(events):
                restrictions_data.append([f"{e.type.title()} - {idx+1}", self.replace_placeholder(e.info)])
        
        # Summary the basic information of this work
        print(f"The base information of {self.name}:")
        print(tabulate(work_data, tablefmt="grid"))
        print()

        # Print open policy information
        print(f"To {opname} this work in compliance, you must take into account the following Warnings({len(warnings)}), Errors({len(errors)}), Restrictions({len(restrictions)}).")
        # Print the restrictions information of this work and all relied works
        print(tabulate(restrictions_data, tablefmt="grid"))
        print()

        # Print the license information of this work
        print(f"The information of {self.license_name} license of this work is:")
        self.license.summary()
        return
