from django import forms


class InputForm(forms.Form):
    pokemon = forms.CharField(label='Pokémon')
    level = forms.IntegerField(label='level')
