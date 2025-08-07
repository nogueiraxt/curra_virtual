# curral/forms.py

from django import forms
from .models import Vaca, Ordenha
from datetime import date

class VacaForm(forms.ModelForm):
    class Meta:
        model = Vaca
        fields = ['nome', 'data_nascimento', 'pai', 'mae']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class OrdenhaForm(forms.ModelForm):
    data_ordenha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data da Ordenha')
    hora_ordenha = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Hora da Ordenha')

    class Meta:
        model = Ordenha
        fields = ['vaca', 'quantidade_leite']

    def save(self, commit=True):
        instance = super().save(commit=False)
        data_hora_combinada = f"{self.cleaned_data['data_ordenha']} {self.cleaned_data['hora_ordenha']}"
        instance.data_hora = data_hora_combinada
        if commit:
            instance.save()
        return instance

class RelatorioForm(forms.Form):
    data_inicio = forms.DateField(
        label='Data de Início',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        initial=date.today
    )
    data_fim = forms.DateField(
        label='Data de Fim',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        initial=date.today
    )
    vaca = forms.ModelChoiceField(
        queryset=Vaca.objects.all(),
        label='Selecionar Vaca',
        required=False,
        empty_label='Todas as Vacas'
    )
    
class OrdenhaFiltroForm(forms.Form):
    data_inicio = forms.DateField(
        label='De:',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    data_fim = forms.DateField(
        label='Até:',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )