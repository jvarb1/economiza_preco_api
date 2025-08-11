@echo off
title Consulta de Precos SEFAZ/AL

:: Entra na pasta onde o script .bat esta localizado, mesmo que seja na rede.
pushd "%~dp0"

echo Executando a consulta de precos...
echo.

python "\\CDBAR_SERVIDOR\Public\Controladoria\economizapreco\consulta.py"

echo.
echo -------------------------------------------------
echo Consulta finalizada!
echo O arquivo 'precos_encontrados.xlsx' foi atualizado.
echo.

:: Libera a pasta.
popd

pause