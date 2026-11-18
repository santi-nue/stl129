
Example create jpg:    paste this:


```python

from pathlib import Path
from PIL import Image
import os 
from jnius import autoclass # Get Android's Pictures folder

Environment = autoclass("android.os.Environment")

pictures_dir = Environment.getExternalStoragePublicDirectory( Environment.DIRECTORY_DOWNLOADS )

INPUT_DIR = os.path.join(pictures_dir.getAbsolutePath() ,"Screenshots" )

OUTPUT_DIR = Path(pictures_dir.getAbsolutePath()) / "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

cropped_images = []

combined_path = os.path.join(OUTPUT_DIR, "out.jpg" )

for file_name in sorted(os.listdir(INPUT_DIR)):
    if not file_name.lower().endswith(".jpg"):
        continue

    image_path = os.path.join(INPUT_DIR, file_name)
    output_path = os.path.join(OUTPUT_DIR, file_name)

    with Image.open(image_path) as img:
        cropped = img.crop((0, 75, img.width, 270))

        if cropped.mode != "RGB":
            cropped = cropped.convert("RGB")

        cropped.save(output_path, "JPEG", quality=95)

        cropped_images.append(cropped)

if cropped_images:
    target_width = cropped_images[0].width

    resized_images = []

    for image in cropped_images:
        if image.width != target_width:
            new_height = round(image.height * target_width / image.width)
            image = image.resize((target_width, new_height))

        resized_images.append(image)

    total_width = target_width
    total_height = sum(image.height for image in resized_images)

    combined = Image.new("RGB", (total_width, total_height), "white")

    y_position = 0

    for image in resized_images:
        combined.paste(image, (0, y_position))
        y_position += image.height

    combined.save(combined_path, "JPEG", quality=95)

print("end program") 

```

Example wr rd in file:    paste this:


```python

import os
from jnius import autoclass

# Get Android's Download folder
Environment = autoclass("android.os.Environment")
downloads = Environment.getExternalStoragePublicDirectory(
    Environment.DIRECTORY_DOWNLOADS
)

# Full path: /storage/emulated/0/Download/kivy_test.txt
file_path = os.path.join(
    downloads.getAbsolutePath(),
    "kivy_test.txt"
)

print("File path:")
print(file_path)

# Write to the file
with open(file_path, "w", encoding="utf-8") as file:
    file.write("Hello Kivy!")

# Read the file back
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

print("\nRead from file:")
print(text)

```

Example list libs installed:    paste this:

```python

from importlib.metadata import distributions

packages = []

for package in distributions():
    name = package.metadata["Name"]
    version = package.metadata["Version"]
    packages.append(f"{name} {version}")

packages.sort()

print(f"Installed packages: {len(packages)}\n")

for package in packages:
    print(package)

```

# Kivy Launcher

(work in progress, not yet published on Google Play)

This is a reboot of the previously pygame/kivy launcher, implemented in Java in Python for android. It was barely maintainable, and with the rewrite of the new Python for android, it was lost.

This version aimed to provide a replacement for the launcher, but works also on desktop, on Python 2 or 3.

Anybody can clone the repo, add the dependencies we would not provide by default, and recompile it.

![kivy-launcher](https://user-images.githubusercontent.com/37904/37256979-0611d5be-2563-11e8-98a6-485e656b0f4b.png)

## How it works

Follow the guide the same as before:

https://kivy.org/docs/guide/packaging-android.html#packaging-your-application-for-the-kivy-launcher

Then just start the launcher, you should see your application listed, then press play.

## `android.txt` specification

- `title`: Title of the application
- `author`: Author of the application
- `orientation`: Default orientation, one of "landscape", "portrait", "sensor"

## Works

- Provide a simple UI to discover and start another app
- Start another main.py as a `__name__ == '__main__'`
- Reduce to the minimum the overhead of the launcher to launch another app
- Support landscape / portrait / sensor

## Ideas

- Act as a server to just launch any Kivy-based app from desktop to mobile
- Ability to configure multiple paths to look for applications
- Different ordering: by name, last updated, size
- Add tiny icon to show what application orientation is
- Allow to change multiple configuration token / environemnt (like different density/dpi to simulate other screens)
- Support for application without "android.txt"
