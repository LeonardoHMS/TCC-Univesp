from django.shortcuts import render

from fontes.models import FonteDados
from indicadores.models import Indicador, ValorIndicador
from localidades.models import Localidade


def home(request):
    indicadores = Indicador.objects.filter(ativo=True).order_by('nome')[:6]
    ultimo_valor = (
        ValorIndicador.objects.select_related('indicador', 'fonte', 'localidade', 'periodo')
        .order_by('-periodo__data_referencia')
        .first()
    )
    return render(
        request,
        'home.html',
        {
            'indicadores': indicadores,
            'ultimo_valor': ultimo_valor,
            'pagina': 'início',
        },
    )


def dashboard(request):
    indicadores = Indicador.objects.filter(ativo=True).order_by('nome')
    categorias = sorted({item.categoria for item in indicadores})
    estados = Localidade.objects.filter(tipo='Estado').order_by('nome')
    regioes = Localidade.objects.filter(tipo='Região').order_by('nome')
    fontes = FonteDados.objects.filter(ativo=True).order_by('nome')

    queryset = ValorIndicador.objects.select_related('indicador', 'fonte', 'localidade', 'periodo')

    selected_indicator = request.GET.get('indicador')
    selected_category = request.GET.get('categoria')
    periodo_inicial = request.GET.get('periodo_inicial')
    periodo_final = request.GET.get('periodo_final')
    regiao = request.GET.get('regiao')
    estado = request.GET.get('estado')
    fonte = request.GET.get('fonte')
    if selected_indicator:
        queryset = queryset.filter(indicador_id=selected_indicator)
    if selected_category:
        queryset = queryset.filter(indicador__categoria=selected_category)
    if periodo_inicial:
        queryset = queryset.filter(periodo__data_referencia__gte=periodo_inicial)
    if periodo_final:
        queryset = queryset.filter(periodo__data_referencia__lte=periodo_final)
    if regiao:
        queryset = queryset.filter(localidade__regiao=regiao)
    if estado:
        queryset = queryset.filter(localidade_id=estado)
    if fonte:
        queryset = queryset.filter(fonte_id=fonte)

    selected_fonte_label = None
    if fonte:
        selected_fonte_label = FonteDados.objects.filter(pk=fonte).values_list('instituicao', flat=True).first()

    tabela = list(queryset.order_by('-periodo__data_referencia', 'localidade__nome')[:40])

    if selected_indicator:
        dados = queryset.order_by('periodo__data_referencia')
        primeiro = dados.first()
        ultimo = dados.last()
        valor_mais_recente = ultimo.valor if ultimo else None
        variacao = None
        if primeiro and ultimo and primeiro.valor != 0:
            variacao = ((ultimo.valor - primeiro.valor) / abs(primeiro.valor)) * 100
    else:
        valor_mais_recente = None
        variacao = None

    chart_data = {'labels': [], 'datasets': []}
    if selected_indicator:
        chart_labels = []
        chart_label_by_date = {}
        chart_series = {}
        for item in queryset.order_by('periodo__data_referencia', 'localidade__nome'):
            date_key = item.periodo.data_referencia.isoformat()
            if date_key not in chart_label_by_date:
                chart_label_by_date[date_key] = item.periodo.data_referencia.strftime('%m/%Y')
                chart_labels.append(date_key)

            locality = item.localidade.nome
            chart_series.setdefault(locality, {})[date_key] = float(item.valor)

        chart_data = {
            'labels': [chart_label_by_date[date_key] for date_key in chart_labels],
            'datasets': [
                {
                    'label': locality,
                    'data': [values.get(date_key) for date_key in chart_labels],
                    'borderWidth': 2,
                    'tension': 0.25,
                    'fill': False,
                }
                for locality, values in chart_series.items()
            ],
        }

    linha = []
    for item in tabela:
        linha.append({
            'indicador': item.indicador.nome,
            'valor': item.valor,
            'periodo': str(item.periodo),
            'localidade': item.localidade.nome,
            'fonte': item.fonte.instituicao,
        })

    return render(
        request,
        'dashboard.html',
        {
            'indicadores': indicadores,
            'categorias': categorias,
            'estados': estados,
            'regioes': regioes,
            'fontes': fontes,
            'tabela': linha,
            'valor_mais_recente': valor_mais_recente,
            'variacao': variacao,
            'selected_indicator': selected_indicator,
            'selected_category': selected_category,
            'periodo_inicial': periodo_inicial,
            'periodo_final': periodo_final,
            'selected_regiao': regiao,
            'selected_estado': estado,
            'selected_fonte': fonte,
            'selected_fonte_label': selected_fonte_label,
            'chart_data': chart_data,
            'regiao': regiao,
            'estado': estado,
            'fonte': fonte,
            'pagina': 'dashboard',
        },
    )


def indicadores_page(request):
    indicadores = Indicador.objects.filter(ativo=True).order_by('nome')
    return render(request, 'indicadores.html', {'indicadores': indicadores, 'pagina': 'indicadores'})


def fontes_page(request):
    fontes = FonteDados.objects.filter(ativo=True).order_by('nome')
    return render(request, 'fontes.html', {'fontes': fontes, 'pagina': 'fontes'})


def about(request):
    return render(request, 'about.html', {'pagina': 'sobre'})
