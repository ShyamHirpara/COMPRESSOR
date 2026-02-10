# Magical Image Compressor

A powerful, user-friendly, and open-source image compression tool built with Django and Pillow.

**Live Demo:** [https://magiccompressor.onrender.com/](https://magiccompressor.onrender.com/)

---

## How to Use This App

### Step 1: Upload Your Image

- **Drag & Drop** your image file into the designated area or **Click to Select** a file from your device.
- **Constraints:**
    - Supported format: **JPEG/JPG**
    - **Maximum File Size: 45MB** (This limit is enforced on the client-side for immediate feedback).
- Once selected, the image will upload automatically. A progress indicator will show the status.
- Upon successful upload, the filename will be displayed with a "Uploaded" checkmark.

![Upload Image][Image-1]

![Select image under 45MB][Image-2]

### Step 2: Select Compression Level

Choose the compression strength that best fits your needs:

| Level      | Ideal For                                 | Target Size (Approx.) | Max Dimension | Quality Range |
| :--------- | :---------------------------------------- | :-------------------- | :------------ | :------------ |
| **Normal** | High-quality photos, minimal loss.        | ~2.0 MB               | 4000px        | 75-95         |
| **Super**  | Sharing on social media or messaging.     | ~500 KB               | 2000px        | 50-80         |
| **Ultra**  | Thumbnails, icons, or strict size limits. | ~200 KB               | 1200px        | 30-60         |

![Select Compression Level][Image-3]

### Step 3: Select Output Format

Choose the desired file format for your compressed image:

- **JPEG:** Standard for photography, good compatibility.
- **PNG:** Lossless compression, best for graphics with sharp edges.
- **WEBP:** Modern format providing superior compression for the web.

![Select Export Format][Image-4]

### Step 4: Compress & Download

1.  Click the **"Compress Image 🚀"** button. An overlay will appear showing the progress of the compression.
2.  Once complete, a **"Compressed Result"** card will appear below.
3.  This card displays:
    - A preview of the compressed image.
    - The new file size (e.g., `0.45 MB`).
    - The final format.
4.  Click the **"Download"** button to save the optimized image to your device.
    ![Compress Image][Image-5]

    ![Download Image][Image-6]

---

## How This App Was Made (From Scratch to Full Functionality)

This application was developed using a modern Python web stack, focusing on performance, user experience, and efficient resource management.

### Backend Development (Django & Python)

1.  **Project Initialization:** Started with a standard Django project structure (`django-admin startproject`).
2.  **Image Processing Core (Pillow):**
    - Integrated the `Pillow` library to handle image manipulation.
    - Implemented a smart compression logic that not only adjusts quality but also intelligently resizes images based on the selected "Level" (Normal, Super, Ultra) to meet target file sizes.
    - Added support for format conversion (JPEG -> PNG/WEBP).
    - **Optimization:** Implemented a binary search algorithm for JPEG/WEBP quality adjustments to hit target file sizes as closely as possible.
3.  **File Management:**
    - Used Django's `FileSystemStorage` for handling uploads.
    - **Session-Based Cleanup:** Implemented a system where uploaded files are tracked via user sessions. When a new file is uploaded, the previous one associated with that session is automatically deleted. This ensures the server storage remains clean without requiring user accounts or complex scheduled tasks.
4.  **Security & Limits:**
    - Configured `settings.py` for security (allowed hosts, static files).
    - **Decompression Bomb Protection:** Adjusted Pillow settings to safely handle large images (up to the 45MB app limit).

### Frontend Development (HTML/CSS/JS)

1.  **Modern UI/UX:**
    - Designed a clean, dark-themed interface using standard CSS variables for easy theming.
    - Implemented a **Theme Toggle** to switch between Dark and Light modes.
    - Used CSS Grid and Flexbox for a responsive layout that works on mobile and desktop.
2.  **Dynamic Interactions (JavaScript):**
    - **AJAX for Everything:** The app does not reload the page for uploads or compression. It uses `XMLHttpRequest` and the `Fetch API` to communicate with Django views asynchronously.
    - **Real-time Feedback:** Added progress bars for uploads and a "processing" overlay for compression tasks.
    - **Client-Side Validation:** JavaScript checks the file size (45MB limit) _before_ the upload starts to save bandwidth and give instant feedback.

### Deployment & DevOps

This project is deployed on **Render** using a robust production configuration. Below are the steps and commands used to host the application.

#### 1. Configuration Setup

- **Dependencies:** `gunicorn` (WSGI Interface) and `whitenoise` (Static File Serving) are included in `requirements.txt`.
- **Gunicorn Config:** A custom `src/gunicorn_config.py` manages workers, threads, and timeouts to handle image processing loads efficiently.
- **Static Files:** `settings.py` is configured with `STATIC_ROOT` and `Whitenoise` middleware to serve assets in production.

#### 2. Render Deployment Configuration

To deploy this project, the following settings were used for the Web Service:

- **Build Command:**

    ```bash
    pip install -r requirements.txt && python src/manage.py collectstatic --noinput
    ```

    _Installs dependencies and gathers static files into the servable directory._

- **Start Command:**
    ```bash
    cd src && gunicorn -c gunicorn_config.py compressor.wsgi:application
    ```
    _Starts the Gunicorn server from the `src` directory using the custom config._

#### 3. Environment Variables

Sensitive keys are not stored in the repo. The following are set in the Render Dashboard:

- `PYTHON_VERSION`: `3.11.0` (Ensures compatibility)
- `DEBUG`: `False` (Production mode)
- `SECRET_KEY`: _[Production Secret Key]_

---

## How to Use Via Live URL

The application is deployed and accessible directly via the web. You do not need to install anything.

**URL:** [https://magiccompressor.onrender.com/](https://magiccompressor.onrender.com/)

1.  Open the link in any modern web browser (Chrome, Firefox, Safari, Edge).
2.  The application is fully responsive and works on both **Desktop** and **Mobile** devices.
3.  Follow the steps outlined in this file to compress your images instantly.

[Image-1]: https://private-user-images.githubusercontent.com/195340508/546814183-c484ab25-78ca-4f74-b741-eb6d1a9e985b.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA3NTI5NTMsIm5iZiI6MTc3MDc1MjY1MywicGF0aCI6Ii8xOTUzNDA1MDgvNTQ2ODE0MTgzLWM0ODRhYjI1LTc4Y2EtNGY3NC1iNzQxLWViNmQxYTllOTg1Yi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjEwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIxMFQxOTQ0MTNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iMzI4ODRhODg4MGJlMGI1NDAxYjA1YzBiMTNiYzYzOTM3MWQxYjQwMTMyMWU5NzM3ZDVlYTJkOTBmMjUyOGVhJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.H3ajgtbO76Ks8apIlWBVlsPttJHj6755qQIjlXBMIgs
[Image-2]: https://private-user-images.githubusercontent.com/195340508/546814256-2e4f8a55-2bd4-4ade-9764-7cdf979ca46c.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA3NTM0NjMsIm5iZiI6MTc3MDc1MzE2MywicGF0aCI6Ii8xOTUzNDA1MDgvNTQ2ODE0MjU2LTJlNGY4YTU1LTJiZDQtNGFkZS05NzY0LTdjZGY5NzljYTQ2Yy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjEwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIxMFQxOTUyNDNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT04NTM5YjYxMzdjMWJiNmJjM2JhNjQwMzViNmRhNDBmNzc4ZDM2ZmUyYWM1NTZmZDc5NTQ4YzgyMDI5OWE5MDhkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.ce1q9AQQXtaCzcSfFe6AoVY777MJ1TyDWF5r-YPHMdE
[Image-3]: https://private-user-images.githubusercontent.com/195340508/546814498-7234cad5-2c94-430d-81c3-d452efea8381.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA3NTM1MTcsIm5iZiI6MTc3MDc1MzIxNywicGF0aCI6Ii8xOTUzNDA1MDgvNTQ2ODE0NDk4LTcyMzRjYWQ1LTJjOTQtNDMwZC04MWMzLWQ0NTJlZmVhODM4MS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjEwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIxMFQxOTUzMzdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mNzAxNTBhNjYyYTA5NDUyNzVlNDI3NmFhMDI4N2ViMzI4NzE3MmM0ODYyNDkzZTU3NDc4MzlmZmExZWM1ZjI1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.1fP92QzVHVfYewdoXDQjJadKTcvfTw5QatSb7BGGy9A
[Image-4]: https://private-user-images.githubusercontent.com/195340508/546814531-36099b4e-8e91-4a31-8093-e953ccd259f4.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA1ODUwNjksIm5iZiI6MTc3MDU4NDc2OSwicGF0aCI6Ii8xOTUzNDA1MDgvNTQ2ODE0NTMxLTM2MDk5YjRlLThlOTEtNGEzMS04MDkzLWU5NTNjY2QyNTlmNC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjA4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIwOFQyMTA2MDlaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT02NjVhNTkyNjhmZGZkNzkwOTRkYzEyYzQzNmJlYzY2ODU2MmNhZTFkN2RkMjFhMmQ5ZGJkZjI3OTJkMTkwZDA4JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.7Bc-HMc6woQUgxo3A1udm8GpRy25viVTTuv5SIDCuCI
[Image-5]: https://private-user-images.githubusercontent.com/195340508/546814588-10bfefb7-a14e-4cb0-aea4-af8e04637934.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA1ODUwOTMsIm5iZiI6MTc3MDU4NDc5MywicGF0aCI6Ii8xOTUzNDA1MDgvNTQ2ODE0NTg4LTEwYmZlZmI3LWExNGUtNGNiMC1hZWE0LWFmOGUwNDYzNzkzNC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjA4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIwOFQyMTA2MzNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iN2JjNjEyYzc3OTU5NjUwYjhjNDNjOGI2MmUyMTExY2EwNjkyMTgzYTEwYjViODEzMjVhZTNlMmI0ODc5ZTc1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.EO6kXpEXNSQHye5FuQsp4fHpIfc9JfwNl5uVqZ19JuI
[Image-6]: https://private-user-images.githubusercontent.com/195340508/546814598-b78696d5-c220-4c4a-8f89-fb06ea97d3dc.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA1ODUxMDQsIm5iZiI6MTc3MDU4NDgwNCwicGF0aCI6Ii8xOTUzNDA1MDgvNTQ2ODE0NTk4LWI3ODY5NmQ1LWMyMjAtNGM0YS04Zjg5LWZiMDZlYTk3ZDNkYy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjA4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIwOFQyMTA2NDRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT04YjIwZDBkNjUzYjZkNmQ5ZDM0ZGU1ZDJhYjM0ZGM0OGU3ZWQ1ODM0MTMyZjFiNmY2ZTc4MDY2MWNjMmJiMjVhJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.bJ8GgVclR3ui3NZl5qSw4lxdZ_GeOJKKYr8Cgwzu7mk
