from django import forms
from apps.maps.models import Maps
from apps.maps.data.constants import AREA_CHOICES

class MapForm(forms.Form):
    fishingArea = forms.ChoiceField(
        choices=AREA_CHOICES, 
        label="Fishing Areas ", 
        widget=forms.Select()
    )
    Speed90 = forms.FloatField(
        label='Weight of Wind Speed 90m ',
        widget=forms.NumberInput()
    )

    ShorelineDist = forms.FloatField(
        label='Weight of Shoreline Distance ',
        widget=forms.NumberInput()
    )

    MilitaryDist = forms.FloatField(
        label='Weight of Military Distance ',
        widget=forms.NumberInput()
    )

    Landing19 = forms.FloatField(
        label='Weight of Landing in 2019 ',
        widget=forms.NumberInput()
    )