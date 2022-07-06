from django import forms
from apps.maps.models import Maps
from apps.maps.data.constants import AREA_CHOICES

class MapForm(forms.Form):
    Speed90 = forms.FloatField(
        label='Weight of Wind Speed 90m ',
        widget=forms.NumberInput(),
        initial=1
    )

    ShorelineDist = forms.FloatField(
        label='Weight of Shoreline Distance ',
        widget=forms.NumberInput(),
        initial=1,
    )

    MilitaryDist = forms.FloatField(
        label='Weight of Military Distance ',
        widget=forms.NumberInput(),
        initial=1,
    )

    Landing19 = forms.FloatField(
        label='Weight of Landing in 2019 ',
        widget=forms.NumberInput(),
        initial=1,
    )

class FishingAreaChoiceForm(forms.Form):
    fishingArea = forms.MultipleChoiceField(
        choices=AREA_CHOICES,
        label="Fishing Areas ",
        widget=forms.SelectMultiple(
            attrs={'onchange':'FishingAreaForm.submit();'}
        )
    )