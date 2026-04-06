# Exercise Analysis Module

Intelligently parses user exercise information through natural language interaction, voice input, and image uploads, recognizing exercise types and estimating durations, calculating calories consumed by exercises.

## Core Capabilities

- **Semantic Analysis** - Understanding user's natural language descriptions of exercise content
- **Speech Recognition** - Calling ASR for speech recognition, converting to text, with particular attention to accurate recognition of numerical and precise information
- **Image Recognition** - Analyzing exercise images to recognize exercise types and estimate durations
- **Exercise Recognition** - Accurately recognizing exercise types in user descriptions or images
- **Entity Extraction** - Extracting key information such as exercise names, durations, and intensity levels
- **Duration Estimation** - Intelligently estimating exercise duration (minutes) based on descriptions or images
- **Calorie Expenditure Estimation** - Estimating calories consumed based on exercise type, duration, and intensity
- **Standardized Output** - Generating standardized format containing exercise information and calorie expenditure

## Exercise Duration Estimation Principles

### Estimation Methodology

When estimating exercise duration, intelligent evaluation should be based on the following principles:

1. **Based on Common Sense and Public Data**: Reference typical duration data from exercise fitness guidelines and industry standards, combined with exercise types for estimation.

2. **Consider Duration Description Semantics**: Accurately understand duration modifier words in user descriptions (e.g., "half an hour", "one hour", "20 minutes"), and judge actual duration based on context.

3. **Comprehensive Exercise Characteristics**: Consider factors affecting duration such as exercise type, intensity, and individual physical fitness. For example:
   - High-intensity exercises (e.g., HIIT) typically have shorter durations
   - Low-intensity exercises (e.g., walking) can last longer
   - Team sports (e.g., basketball, soccer) typically have fixed durations

4. **Prioritize Explicit Numerical Values**: If users provide specific durations (e.g., "30 minutes", "1 hour"), directly use that value.

5. **Image Recognition Duration Estimation**:
   - **Exercise Equipment Priority**: If the image contains exercise equipment (e.g., treadmills, elliptical trainers), prioritize using the duration number displayed on the equipment
   - **Exercise App Priority**: If the image contains exercise app screenshots, prioritize using the exercise duration displayed on the app
   - **Wearable Device Priority**: If the image contains smart wristbands, watches, or other devices, prioritize using the exercise duration displayed on the device

6. **Estimation Uncertainty**: For ambiguous descriptions, request clarification from users when necessary to ensure result accuracy and reliability.

### Estimation Accuracy Requirements

- Prioritize authoritative data sources
- For composite exercises (e.g., cross-training), decompose main exercise types and estimate separately
- Maintain consistency and interpretability of estimation logic
- All exercise duration estimation must be accurate and reliable

## Calorie Expenditure Estimation Principles

### Estimation Methodology

When estimating exercise calorie expenditure, intelligent evaluation should be based on the following principles:

1. **Reference Exercise Calorie Databases**: Based on standard data from authoritative exercise calorie databases, obtain calorie expenditure data (calories consumed per minute) for different exercise types at different intensity levels.

2. **Consider Exercise Intensity Impact**: Different exercise intensities affect calorie expenditure, for example:
   - Low intensity: slow walking, light yoga
   - Moderate intensity: normal speed running, swimming, cycling
   - High intensity: sprinting, HIIT, jumping rope

3. **Consider Individual Factors**: Individual weight, age, gender, and other factors affect calorie expenditure, using these user information for estimation.

4. **Duration × Intensity**: Calorie expenditure = exercise duration (minutes) × calories consumed per minute for that exercise at corresponding intensity.

5. **Mark Estimation Uncertainty**: Due to variations in individual physical conditions, exercise skills, etc., calorie expenditure estimation may have certain errors, which should be marked in output with estimation basis and confidence level.

6. **Accurate Exercise Data**: Utilize exercise search interface provided by API service to obtain accurate calorie expenditure information for all exercise types.
   - **Exercise Type Matching**: Based on user descriptions or image-recognized exercise types, find the most matching exercise in the exercise list.
   - **Intensity Judgment**: Judge exercise intensity (low, medium, high) based on user descriptions or exercise characteristics.
   - **Calorie Calculation**: Use matching exercise type and intensity to calculate calorie expenditure.

### Estimation Accuracy Requirements

- Prioritize median or average values from authoritative databases
- Consider common variation ranges of exercises
- For composite exercises, reference nutrition information of similar exercises
- Maintain consistency and interpretability of estimation logic
- All calorie expenditure data must be accurate and reliable

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
    - Recognize exercise description intent
    - Extract exercise-related descriptions
    ↓
[3] Entity Recognition
    - Extract exercise names
    - Identify duration descriptions (30 minutes, one hour, 20 minutes, etc.)
    - Identify intensity descriptions (轻松, medium, intense, etc.)
    ↓
[4] Duration Estimation
    - Text/Voice input: Estimate duration based on duration descriptions
    - Image input:
        - Prioritize using duration displayed on exercise equipment
        - Prioritize using duration displayed on exercise app
        - Prioritize using duration displayed on wearable devices
    - Reference common duration equivalent table
    - Consider exercise type impact on duration
    ↓
[5] Calorie Expenditure Estimation
    - Query exercise list through API service to obtain accurate calorie expenditure information
    - Select appropriate calories consumed per minute value based on exercise type and intensity
    - Calculate final calorie expenditure (duration × calories consumed per minute)
    ↓
[6] Generate Output
    - Standardize exercise names
    - Determine final duration (minutes)
    - Output calorie expenditure estimation results
    ↓
Output Results
```

## Intent Recognition Rules

### Exercise Description Intent
- Keywords: ran, swam, cycled, exercised, sports, fitness,锻炼, played ball
- Examples:
  - "I ran for 30 minutes" → Extract running and 30 minutes
  - "Swam for 1 hour just now" → Extract swimming and 1 hour
  - "Exercised at the gym for 1 hour" → Extract fitness and 1 hour

### Exercise Query Intent
- Keywords: expenditure, calories, calories, exercise amount
- Examples:
  - "How many calories consumed by running 30 minutes" → Extract running and 30 minutes
  - "Exercise amount of swimming 1 hour" → Extract swimming and 1 hour

## Entity Extraction Strategy

### Exercise Entities
- Aerobic exercises: walking, running, jogging, cycling, swimming, jumping rope, aerobics, HIIT
- Flexibility training: yoga, pilates, stretching
- Strength training: weightlifting, push-ups, sit-ups, squats, pull-ups, plank, dumbbell training, barbell training
- Ball sports: basketball, soccer, tennis, badminton, table tennis, volleyball, golf
- Outdoor sports: rock climbing, hiking, skiing, ice skating
- Water sports: rowing, kayaking
- Entertainment sports: dancing
- Combat sports: boxing, martial arts
- Fitness equipment: elliptical trainers, treadmills, spin bikes, rowing machines, stair climbers

### Duration Entities
- Time units: minutes, hours, half an hour, one hour
- Quantity descriptions: 30 minutes, 1 hour, 20 minutes

### Intensity Entities
- Intensity descriptions:轻松, medium, intense, low intensity, high intensity

## Output Format

```json
{
  "items": [
    {
      "exercise_name": "Running",
      "duration": 30,
      "calories": 300,
      "intensity": "medium"
    }
  ]
}
```

## Notes

1. **Duration Estimation** - When user descriptions are ambiguous, use common duration reference values and explain estimation basis in responses
2. **Calorie Expenditure Estimation** - Calculate based on authoritative databases and standard data to ensure data accuracy and reliability
3. **Multiple Exercise Processing** - Support analyzing multiple exercises at once, output calorie expenditure separately and summarize
4. **Accuracy** - Try to accurately extract exercise names, avoid ambiguous or incorrect recognition
5. **Transparency** - Clearly explain data sources and calculation methods

## Tips for Improving Entry Accuracy

To help the agent more accurately recognize exercise types and assess durations, users can adopt the following methods:

### Text Input Tips
- **Detailed Description**: Provide specific exercise names, durations, and intensity levels
- **Quantitative Information**: Provide specific durations when possible, such as "30 minutes running", "1 hour swimming"
- **Avoid Ambiguous Expressions**: Use clear duration descriptions, such as "30 minutes" instead of "a while"

### Voice Input Tips
- **Clear Pronunciation**: Moderate speech rate to ensure numbers and duration units are clearly distinguishable
- **Complete Description**: Include exercise names, durations, and intensity levels
- **Quiet Environment**: Record in quiet environments to reduce background noise interference

### Image Input Tips
- **Include Exercise Equipment**: Include display information from exercise equipment (e.g., treadmills, elliptical trainers) in images
- **Photograph Exercise App Screenshots**: Photograph exercise app data interfaces, ensuring duration and calorie expenditure are clearly visible
- **Photograph Wearable Devices**: Photograph exercise data displayed on smart wristbands, watches, or other devices
- **Adequate Lighting**: Ensure images have adequate lighting and display information is clearly visible
- **Multi-angle Photography**: For complex exercise scenarios, photograph from multiple angles to provide more comprehensive information
