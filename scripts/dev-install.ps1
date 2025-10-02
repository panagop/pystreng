Param()

function ExecOrReport($cmd, $args) {
    $tool = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($null -eq $tool) {
        Write-Host "Command '$cmd' not found. Please install it or use 'python -m pip install uv'" -ForegroundColor Yellow
        return $false
    }
    Write-Host "Running: $cmd $args"
    & $cmd $args
    return $true
}

Write-Host "Developer install using uv (editable/developer mode)"

# Preferred: use uv to install the project in editable/dev mode
if (-not (ExecOrReport 'uv' 'install -e ".[dev]"')) {
    Write-Host "Falling back: you can run `python -m pip install -e '.[dev]'` manually." -ForegroundColor Cyan
}

Write-Host "Done"
