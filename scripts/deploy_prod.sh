source ../env/Scripts/activate
cd ..
pip freeze > requirements.txt
git add -A
git commit -m "deploy dev"
git push origin master
ssh ivg
