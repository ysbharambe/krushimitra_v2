"""
Custom Plant Disease Model Inference
Compatible with the trained model from train_plant_disease_model.py
"""

import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import json

class PlantDiseasePredictor:
    def __init__(self, model_path, class_names_path=None):
        """
        Initialize the predictor
        
        Args:
            model_path: Path to the trained .pth model file
            class_names_path: Path to class_names.json (optional if included in model)
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load model checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        
        # Get model metadata
        self.class_names = checkpoint['class_names']
        self.num_classes = checkpoint['num_classes']
        self.model_name = checkpoint['model_name']
        self.image_size = checkpoint.get('image_size', 224)
        
        # Load class names from separate file if provided
        if class_names_path:
            with open(class_names_path, 'r') as f:
                self.class_names = json.load(f)
        
        # Create model architecture
        self.model = self._create_model()
        
        # Load trained weights
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Define preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((self.image_size, self.image_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        print(f"Model loaded successfully!")
        print(f"Architecture: {self.model_name}")
        print(f"Classes: {self.num_classes}")
        print(f"Device: {self.device}")
    
    def _create_model(self):
        """Recreate the model architecture"""
        if self.model_name == "resnet50":
            model = models.resnet50(pretrained=False)
            num_features = model.fc.in_features
            model.fc = nn.Linear(num_features, self.num_classes)
        
        elif self.model_name == "efficientnet_b0":
            model = models.efficientnet_b0(pretrained=False)
            num_features = model.classifier[1].in_features
            model.classifier[1] = nn.Linear(num_features, self.num_classes)
        
        elif self.model_name == "mobilenet_v2":
            model = models.mobilenet_v2(pretrained=False)
            num_features = model.classifier[1].in_features
            model.classifier[1] = nn.Linear(num_features, self.num_classes)
        
        else:
            raise ValueError(f"Unknown model: {self.model_name}")
        
        return model
    
    def predict(self, image_path_or_pil):
        """
        Predict disease from image
        
        Args:
            image_path_or_pil: Path to image file or PIL Image object
        
        Returns:
            dict: {
                'disease_name': str,
                'confidence': float (0-100),
                'all_predictions': list of top 5 predictions
            }
        """
        # Load image
        if isinstance(image_path_or_pil, str):
            image = Image.open(image_path_or_pil).convert('RGB')
        else:
            image = image_path_or_pil.convert('RGB')
        
        # Preprocess
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Predict
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            # Get top 5 predictions
            top5_prob, top5_idx = torch.topk(probabilities, min(5, self.num_classes))
            
            top5_predictions = []
            for prob, idx in zip(top5_prob[0], top5_idx[0]):
                top5_predictions.append({
                    'disease': self.class_names[idx.item()],
                    'confidence': prob.item() * 100
                })
            
            # Get best prediction
            best_idx = top5_idx[0][0].item()
            best_prob = top5_prob[0][0].item() * 100
            disease_name = self.class_names[best_idx]
        
        return {
            'disease_name': disease_name,
            'confidence': round(best_prob, 2),
            'all_predictions': top5_predictions
        }
    
    def predict_from_url(self, image_url):
        """
        Predict disease from image URL
        
        Args:
            image_url: URL of the image
        
        Returns:
            dict: Prediction results
        """
        import requests
        from io import BytesIO
        
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        
        return self.predict(image)

# ==================== STANDALONE TESTING ====================
if __name__ == "__main__":
    # Test the predictor
    MODEL_PATH = "plant_disease_model.pth"
    
    try:
        predictor = PlantDiseasePredictor(MODEL_PATH)
        
        print("\nPredictor ready!")
        print(f"Loaded {len(predictor.class_names)} classes")
        print("\nSample classes:")
        for i, cls in enumerate(predictor.class_names[:5]):
            print(f"  {i+1}. {cls}")
        
        # Test prediction (replace with actual image path)
        # result = predictor.predict("path/to/test/image.jpg")
        # print(f"\nPrediction: {result}")
        
    except FileNotFoundError:
        print(f"Error: Model file not found at {MODEL_PATH}")
        print("Please train the model first using train_plant_disease_model.py")
    except Exception as e:
        print(f"Error loading model: {e}")
