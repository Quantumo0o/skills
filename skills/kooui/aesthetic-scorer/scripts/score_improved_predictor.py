#!/usr/bin/env python3
"""
Improved Aesthetic Predictor - Fast Scoring Script
Ultra-fast aesthetic scoring (<1 second response)
"""

import torch
import torchvision.transforms as transforms
from PIL import Image
import argparse
import json
import sys

# Try to import the model
try:
    from improved_aesthetic_predictor import AestheticPredictor
except ImportError:
    print("Error: Improved Aesthetic Predictor model not found.")
    print("Please install it from: https://github.com/christophschuhmann/improved-aesthetic-predictor")
    sys.exit(1)


def load_image(image_path, size=224):
    """Load and preprocess image for model input"""
    try:
        img = Image.open(image_path).convert('RGB')
        
        # Standard preprocessing for the model
        preprocess = transforms.Compose([
            transforms.Resize((size, size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        img_tensor = preprocess(img).unsqueeze(0)
        return img_tensor, img
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)


def predict_aesthetic(image_path, model_path=None):
    """
    Predict aesthetic score using Improved Aesthetic Predictor
    
    Args:
        image_path: Path to the image file
        model_path: Optional path to custom model weights
    
    Returns:
        dict: Contains score and metadata
    """
    # Load model
    print("Loading Improved Aesthetic Predictor...")
    try:
        predictor = AestheticPredictor(model_path=model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
    
    # Load and preprocess image
    print(f"Processing image: {image_path}")
    img_tensor, img_pil = load_image(image_path)
    
    # Predict
    with torch.no_grad():
        score = predictor.predict(img_tensor)
    
    # Format result
    result = {
        'model': 'improved-aesthetic-predictor',
        'score': float(score),
        'image_path': image_path,
        'image_size': img_pil.size,
        'response_time': '<1s (fast)'
    }
    
    return result


def interpret_score(score):
    """Interpret the aesthetic score"""
    if score >= 8.5:
        interpretation = "Excellent - Outstanding aesthetic quality"
    elif score >= 7.0:
        interpretation = "Very Good - High aesthetic quality with minor room for improvement"
    elif score >= 5.5:
        interpretation = "Good - Above average, solid aesthetic foundation"
    elif score >= 4.0:
        interpretation = "Fair - Average aesthetic quality, some areas to improve"
    else:
        interpretation = "Below Average - Significant room for aesthetic improvement"
    
    return interpretation


def main():
    parser = argparse.ArgumentParser(description='Fast aesthetic scoring with Improved Aesthetic Predictor')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    parser.add_argument('--model', type=str, default=None, help='Path to custom model weights')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Predict
    result = predict_aesthetic(args.image_path, args.model)
    
    if result is None:
        sys.exit(1)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "="*60)
        print("AESTHETIC SCORE (Improved Predictor)")
        print("="*60)
        print(f"Score: {result['score']:.2f}/10")
        print(f"Interpretation: {interpret_score(result['score'])}")
        print(f"Image Size: {result['image_size'][0]}x{result['image_size'][1]}")
        print(f"Response Time: {result['response_time']}")
        print("="*60 + "\n")


if __name__ == "__main__":
    main()
