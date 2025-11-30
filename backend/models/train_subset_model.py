"""
ALL CLASSES TRAINING - Complete PlantVillage Dataset with MobileNetV2
Trains on ALL ~38 disease classes with 300 images each (~11,400 total)
MobileNetV2 is 2-3x faster than EfficientNet on CPU
Better coverage + reasonable training time - perfect for hybrid mode!
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from PIL import Image
import os
import json
from pathlib import Path
from tqdm import tqdm
import numpy as np
from sklearn.model_selection import train_test_split

# ==================== CONFIGURATION ====================
class Config:
    DATASET_PATH = "C:/Users/Yash Bharambe/Downloads/plantvillage/plantvillage dataset"
    
    # ALL CLASSES - Train on complete PlantVillage dataset
    # Will auto-discover all classes (should be ~38 classes)
    SELECTED_CLASSES = None  # None = use ALL classes
    
    # Model parameters - OPTIMIZED with MobileNetV2 (faster than EfficientNet)
    IMAGE_SIZE = 224
    BATCH_SIZE = 32  # Good for CPU
    EPOCHS = 5  # 5 epochs for decent accuracy
    LEARNING_RATE = 0.001
    NUM_WORKERS = 0
    MAX_IMAGES_PER_CLASS = 400  # 400 images per class - balanced for all classes
    
    # Model architecture - using MobileNet for faster CPU training
    MODEL_NAME = "mobilenet_v2"
    
    # Output
    OUTPUT_PATH = "plant_disease_model.pth"
    CLASS_NAMES_FILE = "class_names.json"

# ==================== DATASET CLASS ====================
class PlantDiseaseDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        try:
            image = Image.open(self.image_paths[idx]).convert('RGB')
            label = self.labels[idx]
            
            if self.transform:
                image = self.transform(image)
            
            return image, label
        except Exception as e:
            print(f"Error loading {self.image_paths[idx]}: {e}")
            # Return a black image as fallback
            return torch.zeros((3, Config.IMAGE_SIZE, Config.IMAGE_SIZE)), self.labels[idx]

# ==================== DATA LOADING ====================
def load_dataset(dataset_path):
    """Load PlantVillage dataset - ALL CLASSES or SELECTED CLASSES"""
    dataset_path = Path(dataset_path)
    image_types = ['color']  # Use only color images for speed
    
    # Auto-discover all classes if SELECTED_CLASSES is None
    if Config.SELECTED_CLASSES is None:
        print("🔍 Auto-discovering ALL disease classes...")
        all_classes = set()
        for image_type in image_types:
            image_type_folder = dataset_path / image_type
            if image_type_folder.is_dir():
                for class_folder in image_type_folder.iterdir():
                    if class_folder.is_dir():
                        all_classes.add(class_folder.name)
        selected_classes = sorted(list(all_classes))
        print(f"✅ Found {len(selected_classes)} disease classes")
    else:
        selected_classes = Config.SELECTED_CLASSES
        print(f"📋 Using {len(selected_classes)} selected disease classes")
    
    image_paths = []
    labels = []
    class_to_idx = {name: idx for idx, name in enumerate(selected_classes)}
    
    # Load images for selected classes
    for image_type in image_types:
        image_type_folder = dataset_path / image_type
        if image_type_folder.is_dir():
            for class_name in selected_classes:
                class_folder = image_type_folder / class_name
                if class_folder.is_dir():
                    class_idx = class_to_idx[class_name]
                    class_images = []
                    
                    # Collect all images for this class
                    for ext in ['*.jpg', '*.JPG', '*.png', '*.PNG']:
                        class_images.extend(list(class_folder.glob(ext)))
                    
                    # Limit images per class
                    if len(class_images) > Config.MAX_IMAGES_PER_CLASS:
                        import random
                        random.seed(42)
                        class_images = random.sample(class_images, Config.MAX_IMAGES_PER_CLASS)
                    
                    for img_file in class_images:
                        image_paths.append(str(img_file))
                        labels.append(class_idx)
    
    print(f"✓ Total images: {len(image_paths)}")
    print(f"✓ Total classes: {len(selected_classes)}")
    print(f"✓ Average per class: {len(image_paths)//len(selected_classes)} images")
    print(f"\n📊 Disease Classes:")
    for i, cls in enumerate(selected_classes):
        count = labels.count(i)
        print(f"  {i+1}. {cls}: {count} images")
    
    return image_paths, labels, selected_classes

# ==================== DATA TRANSFORMS ====================
def get_transforms():
    """Enhanced data augmentation for better quality with less data"""
    train_transform = transforms.Compose([
        transforms.Resize((Config.IMAGE_SIZE, Config.IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.2),
        transforms.RandomRotation(30),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((Config.IMAGE_SIZE, Config.IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform

# ==================== MODEL ARCHITECTURE ====================
def create_model(num_classes):
    """Create pretrained MobileNetV2 model (faster for CPU)"""
    print(f"Creating {Config.MODEL_NAME} model...")
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)
    return model

# ==================== TRAINING FUNCTIONS ====================
def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(dataloader, desc="Training", ncols=100)
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({
            'loss': f'{running_loss/(pbar.n+1):.3f}',
            'acc': f'{100.*correct/total:.1f}%'
        })
    
    return running_loss/len(dataloader), 100.*correct/total

def validate(model, dataloader, criterion, device):
    """Validate the model"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(dataloader, desc="Validation", ncols=100)
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix({
                'loss': f'{running_loss/(pbar.n+1):.3f}',
                'acc': f'{100.*correct/total:.1f}%'
            })
    
    return running_loss/len(dataloader), 100.*correct/total

# ==================== MAIN TRAINING LOOP ====================
def train_model():
    """Main training function"""
    print("="*60)
    print("🌱 FAST QUALITY TRAINING - Plant Disease Detection")
    print("="*60)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    if device.type == 'cpu':
        print("⚠️  Training on CPU - Will take 1-2 hours")
    
    # Load dataset
    image_paths, labels, class_names = load_dataset(Config.DATASET_PATH)
    
    if len(image_paths) == 0:
        print("❌ ERROR: No images found! Check dataset path.")
        return None, None, None
    
    # Split dataset
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        image_paths, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    print(f"\n📊 Dataset Split:")
    print(f"   Training: {len(train_paths)} images")
    print(f"   Validation: {len(val_paths)} images")
    
    # Get transforms
    train_transform, val_transform = get_transforms()
    
    # Create datasets
    train_dataset = PlantDiseaseDataset(train_paths, train_labels, train_transform)
    val_dataset = PlantDiseaseDataset(val_paths, val_labels, val_transform)
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=Config.BATCH_SIZE,
        shuffle=True,
        num_workers=Config.NUM_WORKERS,
        pin_memory=(device.type == 'cuda')
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=Config.BATCH_SIZE,
        shuffle=False,
        num_workers=Config.NUM_WORKERS,
        pin_memory=(device.type == 'cuda')
    )
    
    # Create model
    model = create_model(len(class_names))
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=Config.LEARNING_RATE)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', patience=2, factor=0.5)
    
    # Training loop
    best_acc = 0.0
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }
    
    print(f"\n🚀 Starting training for {Config.EPOCHS} epochs...")
    print("="*60)
    
    for epoch in range(Config.EPOCHS):
        print(f"\n📍 Epoch {epoch+1}/{Config.EPOCHS}")
        print("-" * 60)
        
        # Train
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        
        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        # Update learning rate
        scheduler.step(val_acc)
        
        # Save history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        print(f"\n📊 Results:")
        print(f"   Train - Loss: {train_loss:.4f} | Acc: {train_acc:.2f}%")
        print(f"   Val   - Loss: {val_loss:.4f} | Acc: {val_acc:.2f}%")
        
        # Save best model
        if val_acc > best_acc:
            best_acc = val_acc
            print(f"   ✨ NEW BEST: {best_acc:.2f}% - Saving model...")
            
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'class_names': class_names,
                'num_classes': len(class_names),
                'best_acc': best_acc,
                'model_name': Config.MODEL_NAME,
                'image_size': Config.IMAGE_SIZE,
                'history': history
            }, Config.OUTPUT_PATH)
            
            with open(Config.CLASS_NAMES_FILE, 'w') as f:
                json.dump(class_names, f, indent=2)
    
    print("\n" + "="*60)
    print("🎉 TRAINING COMPLETED!")
    print(f"✅ Best Validation Accuracy: {best_acc:.2f}%")
    print(f"💾 Model saved: {Config.OUTPUT_PATH}")
    print(f"📋 Classes saved: {Config.CLASS_NAMES_FILE}")
    print("="*60)
    
    return model, class_names, history

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("FAST QUALITY TRAINING MODE")
    print("Training subset for presentation & testing")
    print("="*60 + "\n")
    
    model, class_names, history = train_model()
    
    if model and history:
        print("\n📈 TRAINING SUMMARY:")
        print(f"   Total classes: {len(class_names)}")
        print(f"   Final train acc: {history['train_acc'][-1]:.2f}%")
        print(f"   Final val acc: {history['val_acc'][-1]:.2f}%")
        print(f"\n✅ Model ready for testing!")
        print(f"   Restart backend to use this model automatically")
