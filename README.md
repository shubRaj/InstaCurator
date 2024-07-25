# Instacurator

## Overview
When I'm bored, I sometimes go through Instagram reels and occasionally find really good ones. This application helps by automatically reposting and collecting the reels I like. Whenever I send a reel to the Instagram account associated with this bot, it reposts the reel and adds it to a collection.

## Features
- Automatically reposts Instagram reels sent to the associated account.
- Creates a collection of liked reels.

## Getting Started

### Prerequisites
- Ensure Docker and Docker Compose are installed on your machine.

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/shubRaj/InstaCurator.git
    cd InstaCurator
    ```

2. Fill in the environment variables in the `.env` file:
    ```sh
    PAGE_ID=""
    VERIFY_TOKEN=""
    ACCESS_TOKEN=""
    SECRET_KEY=""
    ```

### Running the Application

1. Build and start the application using Docker Compose:
    ```sh
    docker-compose up --build -d
    ```

2. The bot should now be up and running. To test it, send a reel to your bot's Instagram account.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.