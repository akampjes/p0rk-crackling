from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from models import *

class JobForm(ModelForm):
	class Meta:
		model = Job
		fields = ("hashType", "attackType", "hashes")
