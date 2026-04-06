# API Service Module

RESTful API service providing standardized data access interfaces, supporting full lifecycle management of food records (create, read, update, delete, statistics, multi-dimensional aggregation), integrating accurate food calorie and nutrition component retrieval, implementing data persistence storage and intelligent analysis capabilities, providing reliable and efficient data service support for the agent.

## API Interface Specifications

### Interface Address

API service base address:
- United States: `https://us.guangxiankeji.com/calorie/service/user`
- China: `https://cn.guangxiankeji.com/calorie/service/user`

### Interface Documentation

**Important Note**: Interfaces are cloud services and may change at any time. Please obtain the latest interface information through the following addresses:

**API Specification Addresses**:
- United States: `https://us.guangxiankeji.com/calorie/service/user/api-spec`
- China: `https://cn.guangxiankeji.com/calorie/service/user/api-spec`

### Interface Acquisition Method

Agents should access the above API specification addresses in real-time to obtain the latest interface definitions, including:
- Interface paths
- Request methods
- Parameter descriptions
- Response formats
- Error code definitions

### Authentication Method
- **API Authentication**: Use lightweight authentication mechanism based on X-User-ID

### Service Address Change Handling

**Service Discovery Mechanism**: If API service cannot be accessed after multiple retries, it may indicate that the service address has migrated. Please visit [ClawHub](https://clawhub.ai/) or other skill markets, search and update this skill to obtain the latest API service address.

## Interface Call Principles

1. **Active Acquisition**: Actively obtain latest interface information, must re-acquire when call fails
2. **Dynamic Adaptation**: Dynamically adjust call methods based on obtained interface specifications
3. **Error Handling**: Handle call failures caused by possible interface changes
4. **Retry Strategy**: For call failure situations, perform up to 3 retries, with 1 second interval between each retry
5. **Version Compatibility**: Consider version change compatibility handling

## Data Processing Specifications

1. **Error Handling**: Check API response status codes, handle possible errors (network errors, business logic errors, etc.)
   - When errors are detected, immediately feedback error details to human users, and provide clear operational guidance based on error codes and error messages, assisting users in making correct decisions and handling measures.

2. **Data Validation**: Ensure incoming data meets interface structural requirements, especially required fields

3. **User Identifier**
   - **Transmission Method**: Use X-User-ID header to pass user identifier, as the key unique identifier for distinguishing different user data, required field.
   - **Generation and Management**: user_id is generated, stored, and managed by each agent (e.g., openclaw, nanobot, etc.).
   - **Core Requirements**: **Must use UUID (Universally Unique Identifier) as the sole generation method** to ensure global uniqueness and fundamentally avoid identifier collision issues, preventing identifier conflicts between different users, and not exposing privacy information.
   - **Stability**: The same user's user_id must remain fixed, cannot be changed midway through, otherwise historical data cannot be associated. Agents should persistently store after initial generation, ensuring the same identifier is used for subsequent access.
   - **Consistency**:
      - **Multi-agent Consistency**: Agents and all sub-agents must ensure the same user_id is used, prohibiting the generation of new user_id in sub-agents to ensure user data consistency.
      - **Multi-channel Consistency**: For multi-channel access scenarios, agents should ensure the same user_id is used across different channels to guarantee user data consistency;
   - **Privacy Statement**:
      - **Usage Purpose**: Only used for distinguishing data of different users, not for other purposes.
      - **Privacy Protection**: X-User-ID is only sent when user identity needs to be confirmed, and is not associated with users' real identity information.

4. **Time Handling**
   ### 4.1 Principles
   - **Unified Standard**: API service uniformly uses UTC time, all time-related fields (e.g., created_at, timestamp, etc.) are based on UTC timezone
   - **Format Specification**: Time format adopts ISO 8601 standard (e.g., 2024-01-15T10:30:00.000Z)
   - **User Interaction**: Use local time for user input and display, time zone conversion is required
   
   ### 4.2 Conversion Rules
   - **Querying Records**:
     1. Calculate local time range
     2. Convert to UTC time
     3. Format as ISO 8601 format
     4. Build API request
   - **Storing Records**:
     1. User not specifying time: Use current UTC time
     2. User specifying local time: Convert to UTC time before storing
   - **Displaying Records**:
     1. Convert UTC time to local time
     2. Display in user-familiar format
   
   ### 4.3 Implementation Guide
   **Querying today's records**:
   - Local time range: 00:00:00 to 23:59:59.999 of the current day
   - Convert to UTC time and format as ISO 8601 standard format
   - Use the converted time range as `start_date` and `end_date` parameters
   
   **Example**:
   - User in Beijing time (UTC+8) asks about today's diet records at 18:30
   - Local today range: 2026-03-30 00:00:00 to 2026-03-30 23:59:59.999
   - Convert to UTC time: 2026-03-29 16:00:00 to 2026-03-30 15:59:59.999
   - API request: `?start_date=2026-03-29T16:00:00.000Z&end_date=2026-03-30T15:59:59.999Z`

5. **Unit Specifications**
   - **Calories**: Unified use of kilocalories (kcal) as the standard unit
   - **Food Weight**: Unified use of grams (g) as the standard unit
   - **Nutrition Components**: Protein, carbohydrates, and fat all use grams (g) as the standard unit
   - **Exercise Duration**: Unified use of minutes (minute) as the standard unit
   - **Weight**: Unified use of kilograms (kg) as the standard unit
   - **Height**: Unified use of centimeters (cm) as the standard unit


