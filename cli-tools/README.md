# Baked Tools
A collection of scripts for interacting with the Shotgrid Python API.

## Instructions (for End Users)
### Things You Need
You need the program itself as a file called `baked-tools.pex`. You should
download this to your `Downloads` folder.

You also need a Shotgrid API key. Someone needs to give this to you if you
don't have it already.

### First Time Setup
If you haven't run the program before, there are a few things you need to do to
get it set up on your computer.

The program needs to be run from a terminal emulator. On MacOS, there is a
terminal emulator installed by default called _Terminal_.

Open the _Terminal_ application. Then enter the following commands, paying
careful attention to the different kinds of quotation marks and replacing
`<your api key here>` with the Shotgrid AIP key.

```
$ mkdir ~/bin
$ cp ~/Downloads/baked-tools.pex ~/bin
$ chmod 755 ~/bin/baked-tools.pex
$ echo 'export PATH=~/bin:$PATH' >> ~/.bashrc
$ echo "export SHOTGRID_API_KEY=$(printf "%q" '<your api key here>')" >> ~/.bashrc
```

Once you've done this, close the terminal window and create a new one. Now you
should be good to go.

### Running the Program
You can upload your media by invoking, for example, the following:

```
$ baked-tools.pex upload "Python API Test Project" *.mp4
```

This will upload all of the `.mp4` files in the current directory to the
project named `Python API Test Project`.

If you just want to upload one or two files, you can do that too:

```
$ baked-tools.pex upload "Python API Test Project" TTD_001_0010.mp4 TTD_001_0020.mp4
```

### Getting More Help
You can get additional help about how to run the program by invoking:

```
$ baked-tools.pex --help
```

## Instructions (for Developers)
Create a virtual environment using a tool like `virtualenv`.

The Python dependencies are managed by `pip-tools`. Install `pip-tools` into
your virtual environment with `pip install pip-tools`.

You can then install the remaining dependencies using `pip-sync
requirements.txt dev-requirements.txt`.

### Building for Release
You build a `.pex` executable by running the `build.sh` script.


# Baked Tools - Sheet Sync Setup Guide

This guide provides instructions for setting up the Google Sheets synchronization functionality for Shotgrid.

## Prerequisites

Before starting, ensure you have:

- Installed and configured the Baked Tools CLI as described above
- A Shotgrid API key properly configured
- Admin access to a Google account

## Setup Steps

### 1. Create a Google Service Account

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API for your project:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click on it and press "Enable"
4. Create a service account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name (e.g., "baked-tools-service")
   - Grant it the necessary permissions (Sheets API access)
   - Click "Done"
5. Create and download a JSON key file:
   - Find your service account in the list
   - Click on the three dots menu (actions) and select "Manage keys"
   - Click "Add Key" > "Create new key"
   - Select JSON as the key type
   - Click "Create" (this will download the key file to your computer)

### 2. Set Up Your Google Sheet

1. Create a new Google Sheet
2. Name it according to the format: `{project_name}_Live_Tracking`
   - For example, if your Shotgrid project is called "SIGNAL", name your sheet "SIGNAL_Live_Tracking"
3. Make sure the sheet contains a tab named "Sheet2" (this is where the data will be placed - this is so you can reference the data with google sheets formulas to make it look pretty etc on the main sheet)
4. Share your Google Sheet with the service account email address:
   - Click the "Share" button in your Google Sheet
   - Enter the service account email (it will look something like: `service-account-name@project-id.iam.gserviceaccount.com`)
   - Set permissions to "Editor"
   - Uncheck "Notify people"
   - Click "Share"

### 3. Place the Service Account JSON File

1. Rename the downloaded service account JSON key file to `service_account.json`
2. Place this file in the same directory where you run the `baked-tools.pex` command
   - Typically, this would be your project's root directory

### 4. Running the Sync Command

Once everything is set up, you can run the sync command using:

```bash
$ baked-tools.pex sync "Your Project Name"
```

This will:
1. Fetch shot data from Shotgrid for the specified project
2. Update the Google Sheet with the following columns:
   - Code
   - Description
   - Status
   - Turnover Notes
   - Delivery Notes
3. Add a timestamp at the bottom of the sheet

## Expected Sheet Structure

After syncing, your Sheet2 tab should contain:

- Header row with column names
- One row per shot with data from Shotgrid
- A timestamp row at the bottom indicating when the sync was performed

## Troubleshooting

If you encounter issues:

- **API Key Error**: Ensure your Shotgrid API key is correctly set up with `export SHOTGRID_API_KEY='your-api-key'`
- **Service Account JSON Error**: Verify the `service_account.json` file is in the correct location where you're running the command
- **Sheet Not Found Error**: Check that your Google Sheet is named exactly `{project_name}_Baked_Live_Tracking` and shared with the service account
- **Sheet2 Tab Error**: Make sure your Google Sheet has a tab named exactly "Sheet2"
- **Permission Error**: Ensure the service account has Editor access to the Google Sheet

## Automating Sync

For regular synchronization, consider setting up a cron job:

```bash
# Example: Run sync daily at 9 AM
0 9 * * * cd /path/to/your/directory && ~/bin/baked-tools.pex sync "Your Project Name" >> /path/to/logfile.log 2>&1
```

Remember to replace "Your Project Name" with your actual Shotgrid project name.
