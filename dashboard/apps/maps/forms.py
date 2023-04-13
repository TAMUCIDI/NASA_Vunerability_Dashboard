from django import forms
from apps.maps.models import Maps
from apps.maps.data.constants import AREA_CHOICES
def restore_MSDM_Weight_From_Session(request):
    weight_dict = {
        'Speed90Weight': (float)(request.POST['Speed90Weight']),
        'ShorelineDistWeight': (float)(request.POST['ShorelineDistWeight']),
        'MilitaryDistWeight': (float)(request.POST['MilitaryDistWeight']),
        'Landing19Weight': (float)(request.POST['Landing19Weight']),
        'Landing20Weight': (float)(request.POST['Landing20Weight']),
        'Landing21Weight': (float)(request.POST['Landing21Weight']),
    }
    return WSDMWeightForm(weight_dict)

def restore_TOPSIS_Weight_From_Session(request):
    weight_form = {
        'Speed90Weight': (float)(request.POST['Speed90Weight']),
        'ShorelineDistWeight': (float)(request.POST['ShorelineDistWeight']),
        'MilitaryDistWeight': (float)(request.POST['MilitaryDistWeight']),
        'Landing19Weight': (float)(request.POST['Landing19Weight']),
        'Landing20Weight': (float)(request.POST['Landing20Weight']),
        'Landing21Weight': (float)(request.POST['Landing21Weight']),
    }
    return TopsisWeightForm(weight_form)
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