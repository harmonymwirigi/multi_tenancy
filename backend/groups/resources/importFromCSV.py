import os
import csv

class CSVLoader():
    def __init__(self):
        self.errors = []
        self.phone_number_column = None
        self.names_column = None
        self.BASE_URL = ''

    def _check_size_of_file(self,file_name):
        '''
            check that the file has a decent amount of rows.
        '''
        with open(file_name) as csv_file:          
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count = 0
            self.errors = []
            for row in csv_reader:
                if any(row):
                    if line_count == 0:
                        line_count += 1
                    else:
                        line_count += 1

            if line_count > 250:
                self.errors.append("File has too many rows ("+ str(line_count + 1) + ") expected 250 or less")

            if (len(self.errors) > 0):
                return False
            else:
                return True

    def _check_names(self,file_name):
        '''
            check that the names are valid
        '''
        with open(file_name) as csv_file:           
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count = 0
            self.errors = []
            for row in csv_reader:
                if any(row):
                    if line_count == 0:
                        line_count += 1
                    else:
                        names =  row[self.names_column].strip()
                        line_count += 1

            if (len(self.errors) > 0):
                return False
            else:
                return True

    def _check_phone_number(self,file_name):
        '''
            check that the phone number input provided is correct
        '''    
        with open(file_name) as csv_file:            
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count = 0
            self.errors = []
            for row in csv_reader:
                if any(row):
                    phone_number = row[self.phone_number_column]
                    if line_count == 0:
                        line_count += 1
                    else:
                        phone_number = phone_number.strip()
                        #ignore all white spaces
                        if (    len(phone_number) != 10
                            and len(phone_number) != 9#when the leading zero was left out
                            and len(phone_number) != 0):
                            self.errors.append("incorrect phone number format ("\
                                                + phone_number \
                                                + " ) at line "\
                                                + str(line_count + 1) \
                                                + " use format 0712345678")

                        if (len(phone_number) == 10):
                            if(phone_number[0] != "0"):
                                self.errors.append("incorrect phone number format ("\
                                                    + phone_number \
                                                    + " ) at line "\
                                                    + str(line_count + 1)\
                                                    + " use format 0712345678")
                            # check that they are all numbers
                            try:
                                int(int(phone_number[1:10]))
                            except ValueError:
                                self.errors.append("incorrect phone number format ("\
                                                    + phone_number \
                                                    + " ) at line "\
                                                    + str(line_count + 1)\
                                                    + " use format 0712345678")
                        if (len(phone_number) == 9):
                            try:
                                int(int(phone_number[0:8]))
                            except ValueError:
                                self.errors.append("incorrect phone number format ("\
                                                    + phone_number \
                                                    + " ) at line "\
                                                    + str(line_count + 1) \
                                                    + " use format 712345678")
                        line_count += 1

            if (len(self.errors) > 0):
                return False
            else:
                return True

    #public methods
    def set_base_url(self,base_url):
        self.BASE_URL = base_url.split(':')[0] + "/"

    def preview_CSV(self, file_name):
        '''
            return the csv as json for preview in the UI
        '''
        data = []
        with open(file_name) as csv_file:           
            csv_reader = csv.DictReader(csv_file,delimiter=',')
            row = {}
            count = 0
            for row in csv_reader:
                if count < 200:
                    row = row
                    data.append(row)
                    count += 1
                else:
                    break
        return data

    def configure_CSV(self, file_name, config_tuple):
        '''
            configure the csv file columns according to specifications by the config_tuple
        '''
        self.phone_number_column = None
        self.names_column = None
        with open(file_name) as csv_file:        
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    for key in config_tuple:
                        for i in range(0,len(row)):
                            if row[i].strip() == key.strip():
                                if config_tuple[key] == 'phone number':
                                    self.phone_number_column = i
                                if config_tuple[key] == 'names':
                                    self.names_column = i
                else:
                    break
                line_count += 1

    def check_CSV(self, file_name):
        '''
            check if CSV meets the required standards
        '''
        if (not self._check_size_of_file(file_name)):
            return False
        if (not self._check_names(file_name)):
            return False
        if (not self._check_phone_number(file_name)):
            return False
        #if everything is okay then return True
        return True

    # TODO: review length of this function
    def get_phone_numbers(self, file_name):
        '''
            load a csv file and get its detail
        '''
        phone_numbers = [] 
        with open(file_name) as csv_file:          
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count = 0        
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    # get phone_number
                    phone_number = row[self.phone_number_column]
                    # get names
                    names =  row[self.names_column].strip()
                    names =  names.split(" ")

                    #try getting user by their phone number.
                    if phone_number:
                        if phone_number[0] == '0':
                            phone_number = phone_number.replace('0','+254',1)
                        if phone_number[:3] == '254':
                            phone_number = phone_number.replace('254','+254',1)
                        phone_numbers.append((phone_number," ".join(names)))
                        continue
        return phone_numbers
