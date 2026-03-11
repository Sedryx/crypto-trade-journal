$ErrorActionPreference = "Stop"

$keys = @(
  "HKLM:\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}",
  "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}",
  "HKCU:\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
)

foreach ($key in $keys) {
  try {
    $item = Get-ItemProperty -Path $key -Name pv
    if ($item.pv) {
      Write-Host "WebView2 installed: $($item.pv)"
      exit 0
    }
  } catch {
  }
}

Write-Host "WebView2 not found. Download:"
Write-Host "https://go.microsoft.com/fwlink/p/?LinkId=2124703"
exit 1
