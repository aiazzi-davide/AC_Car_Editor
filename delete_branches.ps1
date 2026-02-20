# Script PowerShell per eliminare tutti i branch locali tranne 'main'
# Esegui questo script nella directory del repository Git

# Controlla se siamo sul branch 'main'
$currentBranch = git branch --show-current
if ($currentBranch -ne 'main') {
    Write-Host "Errore: Non sei sul branch 'main'. Passa a 'main' prima di eseguire lo script."
    exit 1
}

# Ottieni la lista dei branch locali (escludendo 'main')
$branchesToDelete = git branch --format='%(refname:short)' | Where-Object { $_ -ne 'main' }

if ($branchesToDelete.Count -eq 0) {
    Write-Host "Nessun branch da eliminare oltre a 'main'."
    exit 0
}

# Elimina i branch
foreach ($branch in $branchesToDelete) {
    Write-Host "Eliminando branch: $branch"
    git branch -D $branch
}

Write-Host "Operazione completata. Branch rimanenti:"
git branch