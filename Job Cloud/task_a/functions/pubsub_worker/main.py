# Pub/Sub worker: process a single file message and write results to output bucket
# Entry point: worker(event, context)

import base64
import json
import os
from typing import List
try:
    from task_a.text_analysis.analysis import run_selected_analyses, STOP_WORDS, VALID_MODES
except ModuleNotFoundError:
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
from google.cloud import storage

OUTPUT_BUCKET = os.getenv("OUTPUT_BUCKET", "")
DEFAULT_MODES = os.getenv("DEFAULT_MODES", "word_freq,sentence_starts,sentence_length").split(",")
DEFAULT_MODES = [m for m in DEFAULT_MODES if m in VALID_MODES]

storage_client = storage.Client()

def _read_gcs_text(gs_uri: str) -> str:
    if not gs_uri.startswith("gs://"):
        raise ValueError("gcs_uri must start with gs://")
    _, path = gs_uri.split("gs://", 1)
    bucket_name, blob_path = path.split("/", 1)
    blob = storage_client.bucket(bucket_name).blob(blob_path)
    return blob.download_as_text(encoding="utf-8")


def worker(event, context):
    if not OUTPUT_BUCKET:
        print("OUTPUT_BUCKET not configured")
        return
    payload = base64.b64decode(event['data']).decode('utf-8') if event.get('data') else "{}"
    # Be tolerant to non-JSON payloads (e.g., plain 'gs://...' string)
    try:
        msg = json.loads(payload)
    except json.JSONDecodeError:
        # If payload looks like a GCS URI, treat it as such; otherwise, skip gracefully
        if payload.strip().startswith("gs://"):
            msg = {"gcs_uri": payload.strip()}
        else:
            print(f"Skipping non-JSON, non-GCS payload: {payload[:120]}")
            return
    gcs_uri = msg.get("gcs_uri")
    modes: List[str] = [m for m in (msg.get("modes") or DEFAULT_MODES) if m in VALID_MODES]
    if not gcs_uri:
        print("No gcs_uri in message")
        return

    text = _read_gcs_text(gcs_uri)
    result = run_selected_analyses(text, STOP_WORDS, modes)

    # create deterministic output key
    # e.g., gs://bucket/path/file.txt -> results/path/file.txt.json
    bucket_name, blob_path = gcs_uri.replace("gs://", "", 1).split("/", 1)
    out_name = f"results/{blob_path}.json"
    out_blob = storage_client.bucket(OUTPUT_BUCKET).blob(out_name)
    out_blob.content_type = "application/json"
    out_blob.upload_from_string(json.dumps({
        "gcs_uri": gcs_uri,
        "modes": modes,
        "result": result
    }, ensure_ascii=False), content_type="application/json")

    print(f"Processed {gcs_uri} -> gs://{OUTPUT_BUCKET}/{out_name}")
