# curral/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncDate
from decimal import Decimal
from django.contrib import messages
from datetime import timedelta

from .models import Vaca, Ordenha
from .forms import VacaForm, OrdenhaForm, RelatorioForm, OrdenhaFiltroForm


@login_required
def lista_vacas(request):
    vacas = Vaca.objects.all().order_by('nome')

    for vaca in vacas:
        ordenhas_da_vaca = Ordenha.objects.filter(vaca=vaca)
        dias_com_ordenha_set = set()
        for ordenha in ordenhas_da_vaca:
            dias_com_ordenha_set.add(ordenha.data_hora.date())
        total_dias = len(dias_com_ordenha_set)

        if total_dias > 0:
            producao_total = ordenhas_da_vaca.aggregate(Sum('quantidade_leite'))['quantidade_leite__sum']
            vaca.media_diaria = producao_total / Decimal(total_dias)
        else:
            vaca.media_diaria = Decimal('0.00')

    context = {
        'vacas': vacas,
        'titulo_pagina': 'Lista de Vacas'
    }
    return render(request, 'curral/lista_vacas.html', context)


@login_required
def detalhe_vaca(request, pk):
    vaca = get_object_or_404(Vaca, pk=pk)

    filtro_form = OrdenhaFiltroForm(request.GET)
    ordenhas = Ordenha.objects.filter(vaca=vaca).order_by('-data_hora')

    if filtro_form.is_valid():
        data_inicio = filtro_form.cleaned_data.get('data_inicio')
        data_fim = filtro_form.cleaned_data.get('data_fim')
        if data_inicio:
            ordenhas = ordenhas.filter(data_hora__date__gte=data_inicio)
        if data_fim:
            ordenhas = ordenhas.filter(data_hora__date__lte=data_fim)

    producao_total = ordenhas.aggregate(Sum('quantidade_leite'))['quantidade_leite__sum'] or Decimal('0.00')
    dias_com_ordenha_set = set()
    for ordenha in ordenhas:
        dias_com_ordenha_set.add(ordenha.data_hora.date())
    dias_com_ordenha = len(dias_com_ordenha_set)

    media_diaria = Decimal('0.00')
    if dias_com_ordenha > 0:
        media_diaria = producao_total / Decimal(dias_com_ordenha)

    ordenhas_por_dia = {}
    for ordenha in ordenhas:
        dia = ordenha.data_hora.date()
        if dia not in ordenhas_por_dia:
            ordenhas_por_dia[dia] = []
        ordenhas_por_dia[dia].append(ordenha)

    context = {
        'vaca': vaca,
        'filtro_form': filtro_form,
        'producao_total': producao_total,
        'media_diaria': media_diaria,
        'ordenhas_por_dia': ordenhas_por_dia,
        'titulo_pagina': f'Detalhes da Vaca: {vaca.nome}'
    }
    return render(request, 'curral/detalhe_vaca.html', context)


@login_required
def cadastrar_vaca(request):
    if request.method == 'POST':
        form = VacaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaca cadastrada com sucesso!')
            return redirect('lista_vacas')
    else:
        form = VacaForm()

    context = {
        'form': form,
        'titulo_pagina': 'Cadastrar Nova Vaca'
    }
    return render(request, 'curral/cadastrar_vaca.html', context)


@login_required
def cadastrar_ordenha(request):
    vaca_id = request.GET.get('vaca')
    vaca_obj = None
    if vaca_id:
        try:
            vaca_obj = get_object_or_404(Vaca, pk=vaca_id)
        except Vaca.DoesNotExist:
            messages.error(request, 'A vaca selecionada não existe.')
            return redirect('lista_vacas')

    if request.method == 'POST':
        form = OrdenhaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ordenha registrada com sucesso!')
            if vaca_obj:
                return redirect('detalhe_vaca', pk=vaca_obj.pk)
            else:
                return redirect('lista_vacas')
    else:
        initial = {'vaca': vaca_obj} if vaca_obj else {}
        form = OrdenhaForm(initial=initial)

    context = {
        'form': form,
        'titulo_pagina': 'Registrar Ordenha'
    }
    return render(request, 'curral/cadastrar_ordenha.html', context)


@login_required
def editar_ordenha(request, pk):
    ordenha = get_object_or_404(Ordenha, pk=pk)
    try:
        vaca_pk = ordenha.vaca.pk
    except Vaca.DoesNotExist:
        messages.error(request, 'Ordenha vinculada a uma vaca que não existe.')
        return redirect('lista_vacas')

    if request.method == 'POST':
        form = OrdenhaForm(request.POST, instance=ordenha)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ordenha atualizada com sucesso!')
            return redirect('detalhe_vaca', pk=vaca_pk)
    else:
        initial = {
            'vaca': ordenha.vaca,
            'quantidade_leite': ordenha.quantidade_leite,
            'data_ordenha': ordenha.data_hora.date().strftime('%Y-%m-%d'),
            'hora_ordenha': ordenha.data_hora.time()
        }
        form = OrdenhaForm(initial=initial)

    context = {
        'form': form,
        'ordenha': ordenha,
        'titulo_pagina': 'Editar Ordenha'
    }
    return render(request, 'curral/editar_ordenha.html', context)


@login_required
def deletar_ordenha(request, pk):
    ordenha = get_object_or_404(Ordenha, pk=pk)
    try:
        vaca_pk = ordenha.vaca.pk
    except Vaca.DoesNotExist:
        messages.error(request, 'Ordenha vinculada a uma vaca que não existe.')
        return redirect('lista_vacas')

    if request.method == 'POST':
        ordenha.delete()
        messages.success(request, 'Ordenha excluída com sucesso!')
        return redirect('detalhe_vaca', pk=vaca_pk)

    context = {
        'ordenha': ordenha,
        'titulo_pagina': 'Excluir Ordenha'
    }
    return render(request, 'curral/deletar_ordenha.html', context)


@login_required
def relatorio_geral(request):
    form = RelatorioForm(request.GET)
    vacas_com_producao = []

    if form.is_valid():
        data_inicio = form.cleaned_data.get('data_inicio')
        data_fim = form.cleaned_data.get('data_fim')
        vaca_selecionada = form.cleaned_data.get('vaca')

        vacas_a_analisar = []
        if vaca_selecionada:
            vacas_a_analisar.append(vaca_selecionada)
        else:
            vacas_a_analisar = Vaca.objects.all()

        for vaca in vacas_a_analisar:
            ordenhas_da_vaca = Ordenha.objects.filter(vaca=vaca).order_by('-data_hora')

            if data_inicio:
                ordenhas_da_vaca = ordenhas_da_vaca.filter(data_hora__date__gte=data_inicio)
            if data_fim:
                ordenhas_da_vaca = ordenhas_da_vaca.filter(data_hora__date__lte=data_fim)

            if ordenhas_da_vaca.exists():
                producao_total = ordenhas_da_vaca.aggregate(Sum('quantidade_leite'))['quantidade_leite__sum'] or Decimal('0.00')
                dias_com_ordenha = ordenhas_da_vaca.values('data_hora__date').distinct().count()

                media_diaria = Decimal('0.00')
                if dias_com_ordenha > 0:
                    media_diaria = producao_total / Decimal(dias_com_ordenha)

                vacas_com_producao.append({
                    'nome': vaca.nome,
                    'producao_total': producao_total,
                    'media_diaria': media_diaria
                })

    context = {
        'form': form,
        'vacas_com_producao': vacas_com_producao,
        'titulo_pagina': 'Relatório Geral de Produção'
    }
    return render(request, 'curral/relatorio_geral.html', context)