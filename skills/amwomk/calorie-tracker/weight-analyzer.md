# Weight Analysis Module

Intelligently parses user weight information through natural language interaction, voice input, and image uploads, recording weight data and analyzing weight change trends to provide users with weight management references.

## Core Capabilities

- **Semantic Analysis** - Understanding user's natural language descriptions of weight content
- **Speech Recognition** - Calling ASR for speech recognition, converting to text, with particular attention to accurate recognition of numerical and precise information
- **Image Recognition** - Analyzing weight scale images to recognize weight values
- **Weight Recording** - Accurately recording weight data from user descriptions or images
- **Entity Extraction** - Extracting key information such as weight values, measurement times, and weight scale types
- **Trend Analysis** - Analyzing user weight change trends and providing health recommendations
- **Standardized Output** - Generating standardized format containing weight information and change trends

## Weight Data Estimation Principles

### Estimation Methodology

When processing weight data, intelligent evaluation should be based on the following principles:

1. **Based on Common Sense and Public Data**: Reference healthy weight ranges, BMI calculation standards, and other authoritative data, combined with user information for analysis.

2. **Consider Weight Description Semantics**: Accurately understand weight values and units in user descriptions (e.g., "60 kg", "130 jin", "180 lbs"), and judge actual weight based on context.

3. **Comprehensive User Characteristics**: Consider factors affecting weight such as user age, gender, height, and body fat percentage. For example:
   - Healthy weight ranges differ for different age groups
   - Body fat percentage standards differ for different genders
   - Height impact on weight (through BMI calculation)

4. **Prioritize Explicit Numerical Values**: If users provide specific weight values and units, directly use those values.

5. **Image Recognition Weight Estimation**:
   - **Weight Scale Priority**: If the image contains a weight scale, prioritize using the number displayed on the scale as weight
   - **Health App Priority**: If the image contains health app screenshots, prioritize using weight data displayed on the app
   - **Wearable Device Priority**: If the image contains smart wristbands, watches, or other devices, prioritize using weight data displayed on the device

6. **Estimation Uncertainty**: For ambiguous descriptions, request clarification from users when necessary to ensure result accuracy and reliability.

### Estimation Accuracy Requirements

- Prioritize authoritative data sources
- Maintain consistency and interpretability of data recording
- All weight data must be accurate and reliable
- Pay attention to accuracy of unit conversions (e.g., kg to jin, lbs)

## Complete Processing Flow

```
User Input
    ↓
[1] Input Type Judgment
    - Text input: Directly enter semantic analysis
    - Voice input: Call ASR for speech recognition, with particular attention to accurate recognition of numerical and precise information
    - Image input: Call OCR to recognize text in images, utilize large models to recognize image content
    ↓
[2] Semantic Analysis (Text/Voice Transcription)
    - Recognize weight description intent
    - Extract weight-related descriptions
    ↓
[3] Entity Recognition
    - Extract weight values
    - Identify units (kg, jin, lbs, etc.)
    - Identify measurement times (today, yesterday, last week, etc.)
    ↓
[4] Weight Data Processing
    - Text/Voice input: Extract weight values and units based on descriptions
    - Image input:
        - Prioritize using values displayed on weight scales
        - Prioritize using values displayed on health apps
        - Prioritize using values displayed on wearable devices
    - Unit conversion (if necessary)
    - Calculate BMI (if height information is provided)
    ↓
[5] Trend Analysis
    - Compare with historical weight data
    - Analyze weight change trends
    - Calculate change rates
    ↓
[6] Generate Output
    - Standardize weight values
    - Determine final units
    - Output weight analysis results and trends
    ↓
Output Results
```

## Intent Recognition Rules

### Weight Recording Intent
- Keywords: weight, weighed, measured, weight scale, weight is, weight is
- Examples:
  - "My weight today is 60 kg"
  - "Just weighed, weight is 130 jin"
  - "My weight is 180 lbs"

### Weight Query Intent
- Keywords: query, history, trends, changes, BMI
- Examples:
  - "Query my recent weight records"
  - "My weight change trends"
  - "Calculate my BMI"

## Entity Extraction Strategy

### Weight Entities
- Weight values: numbers such as 60, 130, 180
- Weight units: kg, jin, lbs, kilograms
- Measurement times: today, yesterday, last week, last month

### Related Entities
- Height: used for BMI calculation
- Age: used for evaluating healthy weight ranges
- Gender: used for evaluating healthy weight ranges

## Output Format

```json
{
  "items": [
    {
      "weight": 60,
      "unit": "kg",
      "date": "2023-10-01",
      "bmi": 22.5,
      "status": "Normal"
    }
  ]
}
```


## Notes

1. **Weight Data Recording** - When users provide weight data, ensure accurate recording of values and units
2. **Unit Conversion** - Pay attention to conversions between different units to ensure data consistency
3. **BMI Calculation** - If users provide height information, calculate BMI and provide healthy status evaluation
4. **Trend Analysis** - Provide weight change trend analysis based on historical data
5. **Privacy Protection** - Ensure user weight data privacy and security

## Tips for Improving Entry Accuracy

To help the agent more accurately record and analyze weight data, users can adopt the following methods:

### Text Input Tips
- **Detailed Description**: Provide specific weight values and units, such as "60 kg", "130 jin"
- **Include Time**: Provide measurement times when possible, such as "weight today is 60 kg"
- **Provide Height**: If BMI calculation is needed, provide height information, such as "height 170 cm, weight 60 kg"

### Voice Input Tips
- **Clear Pronunciation**: Moderate speech rate to ensure numbers and units are clearly distinguishable
- **Complete Description**: Include weight values, units, and measurement times
- **Quiet Environment**: Record in quiet environments to reduce background noise interference

### Image Input Tips
- **Photograph Weight Scales**: Ensure weight scale numbers are clearly visible
- **Photograph Health Apps**: Photograph health app weight data interfaces, ensuring values are clearly visible
- **Photograph Wearable Devices**: Photograph weight data displayed on smart wristbands, watches, or other devices
- **Adequate Lighting**: Ensure images have adequate lighting and display information is clearly visible
- **Photograph Complete Interfaces**: Include weight values, units, and measurement times
