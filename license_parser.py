import yaml
import logging
from copy import copy
from tabulate import tabulate
from collections import OrderedDict, namedtuple, defaultdict
from works import Work, EVENT

""" Use for standardize the string list of license rights """
def standardize_string_list(string_list):
    # Capitalize and replace underscore
    processed_list = []
    for string in string_list:
        processed_string = string.title().replace("_", " ")
        processed_list.append(processed_string)
    # String list -> String seperated with comma
    standard_string = ", ".join(processed_list)
    return standard_string

class License(object):
    def __init__(self, license_meta, usages_dict):
        self.meta = license_meta
        self.usages_dict = usages_dict
        self.full_name = license_meta["full_name"]
        self.short_id = license_meta["short_id"]

        # Modified by parser
        self.relicense = False
        #self.caution = {'restrictions':defaultdict(list), 'rights':defaultdict(list), 'warnings':defaultdict(list)}

    def is_public(self):
        if "public" in self.meta["categories"]:
            return True
        return False
    
    def is_public_domain(self):
        if "Public Domain" in self.meta["labels"]:
            return True
        return False
        
    def is_copyleft(self):
        if "copyleft" in self.meta["categories"]:
            return True
        return False
    
    def is_disclose(self):
        if "disclose" in self.meta["categories"]:
            return True
        return False
    
    def is_auto_relicensing(self):
        if 'auto-relicensing' in self.meta["categories"]:
            return True
        return False
    
    def is_permissive(self):
        if "permissive" in self.meta["categories"]:
            return True
        return False
    
    def is_irrevocable(self):
        if "irrevocable" in self.meta["rights_prefix"]:
            return True
        return False
    
    # Check whether a right can be granted, such as modify, use, sublicense
    def is_granted_right(self, right:str):
        if self.is_public_domain(): # Always return true for public domain licenses
            return True
        elif right in self.meta["rights"]:
            return True
        elif right in self.meta["reserved_rights"]:
            return False
        return "NODEF"
    
    # Check whether this license can be apply to a work in "type" (model, data, software)
    def is_supported_work_type(self, type:str):
        if type == "model": 
            # Models can be regarded as software, model, or derivative of data
            return True
        elif type in self.meta["categories"]:
            return True
        return False
    
    def get_share_coverage(self) -> list:
        if 'coverage' in self.meta:
            return self.meta['coverage']
        return []
    
    # Generate a summary of this license
    def summary(self):
        notices = []
        if self.is_copyleft() is True: notices.append("Copyleft")
        if self.is_irrevocable() is False: notices.append("Revocable")
        if self.is_public() is False: notices.append("Not Public")
        data = [
            ["License Name",        self.full_name],
            ["License Tags",        standardize_string_list(self.meta['categories'])],
            ["Granted Rights",      standardize_string_list(self.meta['rights'])],
            ["Reserved Rights",     standardize_string_list(self.meta['reserved_rights'])],
            ["Notices for Use",     "None" if notices == [] else ', '.join(notices)],
            ["Full Text Link",      self.meta['url']]
        ]
        print(tabulate(data, tablefmt="grid"))
        return data


class Parser(object):
    def __init__(self, path):
        self.path = path
        try:
            # Read the Summaried License Description from YAML file
            licenses_file = open(path)
            yml_content = yaml.safe_load(licenses_file)
            licenses_file.close()
            usages_dict, licenses_list = yml_content[0], yml_content[1:]
        except IOError:
            logging.error(f"Failed to open the licenses file in {path}.")

        # Use the short id as index of licenses dict
        self.licenses_dict = {}
        for li in licenses_list:
            if "short_id" in li:
                license_meta = li
                self.licenses_dict[li["short_id"]] = License(license_meta, usages_dict)

        self.licenses_list = list(self.licenses_dict.keys())

    def __find_matching_license(self, license_name, ignore_case=True, ignore_version=True):
        def remove_version(license_name): # Remove the version number in license's name
            if '-' in license_name:
                maybe_name, maybe_ver_str = license_name.rsplit('-', 1)
                if maybe_ver_str.replace('.','').isdigit(): # The license name contains version number
                    return maybe_name
            return license_name # Version number no found

        if ignore_case:
            license_name = license_name.casefold()
            licenses_list = [name.casefold() for name in self.licenses_list]
        if ignore_version:
            license_name = remove_version(license_name)
            licenses_list = [remove_version(name) for name in licenses_list]
        if license_name in licenses_list:
            idx = licenses_list.index(license_name)
            return self.licenses_list[idx] # Return the name in license description
        return None
        

    
    # Register license for the work or a list of works
    def register_license(self, work:Work, relicense=False):
        if isinstance(work, list):    
            licenses = [self.register_license(w) for w in work]
            return licenses

        if work.license_name == 'TBD':
            logging.warning(f"The license name of Work {work.name} is not specified")
            return None

        # Create a new license instance by name
        license = self.clone_license(work.license_name)
        if license is None:
            logging.error(f"Cannot find the license decription of {work.license_name} in {self.path}")
            work.add_event(EVENT.LICENSE_NO_FOUND_ERROR)
            return None
        
        if self.work_type_check(license, work) == False:
            work.add_event(EVENT.LICENSE_TYPE_MISMATCH_WARNING)
            logging.warning(f"{license.short_id} is no suitable for {work.name} ({work.type}) licensing")

        if work.is_registered() and relicense == False:
            logging.debug(f"{work.name} already has {license.short_id} license, ignore the license registration")
        else:
            work.set_license(license) # Set the license instanct and fresh the license name of this work
            logging.debug(f"{work.name} is registered as {work.license_name}")
        return license


    # Return a copy of license by name, return none if no found
    def clone_license(self, license_name) -> License:
        match_license = self.__find_matching_license(license_name)
        if match_license:
            logging.debug(f"Find the matching license: {match_license}")
            clone = copy(self.licenses_dict[match_license])
            return clone
        return None
    
    # Check whether the license can support this type of work (software, model, data). Note, work maybe unregistered.
    def work_type_check(self, license:License, work:Work) -> bool:
        if work.type == 'mix':
            if work.is_include_mixworks() == True: # Mixworks list contant at least one work
                # IF this work is mix of works, return True IF the license can match at least one of mixworks' type
                for (mixw, _) in work.mixworks:
                    if self.work_type_check(license, mixw) is True: # Recursion
                        return True
            else: # The mixworks list of this 'mix' type work is empty
                logging.warn(f"The type of {work.name} is 'mix' but its has no mixworks")
                work.add_event(EVENT.MIXWORKS_NO_FOUND_WARNING)
        elif license.is_supported_work_type(work.type) is True: # Work type is one of 'model', 'data', 'algorithm'
            return True
        #license.caution['warnings']['TYPE_MISMATCH'].append((license.short_id, type))
        return False

    # Analysis the right grantable and licensing (license name='TBD') of work
    # The supported 'open_policy' are 'sell', 'share', 'personal'
    # NOTE: The subworks are considered as be released with this work but auxworks are not.
    def analysis(self, work:Work, open_policy:str='share'):

        # 1, Find all relied and no licensed works ('TBD') for licensing analysis, include this work
        # Then, determine license for 'TBD' works by call license_analysis
        works_sequence = [w for w, _ in work.find_relied_works() if w.license_name == 'TBD'] + [work]
        for alys_work in works_sequence:
            self.license_analysis(alys_work)
        
        # 2, Check the rights granting for reuse and open (such as share, sell)
        self.rights_granting_analysis(work, open_policy)

        # 3, Check the restrictions involved by relied works
        self.restrictions_analysis(work, open_policy)
        
        # 4, Finnal check for disclose and redistribute requirements
        self.redistribution_analysis(work, open_policy)
        return  

    """
        Register new license for TBD work, the default license is 'Unlicense'.
        If there has one copyleft license, license proliferation will be applied,
        If there has two or more different copyleft licenses, an error will be thrown.
        NOTE: This function only consider the first level relied works that with explicit licenses, please loop this function if need.
    """
    def license_analysis(self, TBD_work:Work) -> bool:
        if TBD_work.license_name != 'TBD':
            logging.warning(f"{TBD_work.name} has license, no need for license analysis")
            return False
        
        elif TBD_work.has_relied_work() is False: # license_name == TBD but w/o relied work.
            TBD_work.license_name = 'Unlicense' # Default to 'Unlicense'
            self.register_license(TBD_work)
            return True

        # MAIN FUNCTION. license_name == TBD, this work has relied works (first level), and all these works are registered
        elif all(rw.is_registered() == True for rw, _ in TBD_work.mixworks + TBD_work.subworks + TBD_work.auxworks):
            relied_works = TBD_work.mixworks + TBD_work.subworks + TBD_work.auxworks # First level relied works
            # Find applied term in each relied work
            terms = {rw: self.find_applied_term(rw, ru) for rw, ru in relied_works}
            copylefts = [rw for rw, _ in relied_works if rw.license.is_copyleft() == True] # Relied works that under copyleft licenses
            permissives = [rw for rw, _ in relied_works if rw.license.is_permissive() == True] # Relied works that under permissive licenses
            # Find triggered copylefts works that result in copyleft license proliferation 
            triggered_copylefts = [rw for rw in copylefts if terms[rw]['result'] not in ['independent', 'NODEF']]

            # We tend to fullfill the prior license assignment of this work if it is exist
            aim_license_name = self.clone_license(TBD_work.assigned_license_name).short_id if TBD_work.assigned_license_name else None
            
            # Deal with copyleft situation
            # Triggered copyleft licenses be detected, the license proliferation need be handled
            if len(triggered_copylefts) >= 1:
                if all(w.license.short_id == triggered_copylefts[0].license.short_id 
                       for w in triggered_copylefts): # These copyleft licenses are same
                    aim_copyleft_license_name = triggered_copylefts[0].license.short_id
                    if aim_license_name and aim_copyleft_license_name != aim_license_name: 
                        # There has a conflict between the assignment of this work and the copyleft licenses of relied works, this work will be licensed as the copyleft one    
                        logging.warning(f"Cannot fullfill the license assignment of work {TBD_work.name} due to the limitation of copyleft licenses of its relied works")
                    aim_license_name = aim_copyleft_license_name
                else: # Two or more copyleft licenses
                    TBD_work.add_event(EVENT.MULTIPLE_COPYLEFT_ERROR(copylefts))
                    logging.error(f'Mulitiple copyleft licenses exist in work {TBD_work.name}')
                    return False
            
            # Deal with all permissive and no license assignment situation 
            elif aim_license_name is None: 
                # we tend to retain same permissive license to new work
                exclude_unlicense = [w.license.short_id for w in permissives if w.license.short_id != 'Unlicense']
                if all(pli == exclude_unlicense[0] for pli in exclude_unlicense):
                    # All relied work under same permissive license (exclude Unlicense)
                    #aim_license_name = exclude_unlicense[0]
                    aim_license_name = 'Unlicense'
                else:
                    aim_license_name = 'Unlicense' # Register as 'Unlicense' if relied works contain multiple permissive licenses
                    logging.debug(f'Mulitiple permissive licenses exist in work {TBD_work.name}, use Unlicense by default')

            # From these need relicese works, check the availability of relicesing
            need_relicense = [rw for rw, _ in relied_works if rw.license.short_id != aim_license_name]
            cannot_relicense = []
            for rw in need_relicense: 
                if terms[rw].get('relicense') == False and terms[rw].get('result') not in ['independent', 'NODEF']:
                    cannot_relicense.append(rw)

            if len(cannot_relicense) == 0:
                # The aiming license is given and relicensing to different license of reused results is allowed
                # NOTE: The aiming license will be applied to this work, but not applied to relied works
                prev_license_name = TBD_work.license_name
                TBD_work.license_name = aim_license_name # Set to new name
                self.register_license(TBD_work, relicense=True) # Relicensing, register the new license!
                logging.debug(f'Work {TBD_work.name} be relicensed from {prev_license_name} to {TBD_work.license_name}')
                if TBD_work.license_name == TBD_work.assigned_license_name:
                    logging.debug(f"Work {TBD_work.name} was successfully licensed as {TBD_work.assigned_license_name}")
                    TBD_work.assigned_license_name = None # Reset assignment
                return True
            else: # Some relied work do not allow relicensing of reused results
                for w in cannot_relicense:
                    TBD_work.add_event(EVENT.RIGHT_NO_GRANT_ERROR(w.name, 'relicense'))
                    logging.error(f'Work {TBD_work.name} canot be licensed as {aim_license_name} \
                                  due to {w.name} does not grant the relicense rights')
                return False
        return False

    def find_applied_term(self, work:Work, usage:str) -> dict:
        terms = work.license.meta['terms']
        for t in terms:
            # Matching requirements: 1) usage is in definition; 2) work form is also in definition.
            if usage in t['usages'] and work.form in t['forms']:
                return t # Return the first found term
        return defaultdict(list)

    # Analysis rights granting
    def rights_granting_analysis(self, work:Work, open_policy:str):
        # Deal with share policy
        shared_works_list = [w for w, u in work.find_shared_works()]
        req_open_policy_rights = []
        if open_policy == 'personal': # No share and redistribute this work
            work.add_event(EVENT.PERSONAL_OPEN_POLICY)
            logging.debug(f"Work {work.name} will not be shared and does not require any permissions")
        elif open_policy in ['sell', 'share']:
            work.add_event(getattr(EVENT, (open_policy + '_OPEN_POLICY').upper()))
            req_open_policy_rights = work.license.usages_dict[open_policy]

        for rw, ru in work.find_relied_works(): 
            # Check whether the required rights is granted
            req_rights = copy(work.license.usages_dict[ru])
            if rw in shared_works_list:
                req_rights += req_open_policy_rights
            
            #print(rw.name, ru,req_rights)
            for right in req_rights:
                is_granted = rw.license.is_granted_right(right)
                if is_granted == False:
                    if right == 'sublicense' and rw.license.is_auto_relicensing() == True:
                        continue # Skip the check of sublicense right if this work has an auto-relicesing mechanism
                    work.add_event(EVENT.RIGHT_NO_GRANT_ERROR(rw.name, right))
                    logging.error(f"The required {right} right is not granted by Work {rw.name}")
                elif is_granted == 'NODEF':
                    work.add_event(getattr(EVENT, (right + '_NO_GRANT_WARNING').upper())(rw.name, right))
                    logging.warn(f"The required {right} right is not explicity granted by Work {rw.name}")
        return

    def restrictions_analysis(self, work:Work, open_policy:str=''): # open_plicy -> no use
        for rw, ru in work.find_relied_works(): 
            # Gather corresponding terms for this work
            term = self.find_applied_term(rw, ru)
            if 'restrictions' in term:
                for res in term.get('restrictions'):
                    work.add_event(getattr(EVENT, res.upper())(rw.name, rw.license_name))
        return
    
    def redistribution_analysis(self, work:Work, open_policy:str):
        # Add the redistribution requirements of the relied works and this work if it will be shared
        if open_policy in ['share', 'sell']:
            for w, u in work.find_shared_works() + [(work, 'copy')]: # This 'work' be shared as copy
                term = self.find_applied_term(w, u)
                
                if w.license.is_disclose() == True and w.type != 'raw': # Disclose Source Check, only check for shared works
                    work.add_event(EVENT.LICENSE_DISCLOSE_SELF_WARNING(w.name, w.license_name))
                
                if term['result'] and term['result'] not in w.license.get_share_coverage(): # Sharing Coverage Check 
                    work.add_event(EVENT.LICENSE_SHARING_PROHIBITED_ERROR(w.name, w.license_name)) # This work canot be shared according its license
                    continue
                if term['result'] and term['result'] not in ['independent', 'NODEF']: # Sharing Requirement Check
                    for req in w.license.meta['redistribute']:
                        work.add_event(getattr(EVENT, req.upper())(w.name, w.license_name)) # The redistribution requreiments from all shared works (e.g. mixworks and subworks)
            
        # Disclose Source Check
        '''
        for w in [rw for rw, _ in work.find_relied_works()] + [work]:
            if w.license.is_disclose() == True and w.type != 'raw':
                work.add_event(EVENT.LICENSE_DISCLOSE_SELF_WARNING(w.name, w.license_name))
        '''
        return