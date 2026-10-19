# Publishing to GitHub and deploying Streamlit

## A. Prepare your GitHub repository

1. Create a GitHub account at https://github.com/ if you do not already have one.
2. Click **New repository** and choose a name such as `pathfinder-algorithm-lab`.
3. Select **Public** if you want reviewers to see the code without signing in.
4. Create the empty repository. You do not need to auto-generate a README: this project already has one.
5. Select **Add file → Upload files**.
6. **Extract the downloaded ZIP first.** Upload the **contents** of `PathFinder-Complete`, not the ZIP and not an unnecessary extra enclosing folder. The top level of the GitHub repository must contain `app.py`, `main.py`, `requirements.txt` and `README.md`.
7. If GitHub's browser upload does not preserve hidden directories such as `.github` or `.streamlit`, use the Git CLI method below; keep `.github/workflows/tests.yml` so automated checks run.
8. Commit the uploaded files. Visit the **Actions** tab and check the automated tests.

### Alternative: reliable Git CLI upload (Windows)

Open the project root in VS Code Terminal after installing [Git for Windows](https://git-scm.com/download/win):

```powershell
git init
git add .
git commit -m "Initial PathFinder project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/pathfinder-algorithm-lab.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your own GitHub username. If `git push` requires authentication, follow the GitHub authentication prompt. Do not paste a personal access token into a repository file.

## B. Deploy the interactive app

1. Visit https://share.streamlit.io/ and sign in (usually with GitHub).
2. Choose to create a new app from an existing GitHub repository.
3. Select the repository and branch (`main`).
4. Set the app entry point to **`app.py`**.
5. Deploy. The service installs packages from `requirements.txt` and runs your app.
6. Wait for the hosting service to give you a public URL; check that the app opens and Run all algorithms produces a table.
7. Put the actual URL in the repository's **About → Website** field and in the README (replace no existing link until you have the real URL).

## C. Verify before sharing the project

- [ ] GitHub repository is public and its first page renders the README banner.
- [ ] `app.py` is in the root of the repository.
- [ ] GitHub Actions tests have passed.
- [ ] Online app opens without missing-package errors.
- [ ] Both BFS and Dijkstra/A* behave as documented on the Weighted detour map.
- [ ] You can explain the code, the cost model, and each algorithm in your own words.

Do not publish secrets, passwords, private documents, or real personal data in the repository. Deployment is not automatic merely by uploading the ZIP.
