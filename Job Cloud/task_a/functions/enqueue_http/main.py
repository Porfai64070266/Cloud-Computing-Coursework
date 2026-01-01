# HTTP function to enqueue multiple GCS URIs to a Pub/Sub topic for parallel processing
# Entry point: enqueue(request)

import json
import os
from typing import List
from google.cloud import pubsub_v1

TOPIC = os.getenv("TOPIC", "")

publisher = pubsub_v1.PublisherClient()

def enqueue(request):
    try:
        if not TOPIC:
            return (json.dumps({"error": "TOPIC not configured"}), 500, {"Content-Type": "application/json"})
        data = request.get_json(silent=True) or {}
        uris: List[str] = data.get("gcs_uris") or []
        modes: List[str] = data.get("modes") or None
        if not uris:
            return (json.dumps({"error": "Provide gcs_uris: [gs://bucket/file1.txt, ...]"}), 400, {"Content-Type": "application/json"})
        topic_path = TOPIC  # can be full path projects/..../topics/...
        futures = []
        for u in uris:
            message = {"gcs_uri": u}
            if modes:
                message["modes"] = modes
            futures.append(publisher.publish(topic_path, data=json.dumps(message).encode("utf-8")))
        # wait publish
        for f in futures:
            f.result(timeout=30)
        return (json.dumps({"enqueued": len(uris)}), 200, {"Content-Type": "application/json"})
    except Exception as e:
        return (json.dumps({"error": str(e)}), 500, {"Content-Type": "application/json"})
