from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import NewsListing

class UpdateUserForm(forms.Form):
    update_user_select = forms.ModelChoiceField(
        label="Username",
        queryset=User.objects.filter(is_superuser=False))
    update_user_token    = forms.CharField(label="Token ID", required=False)
    update_user_secrecy  = forms.IntegerField(label="Secrecy Level")
    
    def clean(self):
        # STUDENT TODO
        # This is where the "update user" form is validated.
        # The "cleaned_data" is a dictionary with the data
        # entered from the POST request. So, for example,
        # cleaned_data["update_user_secrecy"] returns that
        # form value. You need to update this method to
        # enforce the security policies related to tokens
        # and secrecy.
        # Return a "ValidationError(<err msg>)" if something 
        # is wrong

        #Validation Error if update_user_secrecy is less than the user's current level
        #have to find their current level though

        cleaned_data = super().clean()
        return cleaned_data
        
class CreateNewsForm(forms.Form):
    new_news_query = forms.CharField(label="New Query", required=False)
    new_news_sources = forms.CharField(label="Sources", required=False)
    new_news_secrecy = forms.IntegerField(label="Secrecy Level", required=False)
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.user_secrecy = 0
    
    def clean(self):
        # STUDENT TODO
        # This is where newslisting update form is validated.
        # The "cleaned_data" is a dictionary with the data
        # entered from the POST request. So, for example,
        # cleaned_data["new_news_query"] returns that
        # form value. You need to update this method to
        # enforce the security policies related to tokens
        # and secrecy.
        # Return a "ValidationError(<err msg>)" if something 
        # is wrong

        cleaned_data = super().clean()

        if self.user_secrecy <= cleaned_data['new_news_secrecy']:
            #print("CLEANED")
            return cleaned_data
        else:
            #print("VALIDATION ERROR")
            raise forms.ValidationError('error')
        
class UpdateNewsForm(forms.Form):
    update_news_select = forms.ModelChoiceField(
        label="Update News",
        queryset=None,
        required=False)
    update_news_query   = forms.CharField(label="Update Query", required=False)
    update_news_sources = forms.CharField(label="Update Sources", required=False)
    update_news_secrecy = forms.IntegerField(label="Update Secrecy", required=False)
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        # STUDENT TODO
        # you should change the "queryset" in update_news_select to be None.
        # then, here in the constructor, you can change it to be the filtered
        # data passed in. See this page:
        # https://docs.djangoproject.com/en/3.1/ref/forms/fields/
        # Look specifically in the section "Fields which handle relationships¶"
        # where it talks about starting with an empty queryset.
        #
        # This form is constructed in views.py. Modify this constructor to
        # accept the passed-in (filtered) queryset.

        #args[0] will be the request or None, args[1] will be queryset or None
        self.user_secrecy = 0
        if args[1] is not None:
            self.fields['update_news_select'].queryset = args[1]
    
    def clean(self):
        # STUDENT TODO
        # This is where newslisting update form is validated.
        # The "cleaned_data" is a dictionary with the data
        # entered from the POST request. So, for example,
        # cleaned_data["new_news_query"] returns that
        # form value. You need to update this method to
        # enforce the security policies related to tokens
        # and secrecy.
        # Return a "ValidationError(<err msg>)" if something 
        # is wrong

        if self.fields['update_news_select'].queryset is None:
            #print("VALIDATION ERROR")
            raise forms.ValidationError("error")

        cleaned_data = super().clean()
        #print(cleaned_data['update_news_secrecy'])

        if cleaned_data['update_news_secrecy'] is None:
            #print("CLEAN")
            cleaned_data['update_news_secrecy'] = self.user_secrecy
            return cleaned_data
        elif cleaned_data['update_news_secrecy'] == self.user_secrecy:
            #print("CLEAN")
            return cleaned_data
        else:
            #print("VALIDATION ERROR SECRECY INVALID")
            raise forms.ValidationError("User Secrecy is too high or low to create a query of this secrecy level")