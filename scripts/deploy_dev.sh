source ../.env/Scripts/activate
cd ..
pip freeze > requirements.txt
git add -A
git commit -m "deploy dev check"
git push origin master
cd scripts
ssh ivg 'ls'
