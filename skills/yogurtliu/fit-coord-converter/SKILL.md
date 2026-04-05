---
name: fit-coord-converter
description: "Automatically convert GPS coordinates in FIT files from GCJ-02 to WGS-84 format and optionally upload to Strava. ALWAYS USE when the user uploads a .fit file attachment, sends a FIT file, mentions .fit extension, bike computer data, GPS track files, coordinate conversion, or Strava upload."
---

# FIT Coordinate Converter

Convert GPS coordinates in FIT (Flexible and Interoperable Data Transfer) files from the Chinese GCJ-02 coordinate system to the global WGS-84 standard, with optional automatic upload to Strava.

## When to Use

- User uploads a FIT file and asks to convert coordinates
- User mentions GCJ-02 to WGS-84 conversion
- User mentions bike computer data with offset coordinates
- User wants to import Chinese GPS data to Strava, Garmin Connect, or other international platforms
- User asks to upload to Strava after conversion
- User mentions "同时上传Strava" or "upload to Strava"

## Strava Integration (Optional)

If user explicitly requests Strava upload, perform the following after conversion:

### Required Credentials (stored in skill context)
- Client ID: `220965`
- Client Secret: `43fe7384d00c8f0308553e7a38a410d5f0e551e1`
- Access Token: `98f4da29b5cbe0ea8acd1596b41424621cc9a8d0` (with activity:write permission)

### Upload Process
1. Convert the FIT file coordinates as usual
2. Upload using Strava API endpoint: `POST /api/v3/uploads`
3. Include file as multipart form data with parameters:
   - `file`: the converted FIT file
   - `data_type`: "fit"
   - `name`: activity name (use original filename)
   - `description`: "Converted from GCJ-02 to WGS-84 via OpenClaw"

### Alternative: Create Manual Activity
If file upload fails, create a manual activity:
```
POST /api/v3/activities
{
  "name": "<activity_name>",
  "sport_type": "Ride",
  "start_date_local": "<timestamp_from_fit>",
  "elapsed_time": "<duration_from_fit>",
  "distance": "<distance_from_fit>"
}
```

## How It Works

1. **Receive** the FIT file from the user
2. **Parse** all record messages containing GPS coordinates
3. **Convert** each coordinate from GCJ-02 to WGS-84 using the standard conversion algorithm
4. **Preserve** all other data (timestamps, heart rate, speed, etc.) unchanged
5. **Update** the FIT file CRC checksum
6. **Send** the converted file back to the user

## Conversion Algorithm

The GCJ-02 to WGS-84 conversion uses the standard algorithm:

```python
def gcj02_to_wgs84(lng, lat):
    # Transform from GCJ-02 (Mars Coordinates) to WGS-84
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - 0.00669342162296594323 * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((6378245.0 * (1 - 0.00669342162296594323)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (6378245.0 / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat
```

## Auto-Trigger Behavior

When a .fit file attachment is detected in the conversation:
1. **DO NOT ask for confirmation** - immediately process the file
2. Execute the conversion automatically
3. Send the converted file back
4. **ASK** if user wants to upload to Strava: "是否同时上传到 Strava？"
5. If user confirms, proceed with Strava upload
6. Briefly report the result (number of records converted, upload status)

## Steps

1. Detect FIT file attachment from the user message (look for .fit extension in file names)
2. Read the FIT file and parse all record messages
3. For each record with position_lat and position_long:
   - Convert semicircles to degrees
   - Apply GCJ-02 to WGS-84 conversion
   - Convert back to semicircles
   - Replace original values in the binary file
4. Recalculate and update the FIT file CRC
5. Send the converted file using MEDIA: directive

## Output

Send the converted FIT file with a descriptive name including timestamp:
- Format: `<original_name>_WGS84_YYYYMMDD_HHMM.fit`
- Example: `MAGENE_C606_WGS84_20260405_2321.fit`

After sending the file, ask user:
- "是否需要上传到 Strava？"
- If yes, upload using the script `scripts/upload_strava.py`
- Report upload result (activity ID and link)

## Notes

- Only coordinates are modified; all other data (timestamps, sensor readings, etc.) remain unchanged
- The conversion is lossy due to integer semicircle representation
- Files from Chinese bike computers (Magene, XOSS, etc.) typically use GCJ-02
- Converted files work correctly with Strava, Garmin Connect, Komoot, and other international platforms
- Strava upload requires valid access token with `activity:write` permission
- Use the provided credentials in scripts folder for authentication
