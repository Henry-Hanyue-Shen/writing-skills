# Compile a paper-narrative .tex file and render the page to PNG so it can be looked at.
#
#   powershell -ExecutionPolicy Bypass -File build.ps1 -Tex path\to\narrative.tex
#
# Output: <name>.pdf next to the .tex file and <name>.png beside it (paths printed at the end).
param(
  [Parameter(Mandatory = $true)][string]$Tex,
  [int]$Dpi = 110
)
$ErrorActionPreference = 'Stop'
$item = Get-Item -LiteralPath $Tex
$base = [IO.Path]::GetFileNameWithoutExtension($item.Name)
Push-Location $item.DirectoryName
try {
  Remove-Item "$base.pdf", "$base.png" -ErrorAction SilentlyContinue
  & pdflatex -interaction=nonstopmode -halt-on-error $item.Name | Out-Null
  $log = Get-Content "$base.log"
  if (-not (Test-Path "$base.pdf")) {
    Write-Output "COMPILE FAILED. First error in $base.log:"
    $i = ($log | Select-String -Pattern '^!' | Select-Object -First 1).LineNumber
    if ($i) { $log[($i - 1)..([Math]::Min($i + 8, $log.Count - 1))] } else { $log | Select-Object -Last 25 }
    exit 1
  }
  $warn = $log | Select-String -Pattern 'Overfull|Missing character|undefined'
  if ($warn) { Write-Output 'Warnings:'; $warn | ForEach-Object { '  ' + $_.Line } }
  $pages = ($log | Select-String -Pattern 'Output written on .*\((\d+) page').Matches.Groups[1].Value
  if ($pages -ne '1') { Write-Output "PAGE COUNT IS $pages - the narrative must fit on one page." }
  & pdftoppm -png -r $Dpi -f 1 -l 1 -singlefile "$base.pdf" $base
  Remove-Item "$base.aux", "$base.log" -ErrorAction SilentlyContinue
  Write-Output ("PDF: " + (Join-Path $item.DirectoryName "$base.pdf"))
  Write-Output ("PNG: " + (Join-Path $item.DirectoryName "$base.png"))
} finally { Pop-Location }
