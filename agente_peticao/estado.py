from typing import TypedDict


class EstadoPeticao(TypedDict, total=False):
    caso: str              # descrição do caso (já anonimizada)
    tipo_peca: str         # ex.: "petição inicial", "contestação", "recurso de apelação"
    area: str              # ex.: "cível", "trabalhista", "família"
    analise: str           # fatos, partes, teses, pedidos e lacunas
    consultas: list[str]   # buscas de jurisprudência geradas
    resultados: list[dict] # resultados brutos da web (titulo, url, trecho)
    jurisprudencia: str    # julgados selecionados, com link
    estrutura: str         # roteiro da peça
    minuta: str            # texto da petição
    pendencias: list[str]  # problemas apontados pela revisão
    aprovado: bool
    versao: int
