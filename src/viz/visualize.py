"""
Funções de visualização padronizadas para o projeto.
"""

from __future__ import annotations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_age_hist(df: pd.DataFrame, age_col: str = "NU_IDADE_N", ax=None, bins=20, title="Distribuição da Idade"):
    s = df[age_col].dropna()
    if ax is None:
        plt.figure(figsize=(8,4))
        ax = plt.gca()
    sns.histplot(s, bins=bins, kde=True, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Idade")
    ax.set_ylabel("Frequência")
    return ax

def plot_age_boxplot(df: pd.DataFrame, age_col: str = "NU_IDADE_N", ax=None, title="Boxplot da Idade"):
    s = df[age_col].dropna()
    if ax is None:
        plt.figure(figsize=(6,4))
        ax = plt.gca()
    sns.boxplot(y=s, ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Idade")
    return ax

def plot_weekly_cases(df: pd.DataFrame, date_col: str = "DT_SIN_PRI", ax=None, title="Casos por Semana (DT_SIN_PRI)"):
    if date_col not in df.columns:
        raise ValueError(f"Coluna {date_col} não encontrada.")
    s = df[date_col].dropna().dt.to_period("W").apply(lambda p: p.start_time)
    ts = s.value_counts().sort_index()
    if ax is None:
        plt.figure(figsize=(10,4))
        ax = plt.gca()
    ts.plot(ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Semana")
    ax.set_ylabel("Casos")
    return ax

def plot_symptom_bars(df: pd.DataFrame, symptom_cols=None, ax=None, title="Contagem de 'sim' por sintoma"):
    # Detecta colunas *_BIN automaticamente
    if symptom_cols is None:
        symptom_cols = [c for c in df.columns if c.endswith("_BIN")]
    counts = {c.replace("_BIN",""): int(df[c].eq(1).sum()) for c in symptom_cols}
    if ax is None:
        plt.figure(figsize=(9,4))
        ax = plt.gca()
    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    labels, vals = zip(*items) if items else ([],[])
    sns.barplot(x=list(labels), y=list(vals), ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Sintoma")
    ax.set_ylabel("Casos (sim)")
    ax.tick_params(axis="x", rotation=45)
    return ax

def plot_corr_heatmap(df: pd.DataFrame, ax=None, title="Correlação (variáveis numéricas)"):
    num = df.select_dtypes(include=[float, int])
    if num.empty:
        raise ValueError("Não há variáveis numéricas suficientes para correlação.")
    corr = num.corr(numeric_only=True)
    if ax is None:
        plt.figure(figsize=(10,6))
        ax = plt.gca()
    sns.heatmap(corr, cmap="coolwarm", center=0, ax=ax)
    ax.set_title(title)
    return ax

def plot_notification_delay_boxplot(df: pd.DataFrame, delay_col: str = "ATRASO_NOTIF_DIAS", ax=None,
                                    title="Atraso entre Início de Sintomas e Notificação (dias)"):
    if delay_col not in df.columns:
        raise ValueError(f"Coluna {delay_col} não encontrada. Gere com make_dataset.basic_cleaning().")
    s = df[delay_col].dropna()
    if ax is None:
        plt.figure(figsize=(6,4))
        ax = plt.gca()
    sns.boxplot(x=s, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Dias")
    return ax
