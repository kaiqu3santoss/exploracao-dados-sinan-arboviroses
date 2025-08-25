"""
Helpers e constantes reutilizáveis para o projeto SINAN Arboviroses.
"""

from __future__ import annotations
import os
from typing import Iterable, Dict, List
import numpy as np
import pandas as pd


# Colunas de data conhecidas no SINAN (podem não existir em todos os recortes)
DATE_COLUMNS: List[str] = [
    "DT_NOTIFIC","DT_SIN_PRI","DT_INTERNA","DT_OBITO","DT_ENCERRA","DT_INVEST",
    "DT_ALRM","DT_GRAV","DT_PCR","DT_SORO","DT_NS1","DT_VIRAL","DT_CHIK_S1","DT_CHIK_S2","DT_PRNT"
]

# Colunas de sintomas 1/2 (1=sim, 2=nao) — ajuste conforme seu dicionário local
SYMPTOM_COLUMNS: List[str] = [
    "FEBRE","MIALGIA","CEFALEIA","EXANTEMA","VOMITO","NAUSEA","DOR_COSTAS","CONJUNTVIT",
    "ARTRITE","ARTRALGIA","PETEQUIA_N","LEUCOPENIA","DOR_RETRO"
]

SEX_MAP: Dict[str, str] = {"M": "Masculino", "F": "Feminino"}

def ensure_dirs(paths: Iterable[str]) -> None:
    """Garante que diretórios existam."""
    for p in paths:
        os.makedirs(p, exist_ok=True)

def to_datetime_cols(df: pd.DataFrame, cols: Iterable[str]) -> pd.DataFrame:
    """Converte múltiplas colunas para datetime (coerce)."""
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

def coerce_age(df: pd.DataFrame, col: str = "NU_IDADE_N", min_age: int = 0, max_age: int = 120) -> pd.DataFrame:
    """
    Zera idades impossíveis (fora do intervalo) para NaN.
    """
    if col in df.columns:
        mask = (df[col] < min_age) | (df[col] > max_age)
        df.loc[mask, col] = np.nan
    return df

def save_fig(path: str, dpi: int = 150) -> None:
    """Salva a figura atual do matplotlib."""
    import matplotlib.pyplot as plt
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path, dpi=dpi, bbox_inches="tight")

def value_counts_sorted(s: pd.Series, dropna: bool = False) -> pd.DataFrame:
    """Retorna contagem e proporção ordenadas (helper para tabelas rápidas)."""
    vc = s.value_counts(dropna=dropna)
    prop = s.value_counts(normalize=True, dropna=dropna)
    out = pd.DataFrame({"count": vc, "prop": prop})
    return out.sort_values("count", ascending=False)
