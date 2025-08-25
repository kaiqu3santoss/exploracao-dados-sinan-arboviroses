"""
Ingestão e limpeza inicial dos dados SINAN Arboviroses.
"""

from __future__ import annotations
import os
from typing import Optional
import pandas as pd
import numpy as np

from src.utils.helpers import (
    DATE_COLUMNS, to_datetime_cols, coerce_age
)


def load_raw_data(path: str, sep: str = ",", encoding: Optional[str] = None) -> pd.DataFrame:
    """
    Lê CSV bruto de data/raw.
    """
    return pd.read_csv(path, sep=sep, encoding=encoding)

def _dedupe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove possíveis duplicatas usando um conjunto de chaves conservador.
    Ajuste conforme disponibilidade/qualidade dos campos.
    """
    key_cols = [c for c in ["ID_UNIDADE","DT_NOTIFIC","ID_MUNICIP","ID_MN_RESI","ID_PAIS"] if c in df.columns]
    if key_cols:
        before = len(df)
        df = df.drop_duplicates(subset=key_cols, keep="first")
        after = len(df)
        print(f"[dedupe] removidas {before-after} duplicatas com base em {key_cols}")
    else:
        print("[dedupe] chaves não disponíveis; nenhum registro removido")
    return df

def _add_notification_delay(df: pd.DataFrame) -> pd.DataFrame:
    """Cria coluna ATRASO_NOTIF_DIAS = DT_NOTIFIC - DT_SIN_PRI, se possível."""
    if {"DT_NOTIFIC","DT_SIN_PRI"} <= set(df.columns):
        df["ATRASO_NOTIF_DIAS"] = (df["DT_NOTIFIC"] - df["DT_SIN_PRI"]).dt.days
    return df

def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpeza mínima: datas, idades válidas, duplicatas, atraso de notificação.
    """
    df = df.copy()
    df = to_datetime_cols(df, DATE_COLUMNS)
    df = coerce_age(df, "NU_IDADE_N", 0, 120)
    df = _dedupe(df)
    df = _add_notification_delay(df)
    return df

def save_interim(df: pd.DataFrame, path: str) -> None:
    """Salva CSV intermediário (p/ auditoria)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)

def save_processed(df: pd.DataFrame, path: str) -> None:
    """Salva CSV final (features prontas para análise/modelo)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
