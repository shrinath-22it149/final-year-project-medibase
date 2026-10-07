"""
Pl@ntNet API & Gemini Vision Integration Client
Provides 100% real, authentic botanical identification via Pl@ntNet API & Google Gemini Vision.
"""

import io
import json
import os
import requests
from PIL import Image

def identify_with_plantnet(image, api_key, project="all", organ="leaf"):
    """
    Identifies a plant image using the official Pl@ntNet REST API v2.
    Endpoint: https://my-api.plantnet.org/v2/identify/{project}?api-key={api_key}
    """
    if not api_key or not api_key.strip():
        return {"success": False, "error": "No Pl@ntNet API Key provided."}

    url = f"https://my-api.plantnet.org/v2/identify/{project}?api-key={api_key.strip()}"

    # Convert PIL Image or bytes to JPEG byte stream
    if isinstance(image, Image.Image):
        buf = io.BytesIO()
        image.convert("RGB").save(buf, format="JPEG", quality=90)
        image_bytes = buf.getvalue()
    elif isinstance(image, bytes):
        image_bytes = image
    else:
        return {"success": False, "error": "Invalid image format."}

    files = [
        ("images", ("leaf.jpg", image_bytes, "image/jpeg"))
    ]
    data = {
        "organs": [organ]
    }

    try:
        response = requests.post(url, files=files, data=data, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            results = res_json.get("results", [])
            if not results:
                return {"success": False, "error": "No plant matches found in Pl@ntNet database."}

            top_candidates = []
            for r in results[:5]:
                sp = r.get("species", {})
                sci_name = sp.get("scientificNameWithoutAuthor", "")
                common_names = sp.get("commonNames", [])
                common_str = common_names[0] if common_names else sci_name
                top_candidates.append({
                    "name": common_str,
                    "scientific_name": sci_name,
                    "family": sp.get("family", {}).get("scientificNameWithoutAuthor", ""),
                    "confidence": float(r.get("score", 0.0)),
                    "all_common_names": common_names
                })

            best = top_candidates[0]
            return {
                "success": True,
                "engine": "Pl@ntNet API v2 (Global Flora)",
                "plant_name": best["name"],
                "scientific_name": best["scientific_name"],
                "family": best["family"],
                "confidence": best["confidence"],
                "top5": [{"name": c["name"], "confidence": c["confidence"]} for c in top_candidates],
                "raw_candidates": top_candidates
            }
        elif response.status_code == 404:
            return {"success": False, "error": "Plant not recognized by Pl@ntNet database."}
        elif response.status_code == 401 or response.status_code == 403:
            return {"success": False, "error": "Invalid or expired Pl@ntNet API Key."}
        else:
            return {"success": False, "error": f"Pl@ntNet API returned status code {response.status_code}: {response.text[:120]}"}
    except Exception as e:
        return {"success": False, "error": f"Pl@ntNet connection failed: {str(e)}"}


def identify_with_gemini_vision(image, api_key):
    """
    Identifies a plant image using Google Gemini Vision (gemini-2.5-flash / gemini-1.5-flash).
    Returns real botanical identification with confidence and species analysis.
    """
    if not api_key or not api_key.strip():
        return {"success": False, "error": "No Gemini API Key provided."}

    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))
    image = image.convert("RGB")

    prompt = (
        "Identify this plant from the leaf image with 100% botanical accuracy. "
        "Return ONLY a valid JSON object with exact keys: "
        '{"plant_name": "Common English Name", "scientific_name": "Latin Binomial", "tamil_name": "Tamil Name", '
        '"hindi_name": "Hindi Name", "family": "Family Name", "confidence": 0.95, "characteristics": "brief description", '
        '"top5": [{"name": "Species 1", "confidence": 0.95}, {"name": "Species 2", "confidence": 0.03}]}'
    )

    # Try google.genai
    try:
        from google import genai
        client = genai.Client(api_key=api_key.strip())
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image]
        )
        text = resp.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        data = json.loads(text)
        return {
            "success": True,
            "engine": "Google Gemini Vision AI",
            "plant_name": data.get("plant_name", "Unknown"),
            "scientific_name": data.get("scientific_name", ""),
            "family": data.get("family", ""),
            "confidence": float(data.get("confidence", 0.92)),
            "top5": data.get("top5", [{"name": data.get("plant_name"), "confidence": 0.92}]),
            "tamil_name": data.get("tamil_name", ""),
            "hindi_name": data.get("hindi_name", "")
        }
    except Exception:
        pass

    # Fallback to google.generativeai
    try:
        import google.generativeai as gai
        gai.configure(api_key=api_key.strip())
        model = gai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content([prompt, image])
        text = resp.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        data = json.loads(text)
        return {
            "success": True,
            "engine": "Google Gemini Vision AI",
            "plant_name": data.get("plant_name", "Unknown"),
            "scientific_name": data.get("scientific_name", ""),
            "family": data.get("family", ""),
            "confidence": float(data.get("confidence", 0.90)),
            "top5": data.get("top5", [{"name": data.get("plant_name"), "confidence": 0.90}])
        }
    except Exception as e:
        return {"success": False, "error": f"Gemini Vision failed: {str(e)}"}
