# Cloud Storage finalize trigger - analyze uploaded txt and write JSON result to an output bucket
# Entry point: analyze_gcs(event, context)

import json
import os
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

def analyze_gcs(event, context):
    bucket = event["bucket"]
    name = event["name"]
    content_type = event.get("contentType", "")
    if not name.lower().endswith(".txt"):
        # Skip non-txt files
        return
    if not OUTPUT_BUCKET:
        print("OUTPUT_BUCKET not configured")
        return
    # read text
    blob = storage_client.bucket(bucket).blob(name)
    text = blob.download_as_text(encoding="utf-8")

    # choose modes: allow object metadata 'modes' to override
    modes_meta = blob.metadata.get("modes") if blob.metadata else None
    modes = DEFAULT_MODES if not modes_meta else [m for m in modes_meta.split(",") if m in VALID_MODES]

    result = run_selected_analyses(text, STOP_WORDS, modes)

    # write to output bucket as JSON with same base name
    out_name = f"results/{name}.json"
    out_blob = storage_client.bucket(OUTPUT_BUCKET).blob(out_name)
    out_blob.content_type = "application/json"
    out_blob.upload_from_string(json.dumps({
        "source_bucket": bucket,
        "source_name": name,
        "modes": modes,
        "result": result
    }, ensure_ascii=False), content_type="application/json")

    print(f"Wrote result to gs://{OUTPUT_BUCKET}/{out_name}")
