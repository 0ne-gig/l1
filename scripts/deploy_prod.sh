source ../.env/Scripts/activate
cd ..
pip freeze > requirements.txt
git add -A
git commit -m "deploy prod"
git push origin master
cd scripts
ssh doi 'cd lab2 && source scripts/build.sh'