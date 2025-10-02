Param()

function ExecIfExists($module, $argString) {
    # Prefer uv run <module> if uv is present; forward args as tokens
    $uv = Get-Command uv -ErrorAction SilentlyContinue
    $argArray = @()
    if ($argString -ne '') { $argArray = $argString -split ' ' }
    if ($null -ne $uv) {
        Write-Host "Running via uv: uv run $module $argString"
        & uv run $module $argArray
        if ($LASTEXITCODE -ne 0) { Write-Host "uv run $module failed with exit code $LASTEXITCODE" }
        return
    }

    $exists = Get-Command $module -ErrorAction SilentlyContinue
    if ($null -ne $exists) {
        Write-Host "Running: $module $argString"
        & $module $argArray
        if ($LASTEXITCODE -ne 0) { Write-Host "$module failed with exit code $LASTEXITCODE" }
    } else {
        Write-Host "Skipping: $module not found"
    }
}

Write-Host "make all: lint, test, build, docs"

ExecIfExists 'ruff' 'check src'
ExecIfExists 'pytest' '-q'

# Build using uv if available, otherwise fall back to python -m build
$uv = Get-Command uv -ErrorAction SilentlyContinue
if ($null -ne $uv) {
    Write-Host "Running: uv build"
    & uv build
    if ($LASTEXITCODE -ne 0) { Write-Host "uv build failed with exit code $LASTEXITCODE" }
} else {
    ExecIfExists 'python' '-m build'
}

ExecIfExists 'mkdocs' 'build'

Write-Host "Done"
