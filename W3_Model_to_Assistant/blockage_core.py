"""Shared code of week 3: data pipeline, features from a window, and the model that is registered in MLflow.

The same functions are used for training (notebooks), for the model service and for the monitor,
so that training and operation compute the features in exactly the same way.
"""
import numpy as np
import pandas as pd
import mlflow.pyfunc

FEATURES = ['E30', 'E120', 'slope']
HORIZON = 360                      # minutes: a sample is class 1 if a blockage follows within 6 h
WINDOW = 360                       # minutes of printing needed for the features (E120 now and 240 minutes ago)


def load_printer(folder, k, ts_format=None):
    """Minute data of printer k: energy per minute in Wh (column E, printing minutes only) and the list of blockages."""
    d = pd.read_csv(folder / f'Printer_{k}.csv', sep=';', decimal=',', low_memory=False).dropna(how='all')
    d['Timestamp'] = pd.to_datetime(d['Timestamp'], format=ts_format)
    d = d.set_index('Timestamp')
    d['E'] = d['Total_Power'].diff() * 1000                   # Wh per minute (the file holds a cumulative counter in kWh)
    e = pd.read_csv(folder / f'Printer_{k}_error.csv', sep=';').dropna(how='all')
    e['Timestamp'] = pd.to_datetime(e['Timestamp'], format=ts_format)
    blockages = pd.to_datetime(np.sort(e.loc[e['Error'] == 'Extruder blocked', 'Timestamp'].values))
    return d, blockages


def make_blockage_data(folder, k, ts_format=None, horizon=HORIZON):
    """The pipeline of exercise 2: one row per 10th printing minute with the features E30, E120, slope and the label y."""
    d, blockages = load_printer(folder, k, ts_format)
    p = d[d['State'] == 'printing'].copy()
    idx = p.index.values
    nxt = np.searchsorted(blockages.values, idx)
    mtb = np.where(nxt < len(blockages), (blockages.values[np.minimum(nxt, len(blockages) - 1)] - idx) / np.timedelta64(1, 'm'), np.inf)
    p['y'] = ((mtb > 0) & (mtb <= horizon)).astype(int)         # only used to EVALUATE
    p['E30'] = p['E'].rolling(30).mean()
    p['E120'] = p['E'].rolling(120).mean()
    p['slope'] = p['E120'] - p['E120'].shift(240)
    return p.dropna(subset=FEATURES).iloc[::10], blockages


def window_features(energy):
    """Features of the last sample from a window of at least WINDOW printing minutes (Wh/min, oldest value first).

    Identical to the rolling-window definition of make_blockage_data: E30 and E120 are means of the last 30 and 120 minutes,
    slope = E120 now minus E120 240 minutes ago.
    """
    e = np.asarray(energy, dtype=float)
    if e.ndim != 1 or len(e) < WINDOW:
        raise ValueError(f'need a list of at least {WINDOW} values (printing minutes, Wh/min), got {len(e) if e.ndim == 1 else e.shape}')
    if not np.isfinite(e).all():
        raise ValueError('the window contains NaN or infinite values')
    if (e < 0).any() or (e > 10).any():
        raise ValueError('values outside 0 to 10 Wh/min: wrong unit?')
    e120 = e[-120:].mean()
    return {'E30': float(e[-30:].mean()), 'E120': float(e120), 'slope': float(e120 - e[-360:-240].mean())}


class ZRuleModel(mlflow.pyfunc.PythonModel):
    """The z-value rule of exercise 2b as a registered model: z = (E120 - mean) / sd, alarm if z > limit."""

    def __init__(self, mean, sd, z_limit):
        self.mean, self.sd, self.z_limit = float(mean), float(sd), float(z_limit)

    def predict(self, context, model_input, params=None):
        z = (model_input['E120'].astype(float) - self.mean) / self.sd
        return pd.DataFrame({'score': z.values, 'alarm': (z > self.z_limit).astype(int).values})


class KnnModel(mlflow.pyfunc.PythonModel):
    """KNN (with scaling) as a registered model: score = share of class-1 neighbours, alarm if score >= threshold."""

    def __init__(self, pipeline, threshold=0.5):
        self.pipeline, self.threshold = pipeline, float(threshold)

    def predict(self, context, model_input, params=None):
        s = self.pipeline.predict_proba(model_input[FEATURES].astype(float))[:, 1]
        return pd.DataFrame({'score': s, 'alarm': (s >= self.threshold).astype(int)})


# ---------------------------------------------------------------- evaluation and reference models (same as notebook 01)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score


def fit_references(data_old, k_neighbors=25, train_share=0.7, quantile=0.95):
    """Frozen reference models of weeks 1 to 3: fitted on the first 70 % of printer 1 from 2024/25."""
    old, _ = make_blockage_data(data_old, 1, ts_format='%d.%m.%Y %H:%M')
    ref = old.iloc[:int(len(old) * train_share)]
    mu, sd = ref['E120'].mean(), ref['E120'].std()
    z_limit = float(np.quantile((ref['E120'] - mu) / sd, quantile))
    knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k_neighbors)).fit(ref[FEATURES], ref['y'])
    return {'ref': ref, 'mu': float(mu), 'sd': float(sd), 'z_limit': z_limit, 'knn': knn}


def evaluate_alarms(alarm, test, blockages):
    """alarm: boolean Series on the index of `test`. Returns (announced blockages, blockages, false alarm episodes per week)."""
    t0, t1 = test.index[0], test.index[-1]
    blk = [t for t in blockages if t0 <= t <= t1]
    announced = sum(bool(alarm[(alarm.index >= t - pd.Timedelta(hours=6)) & (alarm.index <= t)].any()) for t in blk)
    times = alarm[alarm].index
    weeks = (t1 - t0).days / 7
    if len(times) == 0:
        return announced, len(blk), 0.0
    new_episode = np.concatenate([[0], np.diff(times.values) > np.timedelta64(6, 'h')])
    ep = pd.DataFrame({'ep': np.cumsum(new_episode), 'y': test.loc[times, 'y'].values}).groupby('ep')['y'].max()
    return announced, len(blk), float((ep == 0).sum() / weeks)


def evaluate_on_farm(printers, model):
    """Score a registered-style model (predict -> DataFrame with score and alarm) on all printers of a dict {k: (data, blockages)}."""
    aucs, ann, blk, fa = [], 0, 0, []
    for k, (d, b) in printers.items():
        out = model.predict(None, d[FEATURES])
        alarm = pd.Series(out['alarm'].values == 1, index=d.index)
        a, n, f = evaluate_alarms(alarm, d, b)
        aucs.append(roc_auc_score(d['y'], out['score'])); ann += a; blk += n; fa.append(f)
    return {'auc': float(np.mean(aucs)), 'announced_share': ann / blk, 'false_episodes_per_week': float(np.mean(fa))}
