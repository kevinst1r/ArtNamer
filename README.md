
# Art Namer

## Introduction
Art Namer leverages OpenAI's AI algorithms for creative image analysis and naming. Designed for artists and designers, it offers a unique blend of AI-driven insights and user interaction to generate and refine image titles.

<img src='https://drive.google.com/uc?export=view&id=147Tme-MxEmqCSDaU3SPzR_78-QqAbZur'>

## Installation
To install Art Namer, follow these steps:
1. Ensure you have Python installed on your system. Art Namer requires Python 3.10 or later.
2. Download the source code for Art Namer from the repository.
3. Run the `Install.bat` script by double-clicking it. This script will install Python (if not already installed) and all required dependencies.
4. After the installation is complete, you can start the application by running `Run.bat`.

## Usage
To use Art Namer, follow these steps:
1. Start the application by executing `Run.bat`.
2. The main window will appear, where you can upload images for analysis.
3. Use the naming window to generate and refine titles for your images based on AI analysis.
4. Adjust settings if necessary in the settings window.

## Features
- AI-Powered Image Analysis: Utilizes OpenAI for in-depth image analysis and creative title generation.
- Interactive Naming Window: A dedicated interface for viewing images, receiving AI-generated analysis and titles, and refining selections.
- Spell Check: Integrated spell checking in user input fields.
- Customizable User Interaction: Options to save, copy, or regenerate analysis and titles, enhancing user engagement.

## Main User Interface
- Image Display and Navigation: Users can view images and navigate through their collection.
- Analysis and Title Generation: The application analyzes the current image and suggests titles, which are displayed in an interactive format.
- User Context Input: A text field allows users to provide context or instructions for the AI, enhancing the relevance of generated titles.
- Regeneration and Saving Options: Users can regenerate titles, save analysis, and copy content to the clipboard.
- Title Selection and Customization: The interface includes checkboxes and buttons for selecting and customizing titles, with spell-check functionality.
- Clicking the title renames the file to the  chosen name and moves to the next image.

## Dependencies
- PyQt5
- OpenAI
- python-dotenv
- PyEnchant

## Configuration (IMPORTANT)
Set your OpenAI API key in the `.env` file. Copy `.env.example` to a new file named `.env` and replace the placeholder with your actual OpenAI API key.

## Examples
An example scenario involves the user uploading an image, providing context, and using the AI-generated analysis and titles to come up with a unique name for the artwork.

## Troubleshooting
If you encounter any issues:
- Ensure all dependencies are correctly installed.
- Check if the OpenAI API key is set correctly in the `.env` file.
- Restart the application after making changes to the settings or environment variables.

UI Assets Generated with the <a href="https://chat.openai.com/g/g-H0UwwgFOe-ui-asset-generator">UI Asset Generator</a> Custom GPT.
