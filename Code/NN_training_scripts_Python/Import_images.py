import os
from openimages.download import download_images

def download_mixed_dataset(output_dir, class_groups, limit_per_label=20):
    """
    Downloads a mix of images from OpenImages for testing.

    Args:
        output_dir (str): Directory to save the downloaded images.
        class_groups (dict): {"birds": [labels...], "non_birds": [labels...]}
        limit_per_label (int): Max images per label.
    """
    os.makedirs(output_dir, exist_ok=True)

    exclusions_path = os.path.join(output_dir, "exclusions.txt")
    if not os.path.exists(exclusions_path):
        with open(exclusions_path, "w") as f:
            f.write("")

    for group, labels in class_groups.items():
        print(f"\n📂 Downloading group: {group}")
        group_dir = os.path.join(output_dir, group)
        os.makedirs(group_dir, exist_ok=True)

        for label in labels:
            try:
                print(f"🔽 Downloading label: {label}")
                download_images(
                    dest_dir=group_dir,          # use correct arg name
                    class_labels=[label],
                    exclusions_path=exclusions_path,
                    limit=limit_per_label
                )
            except Exception as e:
                print(f"⚠️ Failed for label '{label}': {e}")

    print("\n✅ All downloads complete!")

if __name__ == "__main__":
    out_dir = r"<path>"

    # Define bird-related and non-bird categories
    class_groups = {
            "Bird",
            "Eagle",
            "Swan",
            "Pigeon",
            "Duck",
            "Owl",
            "Penguin",
            "Peacock",
            "Crow",
            "Flamingo",
            "City",
            "Street",
            "Building",
            "Car",
            "Tree",
            "Sky",
            "People",
            "Boat",
            "Lake",
            "Mountain",
            "Sktscraper",
            "Pizza",
            "Phone",
            "Airplane"
        
    }

    download_mixed_dataset(out_dir, class_groups, limit_per_label=20)
