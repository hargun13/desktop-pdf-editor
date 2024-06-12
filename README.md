# PDF Editor

## Overview

PDF Editor is a versatile tool that allows you to perform various operations on PDF files, such as merging multiple PDFs, removing specific pages, and managing PDF passwords (encrypting and decrypting). This tool is made with **Streamlit** leveraging **Python** and converted to a Desktop application using **Stlite**, **Electron.Js** and **Pyodide** to provide a seamless and efficient user experience.

## Features

- **PDF Merger**: Combine multiple PDF files into one.
- **PDF Page Remover**: Remove specific pages from a PDF file.
- **PDF Password Manager**: Encrypt and decrypt PDF files to manage security.

## Getting Started

### Prerequisites

Make sure you have the following installed on your system:
- Node.js (v14 or later)
- Python (v3.6 or later)
- npm (v6 or later)

### Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/your-username/pdf-editor.git
   cd pdf-editor
   ```

2. **Initialize the npm project**

   This project is already configured with a `package.json` file. If not, you can create one using:

   ```sh
   npm init -y
   ```

3. **Install the necessary packages**

   Run the following command to install all required dependencies:

   ```sh
   npm install
   ```

4. **Add your Python Streamlit project**

   Place your Python code in a single file named `app.py`. If you have multiple Python files, refer to the [@stlite/desktop documentation](https://www.npmjs.com/package/@stlite/desktop) to configure the `package.json` properly.

### Configuration

Ensure your `package.json` file is properly configured to include your Python Streamlit project. For multiple Python files, you might need to adjust the settings according to the [@stlite/desktop documentation](https://www.npmjs.com/package/@stlite/desktop).

### Building the Project

1. **Dump the project**

   Run the following command to build the project:

   ```sh
   npm run dump
   ```

2. **Serve the project**

   Check your project locally by running:

   ```sh
   npm run serve
   ```

### Exporting the Project

Once the project is ready, you can export it using:

```sh
npm run dist
```

The built application will be available in the `dist` folder.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Acknowledgements

- [Electron](https://www.electronjs.org/)
- [Streamlit](https://streamlit.io/)
- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)

---

More features may be added soon, Stay Tuned!✌️
