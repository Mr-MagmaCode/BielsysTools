# GitHub Desktop Setup Guide for Visual Studio Code (windows)

This guide will walk you through the process of setting up GitHub Desktop to work with Visual Studio Code. This will allow you to easily manage your Git repositories and perform common Git operations directly in the GitHub Desktop app.

Please note that GitHub Desktop is not officially supported on Linux. But it is possible to use GitHub Desktop on Linux using Wine, but it is not officially supported and may not work properly. There is also a community fork of GitHub Desktop for Linux called "GitHub Desktop for Linux". There is also an official GitHub CLI tool that can be used on Linux, but it does not have the same graphical interface as GitHub Desktop.

## Step 1: Install GitHub Desktop
1. First, you need to install GitHub Desktop on your computer. You can download it from the official website: https://desktop.github.com/download/. This link will take you to the download page for windows, there is also a link for macOS users (but we will not look at that here).

2. Once you have downloaded the installer, run it and follow the on-screen instructions to complete the installation process.

![alt text](Images/GithubDesktop.png)

## Step 2: Configure GitHub Desktop
1. After installing GitHub Desktop, open the application. You will be prompted to sign in to your GitHub account. Click on the "Sign in to GitHub.com" button and enter your GitHub credentials (in web browser) to sign in. If you don't have a GitHub account, you can create one for free by clicking on the "Create an account" link on the sign-in page.

2. After signing in, you will se the configure Git page, here you can choose to set up Git with your name and email address, which will be associated with your commits. You can also choose to set up Git with your GitHub account, which will allow you to easily push and pull changes to and from your GitHub repositories. Follow the prompts to complete the Git configuration.

3. Once you have signed in, you will be taken to the getting started page. Here you can choose to create a new repository, clone an existing repository, or add a local repository. You can also access the options menu by clicking on the "File" menu and selecting "Options". In the options menu, you can configure various settings for GitHub Desktop, including the default code editor.

## Step 3: Ensure Visual Studio Code is set as the default editor in GitHub Desktop
1. To connect GitHub Desktop to Visual Studio Code, you need to set Visual Studio Code as the default code editor in GitHub Desktop. To do this, click on the "File" menu in GitHub Desktop and select "Options".

2. In the Options window, go to the "Integrations" tab. Under the "External Editor" section, click on the dropdown menu and select "Visual Studio Code" (it might already be selected). If Visual Studio Code is not listed, you can click on "Choose..." and navigate to the location of the Visual Studio Code executable on your computer.

3. After selecting Visual Studio Code as the default editor, click "Save" to apply the changes.

## Step 4: Use GitHub Desktop with Visual Studio Code
The gitHub Desktop app will not give Visual Studio Code access to git so it is necessary to set up git in Visual Studio Code separately, you can find a separate guide for setting up git in Visual Studio Code here: [Git Setup Guide](EditorGuides/VisualStudioCode/Git/GitSetup.md)

## Conclusion
Setting up GitHub Desktop to work with Visual Studio Code allows you to easily manage your Git repositories and perform Git operations directly from the GitHub Desktop app. With this setup, you can seamlessly switch between GitHub Desktop and Visual Studio Code, making it easier to manage your code and collaborate with others on your projects.
