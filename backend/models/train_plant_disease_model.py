"""
Plant Disease Detection Model Training Script
Compatible with Google Colab and local execution
Uses PlantVillage Dataset

Upload this to Google Colab and run to train the model
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
    # Dataset path (change this to your local/Colab path)
    # DATASET_PATH = "https://drive.google.com/drive/folders/1Dwmf-ToB6OvNRR1DlMgt73DVo96AvfcQ?usp=sharing"  # For Colab
    DATASET_PATH = "C:/Users/Yash Bharambe/Downloads/plantvillage/plantvillage dataset"  # For local
    
    # Model parameters
    IMAGE_SIZE = 224
    BATCH_SIZE = 32
    EPOCHS = 5
    LEARNING_RATE = 0.001
    NUM_WORKERS = 0  # Set to 0 for Windows
    
    # Model architecture
    MODEL_NAME = "efficientnet_b0"  # Options: resnet50, efficientnet_b0, mobilenet_v2
    
    # Output
    OUTPUT_PATH = "plant_disease_model.pth"  # For local
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
        image = Image.open(self.image_paths[idx]).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

# ==================== DATA LOADING ====================
def load_dataset(dataset_path):
    """Load PlantVillage dataset from directory structure"""
    print("Loading dataset...")
    
    image_paths = []
    labels = []
    class_names = set()  # Use a set to store unique class names
    
    dataset_path = Path(dataset_path)
    image_types = ['color', 'grayscale', 'segmented']  # Subfolders containing class folders
    
    # First, find all unique class names across all image types
    for image_type in image_types:
        image_type_folder = dataset_path / image_type
        if image_type_folder.is_dir():
            class_folders_in_type = [f.name for f in image_type_folder.iterdir() if f.is_dir()]
            class_names.update(class_folders_in_type)
    
    class_names = sorted(list(class_names))  # Convert set to sorted list
    class_to_idx = {name: idx for idx, name in enumerate(class_names)}
    
    # Now, load images from the specified subfolders within each class folder
    for image_type in image_types:
        image_type_folder = dataset_path / image_type
        if image_type_folder.is_dir():
            for class_name in class_names:
                class_folder = image_type_folder / class_name
                if class_folder.is_dir():
                    class_idx = class_to_idx[class_name]
                    for img_file in class_folder.glob('*.jpg'):
                        image_paths.append(str(img_file))
                        labels.append(class_idx)
                    for img_file in class_folder.glob('*.JPG'):
                        image_paths.append(str(img_file))
                        labels.append(class_idx)
                    for img_file in class_folder.glob('*.png'):
                        image_paths.append(str(img_file))
                        labels.append(class_idx)
    
    print(f"Found {len(image_paths)} images across {len(class_names)} classes")
    print(f"Classes: {class_names}")
    
    return image_paths, labels, class_names

# ==================== DATA TRANSFORMS ====================
def get_transforms():
    """Data augmentation and normalization"""
    train_transform = transforms.Compose([
        transforms.Resize((Config.IMAGE_SIZE, Config.IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
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
    """Create pretrained model"""
    print(f"Creating {Config.MODEL_NAME} model...")
    
    if Config.MODEL_NAME == "resnet50":
        model = models.resnet50(pretrained=True)
        num_features = model.fc.in_features
        model.fc = nn.Linear(num_features, num_classes)
    
    elif Config.MODEL_NAME == "efficientnet_b0":
        model = models.efficientnet_b0(pretrained=True)
        num_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(num_features, num_classes)
    
    elif Config.MODEL_NAME == "mobilenet_v2":
        model = models.mobilenet_v2(pretrained=True)
        num_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(num_features, num_classes)
    
    return model

# ==================== TRAINING FUNCTIONS ====================
def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(dataloader, desc="Training")
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
            'loss': f'{running_loss/len(dataloader):.4f}',
            'acc': f'{100.*correct/total:.2f}%'
        })
    
    return running_loss/len(dataloader), 100.*correct/total

def validate(model, dataloader, criterion, device):
    """Validate the model"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(dataloader, desc="Validation")
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix({
                'loss': f'{running_loss/len(dataloader):.4f}',
                'acc': f'{100.*correct/total:.2f}%'
            })
    
    return running_loss/len(dataloader), 100.*correct/total

# ==================== MAIN TRAINING LOOP ====================
def train_model():
    """Main training function"""
    print("="*50)
    print("Plant Disease Detection Model Training")
    print("="*50)
    
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Load dataset
    image_paths, labels, class_names = load_dataset(Config.DATASET_PATH)
    
    # Split dataset
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        image_paths, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    print(f"Training samples: {len(train_paths)}")
    print(f"Validation samples: {len(val_paths)}")
    
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
        num_workers=Config.NUM_WORKERS
    )
    val_loader = DataLoader(
        val_dataset, 
        batch_size=Config.BATCH_SIZE, 
        shuffle=False, 
        num_workers=Config.NUM_WORKERS
    )
    
    # Create model
    model = create_model(len(class_names))
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=Config.LEARNING_RATE)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', patience=3)
    
    # Training loop
    best_acc = 0.0
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }
    
    print("\nStarting training...")
    for epoch in range(Config.EPOCHS):
        print(f"\nEpoch {epoch+1}/{Config.EPOCHS}")
        print("-" * 50)
        
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
        
        print(f"\nTrain Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        
        # Save best model
        if val_acc > best_acc:
            best_acc = val_acc
            print(f"New best accuracy: {best_acc:.2f}% - Saving model...")
            
            # Save model with metadata
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
            
            # Save class names separately
            with open(Config.CLASS_NAMES_FILE, 'w') as f:
                json.dump(class_names, f, indent=2)
    
    print("\n" + "="*50)
    print(f"Training completed!")
    print(f"Best validation accuracy: {best_acc:.2f}%")
    print(f"Model saved to: {Config.OUTPUT_PATH}")
    print(f"Class names saved to: {Config.CLASS_NAMES_FILE}")
    print("="*50)
    
    # Download files in Colab
    try:
        from google.colab import files
        print("\nDownloading model files...")
        files.download(Config.OUTPUT_PATH)
        files.download(Config.CLASS_NAMES_FILE)
        print("Download complete!")
    except:
        print("\nNot in Colab environment. Files saved locally.")
    
    return model, class_names, history

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    # For Google Colab: Mount drive and set dataset path
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        print("Google Drive mounted!")
        # Uncomment and modify if dataset is in Google Drive:
        # Config.DATASET_PATH = "/content/drive/MyDrive/PlantVillage"
    except:
        print("Not in Colab environment")
    
    # Install required packages (for Colab)
    try:
        import google.colab
        print("Installing required packages...")
        os.system("pip install -q torch torchvision tqdm scikit-learn pillow")
    except:
        pass
    
    # Train model
    model, class_names, history = train_model()
    
    print("\nTraining Summary:")
    print(f"Total classes: {len(class_names)}")
    print(f"Final train accuracy: {history['train_acc'][-1]:.2f}%")
    print(f"Final validation accuracy: {history['val_acc'][-1]:.2f}%")
