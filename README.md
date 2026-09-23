# TCC-Univesp
Repositório para TCC da Univesp


Base	O que possui	PF	API/CSV	Granularidade
Banco Central – SCR.data	Crédito, inadimplência, saldo, modalidades	✅	CSV	Agregada
BCB – Inadimplência PF	Percentual de inadimplência	✅	CSV/API	Brasil/UF/modalidade
BCB – Endividamento das famílias	Endividamento e comprometimento da renda	✅	CSV/API	Agregada
BCB – Comprometimento de renda	Quanto da renda está comprometida com dívidas	✅	CSV/API	Agregada
CADIN	Pessoas/empresas com débitos perante órgãos públicos	✅	API restrita	Cadastro individual, acesso controlado
Desenrola Brasil	Dados agregados de operações renegociadas	✅	CSV	Agregada


# Banco Central
Serie Code:
    21082 = Inadimplência da carteira de crédito - Total
    21084 = Inadimplência da carteira de crédito - Pessoas físicas - Total
    21119 = Inadimplência da carteira de crédito com recursos livres - Pessoas físicas - Cartão de crédito total
    29038 = Endividamento das famílias com o Sistema Financeiro Nacional exceto crédito habitacional em relação à renda acumulada dos últimos 12 meses (RNDBF)

Taxa de inadimplência por estado:
    Estados:
        26771 = Tocantins
        26769 = Sergipe
        26766 = Roraima
        26765 = Rondônia
        26762 = Paraná
        26761 = Piauí
        26760 = Pernambuco
        26759 = Paraíba
        26758 = Pará
        26754 = Maranhão
        26753 = Goiás
        26750 = Ceará
        26749 = Bahia
        26748 = Amapá
        26747 = Amazonas
        26746 = Alagoas
        26745 = Acre
        26770 = São Paulo
        26768 = Santa Catarina
        26757 = Mato Grosso
        26755 = Minas Gerais
        26752 = Espírito Santo
        26751 = Distrito Federal
        26763 = Rio de Janeiro
        26756 = Mato Grosso do Sul
        26764 = Rio Grande do Norte
