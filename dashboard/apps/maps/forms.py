from django import forms
Weight_Default_Dict = {
    'Female_Percent':1.0,
    'Age_Percent': 1.0,
    'Property_Percent': 1.0,
    'Education_Attainmence': 1.0,
    'LivingAlone_Percent': 1.0,
    'Minority_Percent': 1.0,
    'Unemployed_Rate': 1.0,
    'Language_Percent': 1.0,
    'RentHouse_Percent': 1.0,
    'NoVehicle_Percent': 1.0,
    'NoInsurance_Percent': 1.0,
    'Disable_Percent': 1.0,
    'Computer_Availability': 1.0,
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

    Education_Attainmence = forms.FloatField(
        label='Education_Attainmence',
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

    Unemployed_Rate = forms.FloatField(
        label='Unemployed_Rate',
        widget=forms.NumberInput(),
        initial=0.0
    )

    Language_Percent = forms.FloatField(
        label='Language_Percent',
        widget=forms.NumberInput(),
        initial=0.0
    )

    RentHouse_Percent = forms.FloatField(
        label='RentHouse_Percent',
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

    Computer_Availability = forms.FloatField(
        label='Computer_Availability',
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

    