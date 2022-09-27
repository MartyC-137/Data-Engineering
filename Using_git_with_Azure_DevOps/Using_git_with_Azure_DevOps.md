
## How to use git with Azure DevOps
##### By Martin Palkovic
##### Date: 2022-09-21

<p float = "middle">
    <img align = "top" src = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Visual_Studio_Code_1.35_icon.svg/2048px-Visual_Studio_Code_1.35_icon.svg.png" width="30%" />
    <img align = "top" src = "https://git-scm.com/images/logos/downloads/Git-Icon-1788C.png" width = "30%" />
    <img align = "top" src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Microsoft_Azure.svg/1200px-Microsoft_Azure.svg.png" width = "30%">
</p>

---
## **Introduction**
Azure DevOps is a powerful development tool that allows us to track code changes, automate code deployments and link those code changes to work tasks. Azure DevOps includes Boards, Repos, and Pipelines. The Azure DevOps code repository uses a tool called `Git` in the background. This guide will teach you how to use the repository functionality in a Microsoft application called Visual Studio Code. 
Git is a version control system – you might be familiar with tracked changes in Word. Think of Git like tracked changes, but for code. You may have heard the terms ‘Source Control’ or ‘Version Control’, and I will use these terms in the document – they are all referring to the same thing, tracking code changes using a tool called `Git`.

Note that how to guides for Git extensively recommend using the shell for git - In my experience, that can be very confusing and unapproachable for beginners. I have written this guide in the hopes of making Git approachable for you, and I do encourage you to use the shell once you understand git concepts - you will find it is faster, offers significantly more functionality, and coding stuff is fun! :smiley:

**[Link to my personal Github](https://github.com/MartyC-137)**


### **Before continuing, please install the following:**
- [Visual Studio Code](https://code.visualstudio.com/)

- [Git](https://git-scm.com/)

---

## **Getting Started**

Git functions by having a cloud and a local version of your repository. Think of a repository like any other folder on your computer – a repository contains files and can contain folders. You will work out of your local copy of the repository, and ‘push’ the changes up to the cloud for storage and record keeping. I’ll use Visual Studio Code in this tutorial, but most modern IDE’s have git integration. Azure Data Studio is a good option for pure SQL Server work and has the same native git integration as Visual Studio. This guide is largely applicable for Azure Data Studio as well, many of these steps are exactly the same for that application.
Technically you can store most file types on git, but it only tracks changes for text-based files (.sql, .py, .json, .xml, .yaml, .groovy, .java etc.). Things like powerpoints, word documents, or images are not recommended.

### **Clone the repository to your local machine**

1) Search for `Git Bash` in the search window of your PC and run it as administrator:

![GitBash](images/GitBash.png)

2) Type the following and hit enter: 

```bash
git config --system core.longpaths true
```

![LongPaths](images/GitConfigLongPaths.png)

3)	In Azure DevOps, navigate to the ‘Repos’ tab, and select ‘Clone’:

![ADO_1](images/ADO_1.png)
<!-- <img src=images/ADO_1.png  width="100"> -->

4) Copy the HTTPS link and select ‘Generate Git Credentials’. You may be prompted for these creds in a moment

![ADO_2_CloneLink](images/ADO_2_CloneLink.png)

5) Open Visual Studio Code (Note: your copy of VSCode may initialize with a ‘light’ theme – not to worry, it’s the same thing. I changed my theme)

    a) Select **Clone Git Repository** from the **Get Started** screen:

    ![VSCode_GetStarted](images/VSCode_GetStarted.png)

    b) Paste in the URL copied from step 2 and press enter:

    ![VSCode_CloneLink](images/VSCode_CloneLink.png)

    c) Choose a suitable location on your local machine for the repo. I personally like having a ‘repos’ folder:

    ![RepoFolder](images/RepoFolder.png)

6) You’ve now cloned the repo to your local machine, and Visual Studio Code is connected to it!

![VS_Cloned](images/VS_Cloned.png)

--- 

## **Using Git with VS Code and tracking the changes in Azure DevOps**

### **Branches**

Git has a concept called **branching** which we will use here. In our repo we have a `Main` branch – think of this as your production code. It is a git best practice to create a new branch for any development work (this takes a copy of all our production code at this point in time, so you can work on it freely for testing without affecting our production environment) and **merge** your changes in once your development is complete.

1) Your working branch is displayed in the bottom lefthand corner of the Visual Studio Code window:

![VSC_Branches](images/VSC_Branches.png)

2) Click on the word **Main** in the lower left corner and then **Create new branch**:

![VSCode_NewBranch](images/VSCode_NewBranch.png)

3) Name your branch and press enter:

![VSCode_NameYourBranch](images/VSCode_NameYourBranch.png)


### **Using Git to track your changes** 

1) Create a Folder with your name using the naming convention **FirstName_LastName** in the **Personal** folder of the repository

    - **It is a best practice to avoid spaces in your repo naming conventions. Spaces cause issues when programming from the shell. Use `_` instead**

2) Right click on your personal folder and choose **New File**:

![VSCode_NewFile](images/VSCode_NewFile.png)

3) Create a new file in your directory called `Hello_World.sql`. Note that VS Code will automatically detect the language based on the extension (ex. sql will format the file as a SQL file):

![VSCode_HelloWorldFile](images/VSCode_HelloWorldFile.png)

4) Copy the following code into your `Hello_World.sql` file:

```sql
CREATE TABLE HELLO_WORLD(
   FIRST_NAME VARCHAR 
  , LAST_NAME VARCHAR 
  , INSERT_DATE DATE
);
```

5) Save the file. You will notice an icon appear (‘Open Changes’) in the upper righthand corner, and if you hover over the file in your directory on the left, you’ll notice it is highlighted in green with a ‘U’ next to it. This means that git is recognizing this file is currently ‘untracked’ in our Azure DevOps repo:

    ![VSCode_SavedFile](images/VSCode_SavedFile.png)

    - If you click the ‘Open Changes’ button, it will show you a record of the changes you’ve made since the last version of the file (in this case, that is a blank file):

    ![VSCode_ShowChanges](images/VSCode_ShowChanges.png)

    - Currently, these changes only exist locally. They do not yet exist on Azure DevOps. We need to perform a series of operations to add them to our cloud repository on Azure DevOps.

6) Click the ‘Source Control’ tab on the left. You’ll notice a ‘1’ in blue for our one file that has been changed, as well as the type of change. In this case, the file is untracked.

![VSCode_SourceControl](images/VSCode_SourceControl.png)

7) Click the + sign next to the file to add, or ‘stage’ the change:

![VSCode_git_add](images/VSCode_git_add.png)

8) The file is now **staged** Enter a **commit message** – this is a description of any changes you made to file, to help you or other users understand what has happened with the file. There is no limit on the size of commit messages, and you are encouraged to make them as descriptive as possible. Click  :heavy_check_mark: **Commit** once you are happy with the message:

![VSCode_Commit](images/VSCode_Commit.png)

9) Click ‘Publish Branch’ to push the branch, and the `Hello_World.sql` file to Azure DevOps:

    ![VSCode_PublishBranch](images/VSCode_PublishBranch.png)

    - Note: you may receive an error at this step regarding your username and email not being configured. This is how Azure DevOps will display your commits to the repository. Open a terminal of your choice or the integrated VSCode terminal and run the following commands:

    ```bash
    git config --global user.name "FirstName LastName"
    git config --global user.email "myemail@gmail.com"
    ```

10) If you navigate to the repo, Azure DevOps will notify you of your new branch:

![ADO_NewBranch](images/ADO_NewBranch.png)

11) Click `Hello World` in the red box on step 13, and navigate to the location where you saved `Hello_World.sql`:

![ADO_HelloWorld](images/ADO_HelloWorld.png)

12) The file is now source controlled in Azure DevOps, and we are tracking the changes:

![ADO_SourceControl](images/ADO_SourceControl.png)

13) Switch back to Visual Studio Code, overwrite the code in your `Hello_World.sql` file with the following, and save the file:

```sql
CREATE TABLE HELLO_WORLD(
   FIRST_NAME VARCHAR 
  , LAST_NAME VARCHAR 
  , INSERT_DATE DATE
);

INSERT INTO HELLO_WORLD 
VALUES
('Martin', 'Palkovic', CURRENT_TIMESTAMP()),
('John', 'Doe', CURRENT_TIMESTAMP());
```

14) If you click the ‘Open Changes’ button, you will see the changes we just made. Also notice that the file in our directory on the left is highlighted yellow with an ‘M’ for Modified:

![VSCode_Modified](images/VSCode_Modified.png)

15) Repeat steps **6-9** for these changes – note that on step 12, the green button will now say ‘Sync Changes’ rather than ‘Publish Branch’:

![VSCode_SyncChanges](images/VSCode_SyncChanges.png)

16) In Azure DevOps, the file now contains our changes:

    ![ADO_HelloWorldChanges](images/ADO_HelloWorldChanges.png)

    - The history tab will show all the ‘Commit messages’ you entered to describe your changes:

    ![ADO_Commits](images/ADO_Commits.png)

    - The **Compare** tab will show the changes as we saw them in VS Code, for our current branch. However, on the cloud we can compare any version against each other – this is useful if you’ve done many revisions to a file and need to view the full lineage:

    ![ADO_FullChanges](images/ADO_FullChanges.png)

    * **Note that if you switch over to your `Main` branch at any time, you’ll notice the `Hello_World.sql` file does not exist there – currently, it only exists in our development branch**

---

## Merging Code and creating pull requests

Another foundational concept of git is the **Pull Request** – this is a short write up of the changes you’ve done on your development branch that needs to be approved by a manager or a colleague, and upon completion, the code in your development branch (in our case, the `Hello_World` branch) will be merged into the production code in the `Main` branch.
Pull requests are designed to prevent bad code from entering production, while simultaneously creating a document that can be referenced later to view your development work.

1)	Continuing from step 16 in the previous section, Azure DevOps will prompt you to **Create a pull request** anytime you are working on a branch. Click **Create a pull request**:

    ![ADO_CreatePR](images/ADO_CreatePR.png)

    - You can alternatively select **Pull requests** from the left menu and choose **New pull request**:

    ![ADO_PR_Menu](images/ADO_PR_Menu.png)

2) Fill out the information that you are prompted for and hit create:

![ADO_PR](images/ADO_PR.png)

* In this case, we are merging the development branch (`Hello World`) into the production branch (`Main`). Note that Pull Requests support **Markdown** for easy addition of code blocks, images etc. It is a best practice to keep your Pull Requests as concise as possible - nobody wants to review 50+ files and many commits. 

* **Note that there are ways to clean up your branch prior to merging, specifically using the `git rebase` command - this is a more advanced git topic and is beyond the scope of this document.**

3) View the Pull Request – explore the menu by clicking Files, Updates, Commits, etc. Note that if you have optional or required reviewers, they can leave comments on individual lines of the code, the pull request as a whole, etc. Once you are ready, hit **Complete**

![ADO_CompletePR](images/ADO_CompletePR.png)

4) You will be prompted with a few options – until you get the hang of Git, I recommend the following options. Choose **Complete merge** when ready:

    ![ADO_CompleteMerge](images/ADO_CompleteMerge.png)

    - A **Squash commit** means that every message on your development branch is ‘squashed’ into 1 commit on the main branch. This is helpful if your team members need to view your code because your development branch could have 50 commits with simple messages like **updates**, or **testing another change…** and so forth, which are difficult to sort through. I find one detailed message of the work you did for the branch to be more helpful for the production codebase. Note that this is a topic of active debate among many developers...you may determine you have your own preferences :smiley:

5) Navigate to the Main branch and find your file:

![ADO_MainBranch](images/ADO_MainBranch.png)

---
## Final Notes
If you plan to use SQL Server extensively, you may prefer using [Azure Data Studio](https://learn.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver16). The interface is almost identical to Visual Studio Code, but focused on connecting to Microsoft SQL databases (SQL Server, Azure SQL etc.). I personally use both. I find Azure Data Studio is more reliable for pure SQL Server work and has the same git integration outlined above – this guide will likely work 1:1 for Azure Data Studio.

- Note that you are free to use any IDE you like for development - including SQL Server Management Studio (SSMS). However, SSMS does not have native git integration

- Often times I write code in other applications like the Snowflake UI or SSMS – and copy/paste my code to VS Code when I am ready to save it to DevOps