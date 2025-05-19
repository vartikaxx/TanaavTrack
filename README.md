# TanaavTrack - Remote Work Stress Tracker

TanaavTrack is a web application built with Flask that helps remote workers track their stress levels and receive personalized recommendations for managing stress. The application uses a form-based approach to collect various metrics about work habits and environment, then provides tailored suggestions for songs, movies, and activities based on the calculated stress level.

## Features

- Comprehensive stress assessment form
- Real-time stress level calculation
- Personalized recommendations based on stress level:
  - Music suggestions
  - Movie recommendations
  - Activity recommendations
- Beautiful, responsive user interface
- Form validation
- Clear results presentation

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tanaavtrack.git
cd tanaavtrack
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
```bash
python app.py
```
3. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Fill out the stress assessment form with your information
2. Submit the form to receive your stress analysis
3. Review your stress score and personalized recommendations
4. Use the "Take the Test Again" button to perform another assessment

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask web framework
- Flask-WTF for form handling
- Bootstrap for styling inspiration 