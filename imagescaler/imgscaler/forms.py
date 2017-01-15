from django import forms
import os
 
class UserForm(forms.Form):
    user_file = forms.FileField()
 
    def clean_user_file(self, *args, **kwargs):
        cleaned_data = super(UserForm,self).clean()
        user_file = cleaned_data.get("user_file")
 
        if user_file:
            if user_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File is too big.")
 
            #if not os.path.splitext(user_file.name)[1].strip().lower() in ['.jpg','.png','.gif','.jpeg']:
            #    raise forms.ValidationError("File does not look like as picture.")
 
        return user_file