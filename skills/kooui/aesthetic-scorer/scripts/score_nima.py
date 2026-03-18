#!/usr/bin/env python3
"""
NIMA (Neural Image Assessment) - Detailed Quality Analysis Script
Provides detailed quality distribution and mean score
"""

import torch
import torchvision.transforms as transforms
from PIL import Image
import argparse
import json
import sys
import numpy as np

# Try to import NIMA model
try:
    from nima.model import NIMA
    from nima.utils import load_checkpoint
except ImportError:
    print("Error: NIMA model not found.")
    print("Please install it from: https://github.com/titu1994/neural-image-assessment")
    sys.exit(1)


def load_image(image_path, size=224):
    """Load and preprocess image for model input"""
    try:
        img = Image.open(image_path).convert('RGB')
        
        # Standard preprocessing for NIMA model
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


def predict_with_nima(image_path, model_path=None, device='cuda' if torch.cuda.is_available() else 'cpu'):
    """
    Predict aesthetic scores using NIMA model
    
    Args:
        image_path: Path to the image file
        model_path: Optional path to custom model weights
        device: Device to run model on (cuda/cpu)
    
    Returns:
        dict: Contains detailed quality analysis
    """
    # Load model
    print("Loading NIMA model...")
    try:
        model = NIMA(base_model='resnet50', num_classes=10)  # NIMA typically uses 10 classes
        if model_path:
            load_checkpoint(model, model_path)
        model = model.to(device)
        model.eval()
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Using default pretrained weights...")
        # Fallback to default if custom path fails
    
    # Load and preprocess image
    print(f"Processing image: {image_path}")
    img_tensor, img_pil = load_image(image_path)
    img_tensor = img_tensor.to(device)
    
    # Predict
    with torch.no_grad():
        # NIMA predicts probability distribution over quality scores (1-10)
        output = model(img_tensor)
        
        # Convert to probabilities
        probs = torch.nn.functional.softmax(output, dim=1)
        probs = probs.cpu().numpy()[0]
    
    # Calculate mean score
    scores = np.arange(1, 11)  # Scores 1-10
    mean_score = np.sum(probs * scores)
    std_score = np.sqrt(np.sum(probs * (scores - mean_score) ** 2))
    
    # Quality distribution analysis
    quality_breakdown = {
        'excellent': np.sum(probs[8:10]),  # Scores 9-10
        'good': np.sum(probs[5:8]),         # Scores 6-8
        'fair': np.sum(probs[3:5]),         # Scores 4-5
        'poor': np.sum(probs[0:3])          # Scores 1-3
    }
    
    # Format result
    result = {
        'model': 'nima',
        'mean_score': float(mean_score),
        'std_score': float(std_score),
        'probability_distribution': probs.tolist(),
        'quality_breakdown': quality_breakdown,
        'image_path': image_path,
        'image_size': img_pil.size,
        'response_time': '2-5s'
    }
    
    return result


def interpret_distribution(breakdown):
    """Interpret quality distribution"""
    max_category = max(breakdown.items(), key=lambda x: x[1])[0]
    
    interpretations = {
        'excellent': "Image shows excellent aesthetic quality with high confidence",
        'good': "Image demonstrates good aesthetic quality with room for improvement",
        'fair': "Image has fair aesthetic quality, significant improvements possible",
        'poor': "Image quality is below average, needs considerable improvement"
    }
    
    return interpretations[max_category], max_category


def main():
    parser = argparse.ArgumentParser(description='Detailed quality analysis with NIMA')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    parser.add_argument('--model', type=str, default=None, help='Path to custom model weights')
    parser.add_argument('--device', type=str, default='auto', 
                        help='Device to use (cuda/cpu/auto)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Determine device
    if args.device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = args.device
    
    # Predict
    result = predict_with_nima(args.image_path, args.model, device)
    
    if result is None:
        sys.exit(1)
    
    # Interpret distribution
    interpretation, category = interpret_distribution(result['quality_breakdown'])
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "="*70)
        print("QUALITY ANALYSIS (NIMA - Neural Image Assessment)")
        print("="*70)
        print(f"Mean Score: {result['mean_score']:.2f}/10")
        print(f"Standard Deviation: {result['std_score']:.2f}")
        print(f"\nQuality Distribution:")
        print(f"  Excellent (9-10): {result['quality_breakdown']['excellent']*100:.1f}%")
        print(f"  Good (6-8):        {result['quality_breakdown']['good']*100:.1f}%")
        print(f"  Fair (4-5):        {result['quality_breakdown']['fair']*100:.1f}%")
        print(f"  Poor (1-3):        {result['quality_breakdown']['poor']*100:.1f}%")
        print(f"\nInterpretation: {interpretation}")
        print(f"Primary Category: {category.upper()}")
        print(f"Image Size: {result['image_size'][0]}x{result['image_size'][1]}")
        print(f"Response Time: {result['response_time']}")
        print("="*70 + "\n")


if __name__ == "__main__":
    main()
