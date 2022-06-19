from django import forms
from apps.maps.models import Maps

class MapForm(forms.Form):
    Speed90 = forms.FloatField(
        label='Weight of Wind Speed 90m ',
        widget=forms.NumberInput(
            attrs={
                'onchange': 'form.submit();'
            }
        )
    )

    ShorelineDist = forms.FloatField(
        label='Weight of Shoreline Distance ',
        widget=forms.NumberInput(
            attrs={
                'onchange': 'form.submit();'
            }
        )
    )

    MiliratyDist = forms.FloatField(
        label='Weight of Military Distance ',
        widget=forms.NumberInput(
            attrs={
                'onchange': 'form.submit();'
            }
        )
    )

    Landing19 = forms.FloatField(
        label='Weight of Landing in 2019 ',
        widget=forms.NumberInput(
            attrs={
                'onchange': 'form.submit();'
            }
        )
    )