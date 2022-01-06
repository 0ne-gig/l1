source ../.env/Scripts/activate
cd ..
pip freeze > requirements.txt
git add -A
git commit -m "depllloy dev"
git push origin master
cd scripts
ssh doi 'cd lab1 && source scripts/build.sh'