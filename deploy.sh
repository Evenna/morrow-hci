#!/bin/bash
set -e
read -r TOKEN < /root/.fdl_token || true
export HOME=/root
cd /root/morrow-hci
rm -rf .git
git init -q -b main
printf 'index.html' > .gitignore_tmp; rm -f .gitignore_tmp
git add index.html
git -c user.email=agent@evenna.local -c user.name=agent commit -q -m "Morrow student studio: HCI research agenda"
# create repo if missing
curl -s -o /dev/null -w "create:%{http_code}\n" -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d '{"name":"morrow-hci","private":false,"description":"Morrow 学生工作区 HCI 研究议题规划"}'
git remote remove origin 2>/dev/null || true
git remote add origin "https://x-access-token:$TOKEN@github.com/Evenna/morrow-hci.git"
git push -q -f origin main && echo "push:ok"
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Evenna/morrow-hci/pages \
  -d '{"source":{"branch":"main","path":"/"}}' -w "\npages:%{http_code}\n" | tail -3
