source ../.env/Scripts/activate
cd ..
pip list
pip freeze > requirements.txt
git add -A
git commit -m "deploy dev check"
git push origin master
# ssh ivg
