import face_recognition
import os
import pickle

def train_model(images_dir, encodings_file):
    print(f"Loading images from directory: {images_dir}")

    known_encodings = []
    known_names = []

    # Define allowed image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}

    for person_name in os.listdir(images_dir):
        person_folder = os.path.join(images_dir, person_name)
        if os.path.isdir(person_folder):
            for image_file in os.listdir(person_folder):
                # Check if the file is an image
                if not any(image_file.lower().endswith(ext) for ext in image_extensions):
                    continue

                image_path = os.path.join(person_folder, image_file)

                try:
                    # Load image and get face encodings
                    image = face_recognition.load_image_file(image_path)
                    encoding = face_recognition.face_encodings(image)

                    if encoding:
                        known_encodings.append(encoding[0])
                        known_names.append(person_name)
                except Exception as e:
                    print(f"Error processing image {image_path}: {e}")

    if not known_encodings:
        raise ValueError("No images found in the directory or no faces detected.")

    with open(encodings_file, 'wb') as f:
        pickle.dump((known_encodings, known_names), f)

    print(f"Model saved to {encodings_file}")

if __name__ == "__main__":
    images_dir = '/train/images'
    encodings_file = '/train/face_encodings.pkl'
    train_model(images_dir, encodings_file)
