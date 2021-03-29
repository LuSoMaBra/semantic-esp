
def get_sites_to_recover():
    sites = []
    sites.append({'titulo': 'Instituições de Ensino Superior', 'url': 'https://dados.gov.pt/pt/datasets/r/59ed02b9-410c-4f68-81ef-a3755ca66400', 'tipo': 'json'})
    sites.append({'titulo': 'Classificação Nacional', 'url': 'https://dados.gov.pt/pt/datasets/r/1b8c4f59-a102-4cf3-9347-a2fca406762d', 'tipo': 'json'})

    # para ver com calma
    sites.append({'titulo': 'Indicadores de docentes', 'url': 'https://dados.gov.pt/pt/datasets/indicadores-relativos-a-docentes-no-sistema-de-educacao-e-formacao', 'tipo': 'xls'})

    # para ver com calma
    sites.append({'titulo': 'Doutoramentos', 'url': 'https://dados.gov.pt/pt/datasets/r/6e923177-f1ce-4126-8107-9e2d3969abd1', 'tipo': 'xls'})

    # interessante para promover decisão
    sites.append({'titulo': 'Volume de negócios das empresas', 'url': 'https://dados.gov.pt/pt/datasets/r/61882622-51b4-4ddc-adbc-5d34913e8972', 'tipo': 'xls'})
    sites.append({'titulo': 'Número de empresas', 'url': 'https://dados.gov.pt/pt/datasets/r/98271e8f-d65f-4828-8eaf-d3ba63738035', 'tipo': 'xls'})

    sites.append({'titulo': '1ª Fase - Médias de Ingresso no Acesso ao Ensino Superior', 'url': 'https://orientacao-vocacional.com.pt/wp-content/uploads/documentos/media_2020_1.pdf', 'tipo': 'pdf'})
    sites.append({'titulo': '2ª Fase - Médias de Ingresso no Acesso ao Ensino Superior', 'url': 'https://orientacao-vocacional.com.pt/wp-content/uploads/documentos/media_2020_2.pdf', 'tipo': 'pdf'})

    return sites

