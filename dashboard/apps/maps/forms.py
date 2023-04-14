from django import forms
from apps.maps.models import Maps
from apps.maps.data.constants import AREA_CHOICES
def restore_MSDM_Weight_From_Session(session):
    return {
        'Speed90Weight': (float)(session['Speed90Weight']),
        'ShorelineDistWeight': (float)(session['ShorelineDistWeight']),
        'MilitaryDistWeight': (float)(session['MilitaryDistWeight']),
        'ProtectedAreaDistWeight': (float)(session['ProtectedAreaDistWeight']),
        'Landing19Weight': (float)(session['Landing19Weight']),
        'Landing20Weight': (float)(session['Landing20Weight']),
        'Landing21Weight': (float)(session['Landing21Weight']),
    }
def restore_TOPSIS_Weight_From_Session(session):
    return {
        'Speed90Weight': (float)(session['Speed90Weight']),
        'ShorelineDistWeight': (float)(session['ShorelineDistWeight']),
        'MilitaryDistWeight': (float)(session['MilitaryDistWeight']),
        'ProtectedAreaDistWeight': (float)(session['ProtectedAreaDistWeight']),
        'Landing19Weight': (float)(session['Landing19Weight']),
        'Landing20Weight': (float)(session['Landing20Weight']),
        'Landing21Weight': (float)(session['Landing21Weight']),
    }
class WSDMWeightForm(forms.Form):
    Speed90Weight = forms.FloatField(
        label='Weight of Wind Speed 90m ',
        widget=forms.NumberInput(),
        initial=1
    )

    ShorelineDistWeight = forms.FloatField(
        label='Weight of Shoreline Distance ',
        widget=forms.NumberInput(),
        initial=1,
    )

    MilitaryDistWeight = forms.FloatField(
        label='Weight of Military Distance ',
        widget=forms.NumberInput(),
        initial=1,
    )

    ProtectedAreaDistWeight = forms.FloatField(
        label='Weight of Protected Area Distance ',
        widget=forms.NumberInput(),
        initial=1,
    )

    Landing19Weight = forms.FloatField(
        label='Weight of Landing in 2019 ',
        widget=forms.NumberInput(),
        initial=1,
    )

    Landing20Weight = forms.FloatField(
        label='Weight of Landing in 2020 ',
        widget=forms.NumberInput(),
        initial=1,
    )

    Landing21Weight = forms.FloatField(
        label='Weight of Landing in 2021 ',
        widget=forms.NumberInput(),
        initial=1,
    )

class FishingAreaChoiceForm(forms.Form):
    fishingArea = forms.MultipleChoiceField(
        choices=AREA_CHOICES,
        label="Fishing Areas ",
        widget=forms.SelectMultiple()
    )

class TopsisWeightForm(forms.Form):
    Speed90Weight = forms.FloatField(
        label='Weight of Wind Speed 90m ',
        widget=forms.NumberInput(),
        initial=1
    )

    ShorelineDistWeight = forms.FloatField(
        label='Weight of Shoreline Distance ',
        widget=forms.NumberInput(),
        initial=1,
    )

    MilitaryDistWeight = forms.FloatField(
        label='Weight of Military Distance ',
        widget=forms.NumberInput(),
        initial=1,
    )
    ProtectedAreaDistWeight = forms.FloatField(
        label='Weight of Protected Area Distance ',
        widget=forms.NumberInput(),
        initial=1,
    )
    
    Landing19Weight = forms.FloatField(
        label='Weight of Landing in 2019 ',
        widget=forms.NumberInput(),
        initial=1,
    )

    Landing20Weight = forms.FloatField(
        label='Weight of Landing in 2020 ',
        widget=forms.NumberInput(),
        initial=1,
    )

    Landing21Weight = forms.FloatField(
        label='Weight of Landing in 2021 ',
        widget=forms.NumberInput(),
        initial=1,
    )