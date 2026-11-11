# Compile one figure file on its own and render it to PNG so it can be looked at.
#
#   powershell -ExecutionPolicy Bypass -File preview.ps1 -Fig path\to\fig_arch.tex
#
# The figure file is the one the paper \input's (a figure or figure* environment with a
# tikzpicture and a caption). The paper itself is not touched: the file is copied into
# <fig folder>\_figpreview and compiled there inside a one-page wrapper.
# Output: _figpreview\preview.pdf and _figpreview\preview.png (path printed at the end).
param(
  [Parameter(Mandatory = $true)][string]$Fig,
  [string]$OutDir,
  # Use the paper's own class line so the text width matches the paper.
  [string]$Class = '\documentclass[conference]{IEEEtran}',
  # Extra preamble lines, e.g. the paper's own macros used inside the figure.
  [string]$Preamble = '',
  [int]$Dpi = 200,
  # Render the whole page instead of only its top part.
  [switch]$FullPage
)
$ErrorActionPreference = 'Stop'
$figItem = Get-Item -LiteralPath $Fig
if (-not $OutDir) { $OutDir = Join-Path $figItem.DirectoryName '_figpreview' }
New-Item -ItemType Directory -Force $OutDir | Out-Null
Copy-Item -LiteralPath $figItem.FullName (Join-Path $OutDir 'fig.tex') -Force

$wrapper = @"
$Class
\usepackage{amsmath,amssymb,graphicx,booktabs}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,fit,calc}
$Preamble
\makeatletter
% Typeset floats in place, full width, so a lone figure lands at the top of page 1.
\renewenvironment{figure*}[1][]{\onecolumn\noindent\begin{minipage}{\textwidth}\def\@captype{figure}}{\end{minipage}}
\renewenvironment{figure}[1][]{\noindent\begin{minipage}{\columnwidth}\def\@captype{figure}}{\end{minipage}}
\makeatother
\pagestyle{empty}
\begin{document}
\input{fig}
\end{document}
"@
Set-Content -LiteralPath (Join-Path $OutDir 'preview.tex') -Value $wrapper -Encoding ascii

Push-Location $OutDir
try {
  Remove-Item preview.pdf, preview.png -ErrorAction SilentlyContinue
  & pdflatex -interaction=nonstopmode -halt-on-error preview.tex | Out-Null
  $log = Get-Content preview.log
  if (-not (Test-Path preview.pdf)) {
    Write-Output 'COMPILE FAILED. First error in preview.log:'
    $i = ($log | Select-String -Pattern '^!' | Select-Object -First 1).LineNumber
    if ($i) { $log[($i - 1)..([Math]::Min($i + 8, $log.Count - 1))] } else { $log | Select-Object -Last 25 }
    exit 1
  }
  # Undefined citations are expected here (no bibliography); everything else is worth reading.
  $warn = $log | Select-String -Pattern 'Overfull|Missing character|Reference .* undefined'
  if ($warn) { Write-Output 'Warnings:'; $warn | ForEach-Object { '  ' + $_.Line } }
  if ($FullPage) {
    & pdftoppm -png -r $Dpi -f 1 -l 1 -singlefile preview.pdf preview
  } else {
    $w = [int](8.5 * $Dpi); $h = [int](4.6 * $Dpi)
    & pdftoppm -png -r $Dpi -f 1 -l 1 -singlefile -x 0 -y 0 -W $w -H $h preview.pdf preview
  }
  Write-Output ("PNG: " + (Join-Path $OutDir 'preview.png'))
} finally { Pop-Location }
