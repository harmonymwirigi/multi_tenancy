import os
import csv
import random
import datetime

from django.contrib.auth.models import User
from projects.models import Pledge,PledgePayment,Project
from member.models import MemberContact

class CSVLoader():
	def __init__(self):
		self.errors = []
		self.amount_column = None
		self.pledge_amount_column = None
		self.project_column = None
		self.phone_number_column = None
		self.names_column = None
		self.date_column = None
		self.BASE_URL = ''

	def _check_size_of_file(self,file_path):
		'''
			check that the file has a decent amount of rows.
		'''

		# initial_dir = os.getcwd()
		# os.chdir(self.BASE_URL+"Resources")
		with open(file_path) as csv_file:
			# os.chdir(initial_dir)
			csv_reader = csv.reader(csv_file,delimiter=',')
			line_count = 0
			self.errors = []
			for row in csv_reader:
				if any(row):
					if line_count == 0:
						line_count += 1
					else:
						line_count += 1

			if line_count > 1000:
				self.errors.append("File has too many rows ("\
									+ str(line_count + 1)\
									+ ") expected 1000 or less")

			if (len(self.errors) > 0):
				return False
			else:
				return True

	def _check_names(self,file_path):
		'''
			check that the names are valid
		'''

		# initial_dir = os.getcwd()
		# os.chdir(self.BASE_URL+"Resources")
		with open(file_path) as csv_file:
			# os.chdir(initial_dir)
			csv_reader = csv.reader(csv_file,delimiter=',')
			line_count = 0
			self.errors = []
			for row in csv_reader:
				if any(row):
					if line_count == 0:
						line_count += 1
					else:
						names =  row[self.names_column].strip()
						names =  names.split(" ")
						if (len(names) == 1):
							self.errors.append("got only one name ("\
												+ names[0] \
												+ " ) at line "\
												+ str(line_count + 1)\
												+ " expected two or more")
						line_count += 1

			if (len(self.errors) > 0):
				return False
			else:
				return True

	def _check_projects(self,file_path):
		'''
			check that the names are valid
		'''

		# initial_dir = os.getcwd()
		# os.chdir(self.BASE_URL+"Resources")
		with open(file_path) as csv_file:
			# os.chdir(initial_dir)
			csv_reader = csv.reader(csv_file,delimiter=',')
			line_count = 0
			self.errors = []
			for row in csv_reader:
				if any(row):
					if line_count == 0:
						line_count += 1
					else:
						project =  row[self.project_column].strip()
						if (project == ""):
							self.errors.append("No project given" + "at line" + str(line_count + 1))
						line_count += 1

			if (len(self.errors) > 0):
				return False
			else:
				return True

	def _check_date(self,file_path):
		'''
			check that the date input given is of correct format
		'''
		# initial_dir = os.getcwd()
		# os.chdir(self.BASE_URL+"Resources")
		with open(file_path) as csv_file:
			# os.chdir(initial_dir)
			csv_reader = csv.reader(csv_file,delimiter=',')
			line_count = 0
			self.errors = []
			for row in csv_reader:
				if any(row):
					date = row[self.date_column]
					if line_count == 0:
						line_count += 1
					else:
						date = date.strip()
						try:
							datetime.datetime.strptime(date,'%d %B %Y')
						except:
							self.errors.append("incorrect date format ("\
												+ date \
												+ " ) at line "\
												+ str(line_count + 1) \
												+ " use format '31 March 2020'")
						#increment line count
						line_count += 1

			if (len(self.errors) > 0):
				return False
			else:
				return True

	def _check_phone_number(self,file_path):
		'''
			check that the phone number input provided is correct
		'''
		# initial_dir = os.getcwd()
		# os.chdir(self.BASE_URL+"Resources")
		with open(file_path) as csv_file:
			# os.chdir(initial_dir)
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

	def _check_amount(self,file_path):
		'''
			check that the amount given are correct
		'''
		# initial_dir = os.getcwd()
		# os.chdir(self.BASE_URL + "Resources")
		with open(file_path) as csv_file:
			# os.chdir(initial_dir)
			csv_reader = csv.reader(csv_file,delimiter=',')
			line_count = 0
			self.errors = []
			for row in csv_reader:
				if any(row):
					amount = row[self.amount_column]
					if line_count == 0:
						line_count += 1
					else:
						amount = amount.strip()
						try:
							amount = str(amount)
							amount = amount.replace(',','')#remove commas and try converting to int
							int(int(amount))
						except ValueError:
							self.errors.append("incorrect amount format ("\
												+ amount \
												+ " )at line "\
												+ str(line_count + 1)\
												+ " use integer format for amounts")
						line_count += 1

			if (len(self.errors) > 0):
				return False
			else:
				return True

	def _check_pledge_amount(self,file_path):
			'''
				check that the amount given are correct
			'''
			# initial_dir = os.getcwd()
			# os.chdir(self.BASE_URL + "Resources")
			with open(file_path) as csv_file:
				# os.chdir(initial_dir)
				csv_reader = csv.reader(csv_file,delimiter=',')
				line_count = 0
				self.errors = []
				for row in csv_reader:
					if any(row):
						amount = row[self.pledge_amount_column]
						if line_count == 0:
							line_count += 1
						else:
							amount = amount.strip()
							try:
								amount = str(amount)
								amount = amount.replace(',','')#remove commas and try converting to int
								int(int(amount))
							except ValueError:
								self.errors.append("incorrect amount format ("\
													+ amount \
													+ " )at line "\
													+ str(line_count + 1)\
													+ " use integer format for amounts")
							line_count += 1

				if (len(self.errors) > 0):
					return False
				else:
					return True

	def _member_from_phone_number(self,phone_number):
		if len(phone_number) == 10:
			if MemberContact.objects.filter(phone__contains=phone_number[1:10]).exists():
				contact =  MemberContact.objects.filter(phone__contains=phone_number[1:10])[0]
				return contact.member
			else:
				return None

		if len(phone_number) == 9:
			if MemberContact.objects.filter(phone__contains=phone_number[1:9]).exists():
				contact =  MemberContact.objects.filter(phone__contains=phone_number[1:9])[0]
				return contact.member
			else:
				return None

	#public methods
	def set_base_url(self,base_url):
		self.BASE_URL = base_url.split(':')[0] + "/"

	def preview_CSV(self, file_path):
		'''
			return the csv as json for preview in the UI
		'''
		# initial_dir = os.getcwd()
		# os.chdir(self.BASE_URL+"Resources")

		data = []
		with open(file_path) as csv_file:
			# os.chdir(initial_dir)
			csv_reader = csv.DictReader(csv_file,delimiter=',')
			row = {}
			count = 0
			for row in csv_reader:
				if count < 1000:
					row = row
					data.append(row)
					count += 1
				else:
					break
		return data

	def configure_CSV(self, file_path, config_tuple):
		'''
			configure the csv file columns according to specifications by the config_tuple
		'''
		self.amount_column = None
		self.pledge_amount_column = None
		self.project_column = None
		self.phone_number_column = None
		self.names_column = None
		self.date_column = None

		# initial_dir = os.getcwd()
		# os.chdir(self.BASE_URL+"Resources")
		with open(file_path) as csv_file:
			# os.chdir(initial_dir)
			csv_reader = csv.reader(csv_file,delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
					for key in config_tuple:
						for i in range(0,len(row)):
							if row[i].strip() == key.strip():
								if config_tuple[key] == 'project':
									self.project_column = i
								if config_tuple[key] == 'amount':
									self.amount_column = i
								if config_tuple[key] == 'pledge amount':
									self.pledge_amount_column = i
								if config_tuple[key] == 'phone number':
									self.phone_number_column = i
								if config_tuple[key] == 'names':
									self.names_column = i
								if config_tuple[key] == 'date':
									self.date_column = i
				else:
					break
				line_count += 1

	def check_CSV(self, file_path):
		'''
			check if CSV meets the required standards
		'''
		if (not self._check_size_of_file(file_path)):
			return False

		if (not self._check_names(file_path)):
			return False

		if (not self._check_date(file_path)):
			return False

		if (not self._check_amount(file_path)):
			return False

		if (not self._check_pledge_amount(file_path)):
			return False

		if (self.phone_number_column != None):
			if (not self._check_phone_number(file_path)):
				return False

		if (not self._check_projects(file_path)):
			return False
		#if everything is okay then return True
		return True

	# TODO: review length of this function
	def add_pledge_payments(self,schema,file_path):
		'''
			load a csv file and get its detail
		'''
		# initial_dir = os.getcwd()
		# os.chdir(self.BASE_URL + "Resources")
		with open(file_path) as csv_file:
			# os.chdir(initial_dir)
			csv_reader = csv.reader(csv_file,delimiter=',')
			line_count = 0
			member_id = 0
			for row in csv_reader:
				if line_count == 0:
					line_count += 1
				else:
					#get amount
					amount = None
					if (self.amount_column != None):
						amount = row[self.amount_column]
						amount = str(amount)
						amount = int(amount.replace(',',''))
					# get phone_number
					phone_number = None
					if (self.phone_number_column != None):
						phone_number = row[self.phone_number_column]
					# get date
					date = None
					if (self.date_column != None):
						date = row[self.date_column]
						date = date.strip()
						date = datetime.datetime.strptime(date,'%d %B %Y')
					# get names
					names =  row[self.names_column].strip()

					#only do this if we have a phone number
					if phone_number:
						# try get the pledge
						pledge_amount = int(row[self.pledge_amount_column])
						payment_amount = int(row[self.amount_column])
						project_name = row[self.project_column]
						project,created = Project.objects.get_or_create(project_name.strip())
						member = self._member_from_phone_number(phone_number)
						if member:
							pledge,created = Pledge.objects.get_or_create(
								project=project,
								member=member,
								phone=phone_number,
							)
							pledge.amount = pledge_amount
							pledge.save()
						else:
							pledge,created = Pledge.objects.get_or_create(
								project=project,
								phone=phone_number,
							)
							pledge.names = names
							pledge.amount = pledge_amount
							pledge.save()

						new_payment = PledgePayment.objects.create(
							pledge=pledge,
							payment_amount=payment_amount
						)
