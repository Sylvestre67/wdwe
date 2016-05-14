__author__ = 'gugs'
from datetime import datetime

class Job(object):
    start_date = None
    end_date = None

def number_of_years(filename):
    input = open(filename, 'r')
    input.readline()

    years_of_experience = 0
    for line in input:
        #Check if any of the other experience is on the same timedelta

        #Calculate timedelta in month

        #add it to global expereience
        applicant = line.replace('\n','').split(';')

        for exp in applicant:
            applications = []
            new_job = Job()
            for date in exp.strip().split('-'):
                new_job.start_date = datetime.strptime(date, '%b %Y')
                new_job.end_date = datetime.strptime(date, '%b %Y')

                applications.append(new_job)
                print new_job


number_of_years('dates.txt')