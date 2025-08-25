"""
Engenharia de variáveis para o SINAN: faixas etárias, binários de sintomas,
mapeamentos de rótulos e matriz de features.
"""

from __future__ import annotations
import pandas as pd
import numpy as np
from typing import List

from src.utils.helpers import SYMPTOM_COLUMNS, SEX_MAP


def add_age_bins(df: pd.DataFrame, age_col: str = "NU_IDADE_N") -> pd.DataFrame:
    df = df.copy()
    if age_col in df.columns:
        bins = [0, 5, 12, 18, 30, 45, 60, 120]
        labels = ["0-4","5-11","12-17","18-29","30-44","45-59","60+"]
        df["FAIXA_ETARIA"] = pd.cut(df[age_col], bins=bins, labels=labels, right=True)
    return df

def binarize_symptoms(df: pd.DataFrame, cols: List[str] = None) -> pd.DataFrame:
    """
    Converte colunas 1/2 (1=sim, 2=nao) em *_BIN (1/0).
    """
    df = df.copy()
    cols = cols or SYMPTOM_COLUMNS
    for c in cols:
        if c in df.columns:
            df[c + "_BIN"] = df[c].map({1: 1, 2: 0})
    # Contador de sintomas positivos no registro
    bin_cols = [c+"_BIN" for c in cols if c in df.columns]
    if bin_cols:
        df["N_SINTOMAS"] = df[bin_cols].sum(axis=1, skipna=True)
    return df

def _map_labels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "CS_SEXO" in df.columns:
        df["SEXO_TXT"] = df["CS_SEXO"].map(SEX_MAP).fillna("Ignorado")
    return df

def build_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline de features: faixas etárias + binarização de sintomas + mapeamentos.
    """
    df = add_age_bins(df)
    df = binarize_symptoms(df)
    df = _map_labels(df)
    return df
