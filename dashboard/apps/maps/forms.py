from django import forms
from apps.maps.models import Maps

class MapForm(forms.Form):
    Speed90 = forms.FloatField(
        label='Variables ',
        widget=forms.NumberInput(
            attrs={
                'onchange': 'form.submit();'
            }
        )
    )

    ShorelineDist = forms.FloatField(
        label='Variables ',
        widget=forms.NumberInput(
            attrs={
                'onchange': 'form.submit();'
            }
        )
    )

    MiliratyDist = forms.FloatField(
        label='Variables ',
        widget=forms.NumberInput(
            attrs={
                'onchange': 'form.submit();'
            }
        )
    )

    Landing19 = forms.FloatField(
        label='Variables ',
        widget=forms.NumberInput(
            attrs={
                'onchange': 'form.submit();'
            }
        )
    )