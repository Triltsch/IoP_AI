"""Model service of week 3: HTTP interface to the registered models.

    python blockage_service.py --port 5005 --tracking-uri sqlite:///mlflow.db

POST /predict   {"energy": [... at least 360 values, Wh per printing minute, oldest first ...], "model": "zrule" | "knn"}
GET  /health    status, model versions
POST /reload    loads the models with the alias 'production' again (after a new version has been promoted)
"""
import argparse
import time

import mlflow
import mlflow.pyfunc
import pandas as pd
from flask import Flask, jsonify, request

from blockage_core import FEATURES, window_features

MODELS = {'zrule': 'blockage-zrule', 'knn': 'blockage-knn'}
loaded = {}


def load_models():
    client = mlflow.MlflowClient()
    for key, name in MODELS.items():
        version = client.get_model_version_by_alias(name, 'production')
        loaded[key] = {'model': mlflow.pyfunc.load_model(f'models:/{name}@production'), 'name': name, 'version': version.version}


def create_app():
    app = Flask(__name__)

    @app.get('/health')
    def health():
        return jsonify({'status': 'ok', 'models': {k: {'name': v['name'], 'version': v['version']} for k, v in loaded.items()}})

    @app.post('/reload')
    def reload():
        load_models()
        return health()

    @app.post('/predict')
    def predict():
        t0 = time.perf_counter()
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or 'energy' not in payload:
            return jsonify({'error': 'send JSON with the key "energy"'}), 400
        key = payload.get('model', 'zrule')
        if key not in loaded:
            return jsonify({'error': f'unknown model {key!r}; choose one of {sorted(loaded)}'}), 400
        try:
            feats = window_features(payload['energy'])
        except (ValueError, TypeError) as exc:
            return jsonify({'error': str(exc)}), 400
        out = loaded[key]['model'].predict(pd.DataFrame([feats], columns=FEATURES))
        row = out.iloc[0] if isinstance(out, pd.DataFrame) else None
        if row is None:
            score, alarm = float(out[0][1]), int(out[0][1] >= 0.5)
        else:
            score, alarm = float(row['score']), int(row['alarm'])
        return jsonify({'model': loaded[key]['name'], 'version': loaded[key]['version'], 'features': feats,
                        'score': score, 'alarm': alarm, 'ms': round((time.perf_counter() - t0) * 1000, 2)})

    return app


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=5005)
    ap.add_argument('--tracking-uri', default='sqlite:///mlflow.db')
    args = ap.parse_args()
    mlflow.set_tracking_uri(args.tracking_uri)
    load_models()
    create_app().run(host='127.0.0.1', port=args.port, threaded=True)
