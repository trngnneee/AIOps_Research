param([string]$RepositoryRoot = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent))
$ErrorActionPreference = 'Stop'
$repoPath = (Resolve-Path -LiteralPath $RepositoryRoot).Path
$skillsPath = Join-Path $repoPath '.agents/skills'
if (-not (Test-Path -LiteralPath $skillsPath -PathType Container)) {
    throw "Missing canonical skills directory: $skillsPath"
}
$claudePath = Join-Path $repoPath '.claude'
$linkPath = Join-Path $claudePath 'skills'
New-Item -ItemType Directory -Path $claudePath -Force | Out-Null
if (Test-Path -LiteralPath $linkPath) {
    $existing = Get-Item -LiteralPath $linkPath -Force
    if (-not $existing.LinkType) { throw "Refusing to replace a real directory: $linkPath" }
    $targetPath = $existing.Target[0]
    if (-not [IO.Path]::IsPathRooted($targetPath)) { $targetPath = Join-Path $claudePath $targetPath }
    if ((Resolve-Path -LiteralPath $targetPath).Path -ne (Resolve-Path -LiteralPath $skillsPath).Path) {
        throw "Existing link points somewhere else: $targetPath"
    }
    Write-Output "Existing $($existing.LinkType): $linkPath"
    return
}
if (Get-Item -LiteralPath $linkPath -Force -ErrorAction SilentlyContinue) {
    throw "Refusing to replace a broken link: $linkPath"
}
try {
    New-Item -ItemType SymbolicLink -Path $linkPath -Target '../.agents/skills' | Out-Null
    Write-Output 'Created relative symlink. For Git checkout support, use git config --local core.symlinks true.'
} catch {
    if (Get-Item -LiteralPath $linkPath -Force -ErrorAction SilentlyContinue) { throw }
    New-Item -ItemType Junction -Path $linkPath -Target $skillsPath | Out-Null
    Write-Output 'Created local junction; recreate after cloning/moving. Do not stage files through the junction.'
}
