from django import forms

from .models import CustomerAccount


class CustomerAccountForm(forms.ModelForm):
    """
    This class will allow the account form
    to be rendered directly from the model
    and allow django to handle the validation.
    """
    class Meta:
        """
        Meta class to define the model the form
        will render from and the specific fields
        that need to be rendered.
        """
        model = CustomerAccount
        # Exclude user field as should never be amended.
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        This function changes the form placeholders and
        adds class widgets to form fields in order
        to be inkeeping with the visual style of the site.
        """
        # Calling default init method to call the form as it
        # it is by default.
        super().__init__(*args, **kwargs)
        # This is a dictionary of placeholders to replace the fields
        # from the model as they are unfriendly to the user.
        placeholders = {
            'account_street_address1': 'Enter the first line of your address',
            'account_street_address2': 'Enter the second line of your address',
            'account_postcode': 'Postcode',
            'account_town_or_city': 'Town/City',
            'account_county': 'County',
        }

        # Setting autofocus on first field to true.
        self.fields['account_street_address1'].widget.attrs['autofocus'] = True

        # Loop through fields in model form and if required, append an asterix
        # to indicate required status of field.
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]

            # Loop through all fields and set the placeholder attribute to
            # the relevant value from dictionary via a widget.
            self.fields[field].widget.attrs['placeholder'] = placeholder

            # Looping through all fields and adding class to fields via widget.
            self.fields[field].widget.attrs['class'] = 'custom-account-form'

            # Looping through fields and setting the label attribute to false
            # as there is no requriement for labels due to the placeholders.
            self.fields[field].label = False
