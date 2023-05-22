from django import forms

class WeightForm(forms.Form):
    Female_Percent_Weight = forms.FloatField(
        label='Female Population Percentage Weight',
        widget=forms.NumberInput(),
        initial=1.0
    )

    AgePercentWeight = forms.FloatField(
        label='Elder and Young Population Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    PropertyPercentWeight = forms.FloatField(
        label='Property Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoDiplomaPercentWeight = forms.FloatField(
        label='Low Education Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    LivingAlonePercentWeight = forms.FloatField(
        label='Living Alone Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    MinorityPercentWeight = forms.FloatField(
        label='Minority Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    UnemploymentPercentWeight = forms.FloatField(
        label='Unemployment Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    LanguagePercentWeight = forms.FloatField(
        label='Language Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    RentPercentWeight = forms.FloatField(
        label='Rent Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoVehiclePercentWeight = forms.FloatField(
        label='No Vehicle Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoInsurancePercentWeight = forms.FloatField(
        label='No Insurance Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    DisablePercentWeight = forms.FloatField(
        label='Disable Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    ComputerPercentWeight = forms.FloatField(
        label='Computer Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoInternetPercentWeight = forms.FloatField(
        label='No Internet Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    NoPhonePercentWeight = forms.FloatField(
        label='No Phone Percentage Weight',
        widget=forms.NumberInput(),
        initial=0.0
    )

    