# =================================================================
# Script to Add Multiple Commits with a Specific Historical Date
# =================================================================

# --- Configuration ---
$numberOfCommits = 4
$fileName = "historical_updates.md"
# Set the starting date for your commits
$startDate = [datetime]"2021-08-01T10:00:00"

# --- Script Logic ---
Write-Host "Starting to create $numberOfCommits new commits in August 2021..." -ForegroundColor Yellow

# Loop to create each commit
for ($i=1; $i -le $numberOfCommits; $i++) {
    
    # 1. Calculate the date for the current commit
    $commitDate = $startDate.AddDays($i - 1)
    $iso8601Date = $commitDate.ToString("o") # Format date for Git
    
    # 2. Define a unique change and commit message
    $commitMessage = "refactor: Improve component #$i"
    $logEntry = " Refactor logged on $($commitDate.ToString('yyyy-MM-dd')) for component #$i."
    
    # 3. Make the change by adding a line to a file
    Add-Content -Path $fileName -Value $logEntry
    Write-Host "($i/$numberOfCommits) Appended changes to '$fileName'"

    # 4. Set BOTH the author and committer dates for the commit
    $env:GIT_AUTHOR_DATE = $iso8601Date
    $env:GIT_COMMITTER_DATE = $iso8601Date
    
    # 5. Stage and commit the changes
    git add .
    git commit -m "$commitMessage"
    Write-Host "($i/$numberOfCommits) Created commit for date $($commitDate.ToString('yyyy-MM-dd'))."
    Write-Host "--------------------------------------------------"
}

# Clear the environment variables after the script is done
Remove-Item Env:\GIT_AUTHOR_DATE
Remove-Item Env:\GIT_COMMITTER_DATE

Write-Host "Script finished. Created $numberOfCommits new historical commits."
Write-Host ""
Write-Host "IMPORTANT: You have rewritten history. You must now force push." -ForegroundColor Red
Write-Host "Run the following command to upload your changes:"
Write-Host "git push --force origin main" -ForegroundColor Green