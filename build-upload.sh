echo "Limpieza de directorios"
rm -r *.egg-info
rm -r dist

echo "Crear distribución"
python -m build

echo "Verificar el proyecto"
twine check dist/*

echo "Desplegar el proyecto"
echo "Emplear el comando: twine upload"
read