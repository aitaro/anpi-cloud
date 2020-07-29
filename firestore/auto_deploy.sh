trap "exit 0" 3 # QUITシグナルで停止
echo "started"
firebase deploy --only firestore --token $FIREBASE_TOKEN --project $FIREBASE_PJNAME

inotifywait -m -e MODIFY /firestore/firestore.* | while read line
  do
    firebase deploy --only firestore --token $FIREBASE_TOKEN --project $FIREBASE_PJNAME
done
