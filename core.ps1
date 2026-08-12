param(
    [Parameter(ValueFromRemainingArguments = $true)]
    $ArgsList
)

python "$PSScriptRoot\main.py" @ArgsList
