# HTTP Cloud Function to analyze text by selected modes.
# Entry point: analyze_http(request)

import base64
import json
import os
from typing import Any, Dict, List

try:
    # When deployed with PYTHONPATH hack we can import original module
    from task_a.text_analysis.analysis import (
        run_selected_analyses, STOP_WORDS, VALID_MODES
    )
except ModuleNotFoundError:
    # Fallback: use the vendored copy placed in this function folder for deployment simplicity
    from text_analysis.analysis import (
        analyze_word_frequency,
        analyze_sentence_start_words,
        analyze_sentence_length_distribution,
        STOP_WORDS, VALID_MODES
    )

    def run_selected_analyses(text: str, stop_words: set[str], modes: list[str]):
        results = {}
        for m in modes:
            if m == "word_freq":
                results[m] = analyze_word_frequency(text, stop_words)
            elif m == "sentence_starts":
                results[m] = analyze_sentence_start_words(text)
            elif m == "sentence_length":
                results[m] = analyze_sentence_length_distribution(text)
        return results

# Optional: read text from GCS
from google.cloud import storage

_STORAGE_CLIENT = None

def _get_storage_client():
    global _STORAGE_CLIENT
    if _STORAGE_CLIENT is None:
        _STORAGE_CLIENT = storage.Client()
    return _STORAGE_CLIENT


def _read_gcs_text(gs_uri: str) -> str:
    # gs://bucket/path/to/file.txt
    if not gs_uri.startswith("gs://"):
        raise ValueError("gcs_uri must start with gs://")
    _, path = gs_uri.split("gs://", 1)
    bucket_name, blob_path = path.split("/", 1)
    client = _get_storage_client()
    blob = client.bucket(bucket_name).blob(blob_path)
    return blob.download_as_text(encoding="utf-8")


def analyze_http(request):
    """HTTP trigger
    Request JSON body:
    {
      "modes": ["word_freq", "sentence_starts", "sentence_length"],
      "text": "optional inline text",
      "gcs_uri": "optional gs://bucket/file.txt"
    }
    One of text or gcs_uri is required. modes defaults to all.
    """
    try:
        # Primary JSON parse
        data = request.get_json(silent=True) or {}
        # Fallback: some environments occasionally fail to populate get_json; attempt manual parse
        if (not data) and getattr(request, "data", None):
            try:
                raw = request.data.decode("utf-8")
                if raw.strip():
                    data = json.loads(raw)
                    print(f"Fallback JSON parsed, length={len(raw)}")
            except Exception as parse_err:
                print(f"Fallback JSON parse failed: {parse_err}")
        modes: List[str] = data.get("modes") or list(VALID_MODES)
        modes = [m for m in modes if m in VALID_MODES]
        if not modes:
            return (json.dumps({"error": "No valid modes"}), 400, {"Content-Type": "application/json"})

        text = data.get("text")
        gcs_uri = data.get("gcs_uri")
        if not text and not gcs_uri:
            # Log raw body for debugging
            raw_preview = request.data[:120] if getattr(request, "data", None) else b""
            print(f"Missing text/gcs_uri. Raw body preview: {raw_preview}")
            return (json.dumps({"error": "Provide 'text' or 'gcs_uri'"}), 400, {"Content-Type": "application/json"})
        if not text:
            text = _read_gcs_text(gcs_uri)
        result = run_selected_analyses(text, STOP_WORDS, modes)
        return (json.dumps({"modes": modes, "result": result}), 200, {"Content-Type": "application/json"})
    except Exception as e:
        return (json.dumps({"error": str(e)}), 500, {"Content-Type": "application/json"})
