# PlatinumAI API: Advanced AI API with Auto-Provider Selection, Database Integration, and Streaming

**PlatinumAI API** is an open-source project that provides a versatile AI API, offering advanced features like automatic provider selection, seamless database integration, and streaming capabilities. Designed for developers and AI enthusiasts, PlatinumAI API simplifies the process of integrating and managing AI functionalities in applications.

## Key Features
- **Auto-Provider Selection:** Dynamically selects the best AI provider based on performance metrics and availability, ensuring optimal responses.
- **Database Integration:** Utilizes MongoDB for efficient data storage and retrieval, enabling stateful interactions and data persistence.
- **Streaming Support:** Provides real-time data streaming for interactive and responsive AI experiences.

## Getting Started

To set up PlatinumAI API, follow these steps:

1. **Get a MongoDB URI:**
   - Sign up for a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Create a new database and obtain the connection URI.

2. **Install Requirements:**
   - Clone the repository and navigate to the project directory.
   - Install the necessary dependencies by running:
     ```
     pip install -r requirements.txt
     ```

3. **Configure the API:**
   - Replace the placeholder values in the configuration file with your own:
     - **MongoDB URI:** Update the connection string with the URI obtained from MongoDB Atlas.
     - **API Key:** Add your API key(s) for the AI providers you wish to use.
   - Ensure all necessary configurations and permissions are set.

4. **Deploy the API:**
   - You can run the API locally or deploy it on cloud hosting platforms like [Render](https://render.com), [Bot Hosting](https://bot-hosting.net), or [Pylex Nodes](https://pylexnodes.net).
   - To start the API, run:
     ```
     python api.py
     ```

## Usage

Once deployed, the PlatinumAI API can be accessed via HTTP requests. For detailed documentation on available endpoints and usage examples, please refer to the [API Documentation](docs/README.md).

## Contributing

PlatinumAI API is an open-source project, and contributions are welcome! Whether you're fixing bugs, adding new features, or enhancing documentation, your contributions are valuable. Please follow our [contribution guidelines](CONTRIBUTING.md) and adhere to the [code of conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the Unlicense. See the [LICENSE](LICENSE) file for more information.
