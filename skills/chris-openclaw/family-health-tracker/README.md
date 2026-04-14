# Family Health Tracker

A conversational OpenClaw skill that keeps medical records organized for your whole family. Tracks medications, allergies, doctor visits, immunizations, insurance, prescriptions, chronic conditions, and growth milestones. Smart reminders for checkups, refills, and immunization schedules. All data stored locally on your device.

## What It Does

- **Family Profiles** -- each person gets a full health record with allergies, medications, conditions, and emergency notes
- **Visit Logging** -- log doctor, dentist, specialist, and urgent care visits with notes, prescriptions, and follow-ups
- **Immunization Tracking** -- full CDC childhood schedule built in, flags when doses are due
- **Medication Management** -- track dosages, prescribers, pharmacies, and refill dates with reminders
- **Insurance Info** -- carrier, plan type, and PCP on file for each family member (no sensitive IDs stored)
- **Growth Log** -- track height, weight, and percentiles for kids over time
- **Provider Directory** -- doctors, dentists, specialists with contact info and notes
- **Smart Reminders** -- proactive nudges for checkups, dental cleanings, immunizations, and refills
- **Pre-Appointment Prep** -- pull up everything you need before a visit in one shot

## Privacy

All data is stored in a local JSON file on your device. Nothing is sent externally. The skill explicitly avoids storing sensitive identifiers (SSNs, full policy numbers).

## Example Usage

**Log a visit:**
> "Took Emma to Dr. Patel today for her checkup. 42 inches, 38 pounds. Everything looks good."

**Quick lookup:**
> "What are Emma's allergies?"

**Prep for an appointment:**
> "We have a dentist appointment for the kids tomorrow."

**Family overview:**
> "Give me a health summary for the whole family."

**Log a medication:**
> "Emma started Zyrtec today. 5mg daily."

## Installation

Copy the `family-health-tracker` folder into your OpenClaw skills directory and restart your agent.
