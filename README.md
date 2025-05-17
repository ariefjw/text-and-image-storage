# Text and Image Storage Application

A web application built with Flask for storing and managing text and images. This application allows users to upload, view, download, and delete text entries and images.

## Features

- Store and manage text entries
- Upload and display images
- Download images
- Delete stored texts and images
- Modern and responsive UI with Bootstrap 5
- Flash messages for user feedback
- Vercel deployment ready

## Tech Stack

- Python 3.x
- Flask 2.0.1
- Bootstrap 5
- Pillow (for image processing)
- Vercel (for deployment)

## Local Development Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

### Adding Text
1. Enter your text in the text area
2. Click "Save Text" to store it

### Managing Images
1. Click "Choose File" to select an image
2. Click "Upload Image" to store it
3. Use the "Download" button to save images to your device
4. Use the "Delete" button to remove images
5. Supported formats: PNG, JPG, JPEG, GIF

## Project Structure

```
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel configuration
├── templates/         # HTML templates
│   └── index.html    # Main template
├── static/           # Static files (if any)
└── README.md         # This file
```

## Deployment

This application is configured for deployment on Vercel. To deploy:

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel
```

## Environment Variables

For production deployment, set the following environment variables:
- `SECRET_KEY`: Your Flask secret key

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation
- Bootstrap 5
- Vercel platform 