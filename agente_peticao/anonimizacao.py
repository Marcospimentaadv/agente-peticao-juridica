# Copyright (c) 2026 Marcos Vinícius Pimenta. Todos os direitos reservados.
# Módulo publicado apenas para demonstração. Uso, cópia ou redistribuição
# exigem licença comercial. Veja o arquivo LICENSE.

"""Mascaramento de dados pessoais antes do envio ao modelo (LGPD).

Substitui identificadores diretos por marcadores. O mapeamento fica só na
memória da execução local e permite restaurar os dados na minuta final.
"""

import re

PADROES = {
    "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "CNPJ": r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b",
    "EMAIL": r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
    "TELEFONE": r"\(?\b\d{2}\)?\s?9?\d{4}-?\d{4}\b",
    "PROCESSO": r"\b\d{7}-?\d{2}\.?\d{4}\.?\d\.?\d{2}\.?\d{4}\b",
}


def anonimizar(texto: str, nomes: list[str] | None = None) -> tuple[str, dict[str, str]]:
    """Retorna o texto mascarado e o mapa marcador -> valor original."""
    mapa: dict[str, str] = {}
    contadores: dict[str, int] = {}

    def substituir(tipo: str, valor: str) -> str:
        for marcador, original in mapa.items():
            if original == valor:
                return marcador
        contadores[tipo] = contadores.get(tipo, 0) + 1
        marcador = f"[{tipo}_{contadores[tipo]}]"
        mapa[marcador] = valor
        return marcador

    # Processo antes de CPF/CNPJ para não ser quebrado por padrões menores.
    for tipo in ("PROCESSO", "CNPJ", "CPF", "EMAIL", "TELEFONE"):
        texto = re.sub(PADROES[tipo], lambda m, t=tipo: substituir(t, m.group(0)), texto)

    for nome in sorted(nomes or [], key=len, reverse=True):
        if nome.strip():
            texto = re.sub(re.escape(nome), lambda m: substituir("PARTE", m.group(0)), texto, flags=re.IGNORECASE)

    return texto, mapa


def restaurar(texto: str, mapa: dict[str, str]) -> str:
    """Devolve os dados originais no lugar dos marcadores."""
    for marcador, original in mapa.items():
        texto = texto.replace(marcador, original)
    return texto
