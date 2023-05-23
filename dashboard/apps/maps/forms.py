from django import forms
Weight_Default_Dict = {
    'Female_Percent':1.0,
    'Age_Percent': 1.0,
    'Property_Percent': 1.0,
    'NoDiploma_Percent': 1.0,
    'LivingAlone_Percent': 1.0,
    'Minority_Percent': 1.0,
    'Unemployed_Percent': 1.0,
    'Language_Percent': 1.0,
    'Rent_Percent': 1.0,
    'NoVehicle_Percent': 1.0,
    'NoInsurance_Percent': 1.0,
    'Disable_Percent': 1.0,
    'Computer_Percent': 1.0,
    'NoInternet_Percent': 1.0,
    'NoPhone_Percent': 1.0,
}
class WeightForm(forms.Form):
    Female_Percent = forms.FloatField(
        label='Female_Percent',
        widget=forms.NumberInput(),
        initial=1.0
    )

    Age_Percent = forms.FloatField(
        label='Age_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    Property_Percent = forms.FloatField(
        label='Property_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoDiploma_Percent = forms.FloatField(
        label='NoDiploma_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    LivingAlone_Percent = forms.FloatField(
        label='LivingAlone_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    Minority_Percent = forms.FloatField(
        label='Minority_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    Unemployed_Percent = forms.FloatField(
        label='Unemployed_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    Language_Percent = forms.FloatField(
        label='Language_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    Rent_Percent = forms.FloatField(
        label='Rent_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoVehicle_Percent = forms.FloatField(
        label='NoVehicle_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoInsurance_Percent = forms.FloatField(
        label='NoInsurance_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    Disable_Percent = forms.FloatField(
        label='Disable_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    Computer_Percent = forms.FloatField(
        label='Computer_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoInternet_Percent = forms.FloatField(
        label='NoInternet_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoPhone_Percent = forms.FloatField(
        label='NoPhone_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    