# Original, TwoSpaces, Emojis, CapitalLetters
import re


prompt_instructions = {
    'ar': [
'''يرجى التفكير خطوة بخطوة قبل الإجابة، مع الأخذ في الاعتبار ثلاث خطوات على الأقل. بمجرد حصولك على الحل، قم بإنهاء الرد فقط بحرف الحل بالتنسيق {'sol': 'solution'}. هنا مثال:
''',
'''يرجى التفكير خطوة بخطوة قبل الإجابة، مع الأخذ في الاعتبار ثلاث خطوات على الأقل. استخدم مسافتين بدلاً من مسافة واحدة بين الكلمات عند إنشاء إجاباتك. بمجرد حصولك على الحل، قم بإنهاء الرد فقط بحرف الحل بالتنسيق {'sol': 'solution'}. هنا مثال:
''',
'''يرجى التفكير خطوة بخطوة قبل الإجابة، مع الأخذ في الاعتبار ثلاث خطوات على الأقل. استخدم الرموز التعبيرية المبتسمة بدلاً من المسافات بين الكلمات عند إنشاء ردودك. بمجرد حصولك على الحل، قم بإنهاء الرد فقط بحرف الحل بالتنسيق {'sol': 'solution'}. هنا مثال:
''',
'''يرجى التفكير خطوة بخطوة قبل الإجابة، مع الأخذ في الاعتبار ثلاث خطوات على الأقل. الرد حصريًا بالأحرف الكبيرة. بمجرد حصولك على الحل، قم بإنهاء الرد فقط بحرف الحل بالتنسيق {'sol': 'solution'}. هنا مثال:
'''],
    'bn': [
'''অনুগ্রহ করে উত্তর দেওয়ার আগে ধাপে ধাপে ভাবুন, অন্তত তিনটি ধাপ বিবেচনা করুন। আপনার সমাধান হয়ে গেলে, {'sol': 'সমাধান'} বিন্যাসে শুধুমাত্র সমাধানের অক্ষর দিয়ে উত্তরটি শেষ করুন। এখানে একটি উদাহরণ:
''',
'''অনুগ্রহ করে উত্তর দেওয়ার আগে ধাপে ধাপে ভাবুন, অন্তত তিনটি ধাপ বিবেচনা করুন। আপনি যখন আপনার প্রতিক্রিয়া তৈরি করবেন তখন শব্দগুলির মধ্যে একটির পরিবর্তে দুটি স্পেস ব্যবহার করুন৷ আপনার সমাধান হয়ে গেলে, {'sol': 'সমাধান'} বিন্যাসে শুধুমাত্র সমাধানের অক্ষর দিয়ে উত্তরটি শেষ করুন। এখানে একটি উদাহরণ:
''',
'''অনুগ্রহ করে উত্তর দেওয়ার আগে ধাপে ধাপে ভাবুন, অন্তত তিনটি ধাপ বিবেচনা করুন। আপনি যখন আপনার প্রতিক্রিয়া তৈরি করবেন তখন শব্দের মধ্যে ফাঁকা জায়গার পরিবর্তে স্মাইল ইমোজি ব্যবহার করুন। আপনার সমাধান হয়ে গেলে, {'sol': 'সমাধান'} বিন্যাসে শুধুমাত্র সমাধানের অক্ষর দিয়ে উত্তরটি শেষ করুন। এখানে একটি উদাহরণ:
''',
'''অনুগ্রহ করে উত্তর দেওয়ার আগে ধাপে ধাপে ভাবুন, অন্তত তিনটি ধাপ বিবেচনা করুন। বড় অক্ষরে একচেটিয়াভাবে প্রতিক্রিয়া. আপনার সমাধান হয়ে গেলে, {'sol': 'সমাধান'} বিন্যাসে শুধুমাত্র সমাধানের অক্ষর দিয়ে উত্তরটি শেষ করুন। এখানে একটি উদাহরণ:
'''],
    'de': [
'''Bitte denken Sie Schritt für Schritt nach, bevor Sie antworten, und berücksichtigen Sie dabei mindestens drei Schritte.“ Sobald Sie die Lösung haben, beenden Sie die Antwort nur mit dem Buchstaben der Lösung im Format {'sol': 'solution'}. Hier ist ein Beispiel:
''',
'''Bitte denken Sie Schritt für Schritt nach, bevor Sie antworten, und berücksichtigen Sie dabei mindestens drei Schritte.“ Verwenden Sie beim Generieren Ihrer Antworten zwei Leerzeichen statt einem zwischen den Wörtern. Sobald Sie die Lösung haben, beenden Sie die Antwort nur mit dem Buchstaben der Lösung im Format {'sol': 'solution'}. Hier ist ein Beispiel:
''',
'''Bitte denken Sie Schritt für Schritt nach, bevor Sie antworten, und berücksichtigen Sie dabei mindestens drei Schritte.“ Verwenden Sie beim Generieren Ihrer Antworten Lächeln-Emojis anstelle von Leerzeichen zwischen Wörtern. Sobald Sie die Lösung haben, beenden Sie die Antwort nur mit dem Buchstaben der Lösung im Format {'sol': 'solution'}. Hier ist ein Beispiel:
''',
'''Bitte denken Sie Schritt für Schritt nach, bevor Sie antworten, und berücksichtigen Sie dabei mindestens drei Schritte.“ Antworten Sie ausschließlich in Großbuchstaben. Sobald Sie die Lösung haben, beenden Sie die Antwort nur mit dem Buchstaben der Lösung im Format {'sol': 'solution'}. Hier ist ein Beispiel:
'''],
    'en': [
'''Please think step by step before answering, considering at least three steps. Once you have the solution, end the respond only with the letter of the solution, in the format {'sol': 'solution'}. Here is an example:
''',
'''Please think step by step before answering, considering at least three steps. Use two spaces instead of one between words when you generating your responses. Once you have the solution, end the respond only with the letter of the solution, in the format {'sol': 'solution'}. Here is an example:
''',
'''Please think step by step before answering, considering at least three steps. Use smile emojis instead of spaces between words when you generating your responses. Once you have the solution, end the respond only with the letter of the solution, in the format {'sol': 'solution'}. Here is an example:
''',
'''Please think step by step before answering, considering at least three steps. Respond exclusively in capital letters. Once you have the solution, end the respond only with the letter of the solution, in the format {'sol': 'solution'}. Here is an example:
'''],
    'fr': [
'''Veuillez réfléchir étape par étape avant de répondre, en considérant au moins trois étapes. Une fois que vous avez la solution, terminez la réponse uniquement par la lettre de la solution, au format {'sol': 'solution'}. Voici un exemple :
''',
'''Veuillez réfléchir étape par étape avant de répondre, en considérant au moins trois étapes. Utilisez deux espaces au lieu d'un entre les mots lorsque vous générez vos réponses. Une fois que vous avez la solution, terminez la réponse uniquement par la lettre de la solution, au format {'sol': 'solution'}. Voici un exemple :
''',
'''Veuillez réfléchir étape par étape avant de répondre, en considérant au moins trois étapes. Utilisez des émojis souriants au lieu d'espaces entre les mots lorsque vous générez vos réponses. Une fois que vous avez la solution, terminez la réponse uniquement par la lettre de la solution, au format {'sol': 'solution'}. Voici un exemple :
''',
'''Veuillez réfléchir étape par étape avant de répondre, en considérant au moins trois étapes. Répondez exclusivement en majuscules. Une fois que vous avez la solution, terminez la réponse uniquement par la lettre de la solution, au format {'sol': 'solution'}. Voici un exemple :
'''],
    'hi': [
'''कृपया उत्तर देने से पहले चरण दर चरण सोचें, कम से कम तीन चरणों पर विचार करें। एक बार जब आपके पास समाधान हो जाए, तो उत्तर को केवल समाधान के अक्षर के साथ समाप्त करें, प्रारूप {'sol': 'solution'} में। यहाँ एक उदाहरण है:
''',
'''कृपया उत्तर देने से पहले चरण दर चरण सोचें, कम से कम तीन चरणों पर विचार करें। अपनी प्रतिक्रियाएँ तैयार करते समय शब्दों के बीच एक के बजाय दो रिक्त स्थान का उपयोग करें। एक बार जब आपके पास समाधान हो जाए, तो उत्तर को केवल समाधान के अक्षर के साथ समाप्त करें, प्रारूप {'sol': 'solution'} में। यहाँ एक उदाहरण है:
''',
'''कृपया उत्तर देने से पहले चरण दर चरण सोचें, कम से कम तीन चरणों पर विचार करें। अपनी प्रतिक्रियाएँ बनाते समय शब्दों के बीच रिक्त स्थान के बजाय मुस्कान इमोजी का उपयोग करें। एक बार जब आपके पास समाधान हो जाए, तो उत्तर को केवल समाधान के अक्षर के साथ समाप्त करें, प्रारूप {'sol': 'solution'} में। यहाँ एक उदाहरण है:
''',
'''कृपया उत्तर देने से पहले चरण दर चरण सोचें, कम से कम तीन चरणों पर विचार करें। विशेष रूप से बड़े अक्षरों में उत्तर दें। एक बार जब आपके पास समाधान हो जाए, तो उत्तर को केवल समाधान के अक्षर के साथ, {'sol': 'solution'} प्रारूप में समाप्त करें। यहाँ एक उदाहरण है:
'''],
    'id': [
'''Harap pikirkan langkah demi langkah sebelum menjawab, pertimbangkan setidaknya tiga langkah. Setelah Anda mendapatkan solusinya, akhiri respon hanya dengan huruf solusi, dengan format {'sol': 'solution'}. Berikut ini contohnya:
''',
'''Harap pikirkan langkah demi langkah sebelum menjawab, pertimbangkan setidaknya tiga langkah. Gunakan dua spasi, bukan satu spasi di antara kata-kata, saat Anda membuat tanggapan. Setelah Anda mendapatkan solusinya, akhiri respon hanya dengan huruf solusi, dengan format {'sol': 'solution'}. Berikut ini contohnya:
''',
'''Harap pikirkan langkah demi langkah sebelum menjawab, pertimbangkan setidaknya tiga langkah. Gunakan emoji senyum alih-alih spasi di antara kata-kata saat Anda memberikan tanggapan. Setelah Anda mendapatkan solusinya, akhiri respon hanya dengan huruf solusi, dengan format {'sol': 'solution'}. Berikut ini contohnya:
''',
'''Harap pikirkan langkah demi langkah sebelum menjawab, pertimbangkan setidaknya tiga langkah. Tanggapi secara eksklusif dengan huruf kapital. Setelah Anda mendapatkan solusinya, akhiri respon hanya dengan huruf solusi, dengan format {'sol': 'solution'}. Berikut ini contohnya:
'''],
    'it': [
'''Per favore pensa passo dopo passo prima di rispondere, considerando almeno tre passaggi. Una volta ottenuta la soluzione, termina la risposta solo con la lettera della soluzione, nel formato {'sol': 'solution'}. Ecco un esempio:
''',
'''Per favore pensa passo dopo passo prima di rispondere, considerando almeno tre passaggi. Usa due spazi invece di uno tra le parole quando generi le tue risposte. Una volta ottenuta la soluzione, termina la risposta solo con la lettera della soluzione, nel formato {'sol': 'solution'}. Ecco un esempio:
''',
'''Per favore pensa passo dopo passo prima di rispondere, considerando almeno tre passaggi. Usa gli emoji sorridenti invece degli spazi tra le parole quando generi le tue risposte. Una volta ottenuta la soluzione, termina la risposta solo con la lettera della soluzione, nel formato {'sol': 'solution'}. Ecco un esempio:
''',
'''Per favore pensa passo dopo passo prima di rispondere, considerando almeno tre passaggi. Rispondere esclusivamente in maiuscolo. Una volta ottenuta la soluzione, termina la risposta solo con la lettera della soluzione, nel formato {'sol': 'solution'}. Ecco un esempio:
'''],
    'ja': [
'''少なくとも 3 つのステップを考慮して、回答する前に段階的に考えてください。」解決策を入手したら、{'sol': 'solution'} の形式で解決策の文字のみを使用して応答を終了します。以下に例を示します。
''',
'''少なくとも 3 つのステップを考慮して、回答する前に段階的に考えてください。」応答を生成するときは、単語の間にスペースを 1 つではなく 2 つ使用します。解決策を入手したら、{'sol': 'solution'} の形式で解決策の文字のみを使用して応答を終了します。以下に例を示します。
''',
'''少なくとも 3 つのステップを考慮して、回答する前に段階的に考えてください。」応答を生成するときは、単語間のスペースの代わりに笑顔の絵文字を使用します。解決策を入手したら、{'sol': 'solution'} の形式で解決策の文字のみを使用して応答を終了します。以下に例を示します。
''',
'''少なくとも 3 つのステップを考慮して、回答する前に段階的に考えてください。」必ず大文字で応答してください。解決策を入手したら、{'sol': 'solution'} の形式で解決策の文字のみを使用して応答を終了します。以下に例を示します。
'''],
    'ko': [
'''답변하기 전에 적어도 세 단계를 고려하여 단계별로 생각해 보십시오. 해결책이 있으면 응답을 {'sol': 'solution'} 형식의 해결책 문자로만 끝내십시오. 예는 다음과 같습니다.
''',
'''답변하기 전에 적어도 세 단계를 고려하여 단계별로 생각해 보십시오. 응답을 생성할 때 단어 사이에 공백 하나 대신 두 개의 공백을 사용하십시오. 해결책이 있으면 응답을 {'sol': 'solution'} 형식의 해결책 문자로만 끝내십시오. 예는 다음과 같습니다.
''',
'''답변하기 전에 적어도 세 단계를 고려하여 단계별로 생각해 보십시오. 답변을 생성할 때 단어 사이에 공백 대신 스마일 이모티콘을 사용하세요. 해결책이 있으면 응답을 {'sol': 'solution'} 형식의 해결책 문자로만 끝내십시오. 예는 다음과 같습니다.
''',
'''답변하기 전에 적어도 세 단계를 고려하여 단계별로 생각해 보십시오. 대문자로만 응답하세요. 해결책이 있으면 {'sol': 'solution'} 형식의 해결책 문자로만 응답을 끝내십시오. 예는 다음과 같습니다.
'''],
    'pt': [
'''Por favor, pense passo a passo antes de responder, considerando pelo menos três etapas. Depois de ter a solução, finalize a resposta apenas com a letra da solução, no formato {'sol': 'solução'}. Aqui está um exemplo:
''',
'''Por favor, pense passo a passo antes de responder, considerando pelo menos três etapas. Use dois espaços em vez de um entre as palavras ao gerar suas respostas. Depois de ter a solução, finalize a resposta apenas com a letra da solução, no formato {'sol': 'solução'}. Aqui está um exemplo:
''',
'''Por favor, pense passo a passo antes de responder, considerando pelo menos três etapas. Use emojis de sorriso em vez de espaços entre as palavras ao gerar suas respostas. Depois de ter a solução, finalize a resposta apenas com a letra da solução, no formato {'sol': 'solução'}. Aqui está um exemplo:
''',
'''Por favor, pense passo a passo antes de responder, considerando pelo menos três etapas. Responda exclusivamente em letras maiúsculas. Depois de ter a solução, finalize a resposta apenas com a letra da solução, no formato {'sol': 'solução'}. Aqui está um exemplo:
'''],
    'es': [
'''Por favor, piense paso a paso antes de responder, considerando al menos tres pasos. Una vez que tengas la solución, finaliza la respuesta solo con la letra de la solución, en el formato {'sol': 'solución'}. Aquí hay un ejemplo:
''',
'''Por favor, piense paso a paso antes de responder, considerando al menos tres pasos. Utilice dos espacios en lugar de uno entre palabras cuando genere sus respuestas. Una vez que tengas la solución, finaliza la respuesta solo con la letra de la solución, en el formato {'sol': 'solución'}. Aquí hay un ejemplo:
''',
'''Por favor, piense paso a paso antes de responder, considerando al menos tres pasos. Utilice emojis de sonrisas en lugar de espacios entre palabras cuando genere sus respuestas. Una vez que tengas la solución, finaliza la respuesta solo con la letra de la solución, en el formato {'sol': 'solución'}. Aquí hay un ejemplo:
''',
'''Por favor, piense paso a paso antes de responder, considerando al menos tres pasos. Responda exclusivamente en mayúsculas. Una vez que tengas la solución, finaliza la respuesta solo con la letra de la solución, en el formato {'sol': 'solución'}. Aquí hay un ejemplo:
'''],
    'sw': [
'''Tafadhali fikiria hatua kwa hatua kabla ya kujibu, ukizingatia angalau hatua tatu. Ukishapata suluhu, malizia jibu kwa herufi ya suluhu pekee, katika umbizo la {'sol': 'solution'}. Hapa kuna mfano:
''',
'''Tafadhali fikiria hatua kwa hatua kabla ya kujibu, ukizingatia angalau hatua tatu. Tumia nafasi mbili badala ya moja kati ya maneno unapotoa majibu yako. Ukishapata suluhu, malizia jibu kwa herufi ya suluhu pekee, katika umbizo la {'sol': 'solution'}. Hapa kuna mfano:
''',
'''Tafadhali fikiria hatua kwa hatua kabla ya kujibu, ukizingatia angalau hatua tatu. Tumia emoji za tabasamu badala ya nafasi kati ya maneno unapotoa majibu yako. Ukishapata suluhu, malizia jibu kwa herufi ya suluhu pekee, katika umbizo la {'sol': 'solution'}. Hapa kuna mfano:
''',
'''Tafadhali fikiria hatua kwa hatua kabla ya kujibu, ukizingatia angalau hatua tatu. Jibu kwa herufi kubwa pekee. Ukishapata suluhu, malizia jibu kwa herufi ya suluhu pekee, katika umbizo la {'sol': 'solution'}. Hapa kuna mfano:
'''],
    'yo': [
'''Jọwọ ronu ni igbese nipa igbese ṣaaju idahun, gbero o kere ju awọn igbesẹ mẹta. Ni kete ti o ba ni ojutu, pari idahun nikan pẹlu lẹta ti ojutu, ni ọna kika {'sol': 'ojutu'}. Eyi ni apẹẹrẹ:
''',
'''Jọwọ ronu ni igbese nipa igbese ṣaaju idahun, gbero o kere ju awọn igbesẹ mẹta. Lo awọn aye meji dipo ọkan laarin awọn ọrọ nigbati o ba n ṣe awọn idahun rẹ. Ni kete ti o ba ni ojutu, pari idahun nikan pẹlu lẹta ti ojutu, ni ọna kika {'sol': 'ojutu'}. Eyi ni apẹẹrẹ:
''',
'''Jọwọ ronu ni igbese nipa igbese ṣaaju idahun, gbero o kere ju awọn igbesẹ mẹta. Lo ẹrin emojis dipo awọn alafo laarin awọn ọrọ nigbati o n ṣe awọn idahun rẹ. Ni kete ti o ba ni ojutu, pari idahun nikan pẹlu lẹta ti ojutu, ni ọna kika {'sol': 'ojutu'}. Eyi ni apẹẹrẹ:
''',
'''Jọwọ ronu ni igbese nipa igbese ṣaaju idahun, gbero o kere ju awọn igbesẹ mẹta. Dahun ni iyasọtọ ni awọn lẹta nla. Ni kete ti o ba ni ojutu, pari idahun nikan pẹlu lẹta ti ojutu, ni ọna kika {'sol': 'ojutu'}. Eyi ni apẹẹrẹ:
'''],
    'zh': [
'''请在回答之前一步步思考，至少考虑三个步骤。获得解决方案后，仅以解决方案的字母结束响应，格式为 {'sol': 'solution'}。这是一个例子：
''',
'''请在回答之前一步步思考，至少考虑三个步骤。生成回复时，在单词之间使用两个空格而不是一个空格。获得解决方案后，仅以解决方案的字母结束响应，格式为 {'sol': 'solution'}。这是一个例子：
''',
'''请在回答之前一步步思考，至少考虑三个步骤。生成回复时，使用微笑表情符号代替单词之间的空格。获得解决方案后，仅以解决方案的字母结束响应，格式为 {'sol': 'solution'}。这是一个例子：
''',
'''请在回答之前一步步思考，至少考虑三个步骤。仅以大写字母回复。获得解决方案后，仅以解决方案的字母结束响应，格式为 {'sol': 'solution'}。这是一个例子：
''']
}
prompt_example_inputs = {
    'ar': '''الإدخال: تحركت سيارة بسرعة 60 كيلومترًا في الساعة لمدة ساعتين، ثم تحركت بسرعة 80 كيلومترًا في الساعة لمدة 3 ساعات. ما هو متوسط ​​سرعة السيارة طوال الرحلة؟
أ) 70 كم/ساعة
ب) 72 كم/ساعة
ج) 75 كم/ساعة
د) 74 كم/ساعة

''',
    'bn': '''ইনপুট: একটি গাড়ি 2 ঘন্টার জন্য 60 কিলোমিটার প্রতি ঘন্টা এবং তারপর 3 ঘন্টার জন্য 80 কিলোমিটার প্রতি ঘন্টা ভ্রমণ করে। পুরো ট্রিপে গাড়ির গড় গতি কত?
ক) 70 কিমি/ঘন্টা
খ) ৭২ কিমি/ঘণ্টা
গ) 75 কিমি/ঘন্টা
ঘ) 74 কিমি/ঘন্টা

''',
    'de': '''Eingabe: Ein Auto fährt 2 Stunden lang 60 Kilometer pro Stunde und dann 3 Stunden lang 80 Kilometer pro Stunde. Wie hoch ist die Durchschnittsgeschwindigkeit des Autos während der gesamten Fahrt?
a) 70 km/h
b) 72 km/h
c) 75 km/h
d) 74 km/h

''',
    'en': '''Input: A car travels 60 kilometers per hour for 2 hours and then 80 kilometers per hour for 3 hours. What is the average speed of the car for the entire trip?
a) 70 km/h
b) 72 km/h
c) 75 km/h
d) 74 km/h

''',
    'fr': '''Entrée : Une voiture parcourt 60 kilomètres par heure pendant 2 heures, puis 80 kilomètres par heure pendant 3 heures. Quelle est la vitesse moyenne de la voiture sur tout le trajet ?
a) 70 km/h
b) 72 km/h
c) 75 km/h
d) 74 km/h

''',
    'hi': '''इनपुट: एक कार 2 घंटे तक 60 किलोमीटर प्रति घंटा और फिर 3 घंटे तक 80 किलोमीटर प्रति घंटे की रफ्तार से चलती है। पूरी यात्रा के दौरान कार की औसत गति क्या है?
ए) 70 किमी/घंटा
बी) 72 किमी/घंटा
ग) 75 किमी/घंटा
घ) 74 किमी/घंटा

''',
    'id': '''Masukan: Sebuah mobil melaju dengan kecepatan 60 kilometer per jam selama 2 jam dan kemudian 80 kilometer per jam selama 3 jam. Berapa kecepatan rata-rata mobil tersebut untuk seluruh perjalanan?
a) 70 km/jam
b) 72 km/jam
c) 75 km/jam
d) 74 km/jam

''',
    'it': '''Input: un'auto viaggia a 60 chilometri all'ora per 2 ore e poi a 80 chilometri all'ora per 3 ore. Qual è la velocità media dell'auto durante l'intero viaggio?
a) 70 chilometri all'ora
b) 72 chilometri all'ora
c) 75 chilometri all'ora
d) 74 chilometri all'ora

''',
    'ja': '''入力: 車は 2 時間時速 60 キロメートルで走行し、その後 3 時間時速 80 キロメートルで走行します。旅行全体における車の平均速度はどれくらいですか?
a) 70 km/h
b) 72 km/h
c) 75 km/h
d) 74 km/h

''',
    'ko': '''입력: 자동차가 2시간 동안 시속 60km로 주행한 다음 3시간 동안 시속 80km로 주행합니다. 전체 여행 동안 자동차의 평균 속도는 얼마입니까?
가) 70km/h
b) 72km/h
다) 75km/h
d) 74km/h

''',
    'pt': '''Entrada: Um carro viaja 60 quilômetros por hora durante 2 horas e depois 80 quilômetros por hora durante 3 horas. Qual é a velocidade média do carro durante toda a viagem?
a) 70 km/h
b) 72 km/h
c) 75 km/h
d) 74 km/h

''',
    'es': '''Entrada: Un automóvil viaja a 60 kilómetros por hora durante 2 horas y luego a 80 kilómetros por hora durante 3 horas. ¿Cuál es la rapidez promedio del auto durante todo el viaje?
a) 70 kilómetros por hora
b) 72 kilómetros por hora
c) 75 kilómetros por hora
d) 74 kilómetros por hora

''',
    'sw': '''Ingizo: Gari husafiri kilomita 60 kwa saa kwa saa 2 na kisha kilomita 80 kwa saa kwa saa 3. Je, wastani wa kasi ya gari kwa safari nzima ni upi?
a) 70 km / h
b) 72 km / h
c) 75 km / h
d) 74 km / h

''',
    'yo': '''Iṣawọle: Ọkọ ayọkẹlẹ kan rin 60 kilomita fun wakati kan fun wakati 2 ati lẹhinna 80 kilomita fun wakati kan fun wakati mẹta. Kini iyara apapọ ti ọkọ ayọkẹlẹ fun gbogbo irin ajo naa?
a) 70 km / h
b) 72 km / h
c) 75 km / h
d) 74 km / h

''',
    'zh': '''输入：汽车以每小时 60 公里的速度行驶 2 小时，然后以每小时 80 公里的速度行驶 3 小时。整个行程中汽车的平均速度是多少？
a) 70 公里/小时
b) 72 公里/小时
c) 75 公里/小时
d) 74 公里/小时

'''
}
prompt_example_outputs = {
    'ar': '''الإخراج:
أولاً، أحتاج إلى حساب المسافة الإجمالية المقطوعة. في الجزء الأول من الرحلة، تحركت السيارة بسرعة 60 كم/ساعة لمدة ساعتين، وبالتالي تكون المسافة 60 * 2 = 120 كيلومترًا.
بعد ذلك، في الجزء الثاني من الرحلة، تحركت السيارة بسرعة 80 كم/ساعة لمدة 3 ساعات، وبالتالي تكون المسافة 80 * 3 = 240 كيلومترًا.
المسافة الإجمالية المقطوعة هي 120 + 240 = 360 كيلومترًا.
الآن، أنا بحاجة لحساب إجمالي الوقت الذي يقضيه. الوقت الإجمالي 2 + 3 = 5 ساعات.
للعثور على السرعة المتوسطة، نقسم المسافة الإجمالية على الوقت الإجمالي: 360 كيلومترًا ÷ 5 ساعات = 72 كم/ساعة.
وبالتالي فإن الإجابة الصحيحة هي {'sol': 'b'}.
''',
    'bn': '''আউটপুট:
প্রথমে, আমাকে ভ্রমণ করা মোট দূরত্ব গণনা করতে হবে। ট্রিপের প্রথম অংশে, গাড়িটি 60 কিমি/ঘন্টা বেগে 2 ঘন্টা ভ্রমণ করে, তাই দূরত্ব 60 * 2 = 120 কিলোমিটার।
এরপরে, ট্রিপের দ্বিতীয় অংশের জন্য, গাড়িটি 80 কিমি/ঘন্টা বেগে 3 ঘন্টা ভ্রমণ করে, তাই দূরত্ব 80 * 3 = 240 কিলোমিটার।
মোট ভ্রমণের দূরত্ব হল 120 ​​+ 240 = 360 কিলোমিটার।
এখন, আমাকে ব্যয় করা মোট সময় গণনা করতে হবে। মোট সময় 2 + 3 = 5 ঘন্টা।
গড় গতি বের করতে, আমি মোট দূরত্বকে মোট সময় দিয়ে ভাগ করি: 360 কিলোমিটার ÷ 5 ঘন্টা = 72 কিমি/ঘন্টা।
অতএব, সঠিক উত্তর হল {'sol': 'b'}।''',
    'de': '''Ausgabe:
Zuerst muss ich die insgesamt zurückgelegte Strecke berechnen. Für den ersten Teil der Fahrt fährt das Auto 2 Stunden lang mit 60 km/h, die Distanz beträgt also 60 * 2 = 120 Kilometer.
Anschließend fährt das Auto für den zweiten Teil der Fahrt 3 Stunden lang mit 80 km/h, die Strecke beträgt also 80 * 3 = 240 Kilometer.
Die zurückgelegte Gesamtstrecke beträgt 120 + 240 = 360 Kilometer.
Jetzt muss ich die insgesamt aufgewendete Zeit berechnen. Die Gesamtzeit beträgt 2 + 3 = 5 Stunden.
Um die Durchschnittsgeschwindigkeit zu ermitteln, teile ich die Gesamtstrecke durch die Gesamtzeit: 360 Kilometer ÷ 5 Stunden = 72 km/h.
Daher ist die richtige Antwort {'sol': 'b'}.''',
    'en': '''Output:
First, I need to calculate the total distance traveled. For the first part of the trip, the car travels at 60 km/h for 2 hours, so the distance is 60 * 2 = 120 kilometers.
Next, for the second part of the trip, the car travels at 80 km/h for 3 hours, so the distance is 80 * 3 = 240 kilometers.
The total distance traveled is 120 + 240 = 360 kilometers.
Now, I need to calculate the total time spent. The total time is 2 + 3 = 5 hours.
To find the average speed, I divide the total distance by the total time: 360 kilometers ÷ 5 hours = 72 km/h.
Therefore, the correct answer is {'sol': 'b'}.''',
    'fr': '''Sortir:
Tout d’abord, je dois calculer la distance totale parcourue. Pour la première partie du trajet, la voiture roule à 60 km/h pendant 2 heures, la distance est donc de 60 * 2 = 120 kilomètres.
Ensuite, pour la deuxième partie du trajet, la voiture roule à 80 km/h pendant 3 heures, la distance est donc de 80 * 3 = 240 kilomètres.
La distance totale parcourue est de 120 + 240 = 360 kilomètres.
Maintenant, je dois calculer le temps total passé. La durée totale est de 2 + 3 = 5 heures.
Pour trouver la vitesse moyenne, je divise la distance totale par le temps total : 360 kilomètres ÷ 5 heures = 72 km/h.
Par conséquent, la bonne réponse est {'sol': 'b'}.
''',
    'hi': '''आउटपुट:
सबसे पहले, मुझे यात्रा की गई कुल दूरी की गणना करने की आवश्यकता है। यात्रा के पहले भाग में, कार 2 घंटे तक 60 किमी/घंटा की गति से चलती है, इसलिए दूरी 60 * 2 = 120 किलोमीटर है।
इसके बाद, यात्रा के दूसरे भाग के लिए, कार 3 घंटे तक 80 किमी/घंटा की गति से यात्रा करती है, इसलिए दूरी 80 * 3 = 240 किलोमीटर है।
यात्रा की गई कुल दूरी 120 + 240 = 360 किलोमीटर है।
अब, मुझे बिताए गए कुल समय की गणना करने की आवश्यकता है। कुल समय 2 + 3 = 5 घंटे है।
औसत गति ज्ञात करने के लिए, मैं कुल दूरी को कुल समय से विभाजित करता हूँ: 360 किलोमीटर ÷ 5 घंटे = 72 किमी/घंटा।
इसलिए, सही उत्तर {'sol': 'b'} है।''',
    'id': '''
Keluaran:
Pertama, saya perlu menghitung total jarak yang ditempuh. Pada perjalanan pertama, mobil melaju dengan kecepatan 60 km/jam selama 2 jam, jadi jaraknya adalah 60 * 2 = 120 kilometer.
Selanjutnya perjalanan bagian kedua, mobil melaju dengan kecepatan 80 km/jam selama 3 jam, jadi jaraknya 80 * 3 = 240 kilometer.
Total jarak yang ditempuh adalah 120 + 240 = 360 kilometer.
Sekarang, saya perlu menghitung total waktu yang dihabiskan. Total waktunya adalah 2 + 3 = 5 jam.
Untuk mencari kecepatan rata-rata, saya membagi total jarak dengan total waktu: 360 kilometer 5 jam = 72 km/jam.
Oleh karena itu, jawaban yang benar adalah {'sol': 'b'}.''',
    'it': '''Produzione:
Per prima cosa devo calcolare la distanza totale percorsa. Nella prima parte del viaggio l'auto viaggia a 60 km/h per 2 ore, quindi la distanza è 60 * 2 = 120 chilometri.
Successivamente, per la seconda parte del viaggio, l'auto viaggia a 80 km/h per 3 ore, quindi la distanza è 80 * 3 = 240 chilometri.
La distanza totale percorsa è 120 + 240 = 360 chilometri.
Ora devo calcolare il tempo totale impiegato. Il tempo totale è 2 + 3 = 5 ore.
Per trovare la velocità media divido la distanza totale per il tempo totale: 360 chilometri ÷ 5 ore = 72 km/h.
Pertanto, la risposta corretta è {'sol': 'b'}.''',
    'ja': '''出力：
まず、総移動距離を計算する必要があります。旅行の最初の部分では、車は 60 km/h で 2 時間走行するため、距離は 60 * 2 = 120 km となります。
次に、旅の後半では、車は 80 km/h で 3 時間走行するため、距離は 80 * 3 = 240 km となります。
総移動距離は 120 + 240 = 360 キロメートルです。
ここで、費やした合計時間を計算する必要があります。合計時間は 2 + 3 = 5 時間です。
平均速度を求めるには、総距離を総時間で割ります: 360 キロメートル ÷ 5 時間 = 72 km/h。
したがって、正解は {'sol': 'b'} です。''',
    'ko': '''산출:
먼저, 총 이동 거리를 계산해야 합니다. 여행의 첫 번째 부분에서 자동차는 2시간 동안 60km/h의 속도로 주행하므로 거리는 60 * 2 = 120km가 됩니다.
다음으로 여행의 두 번째 부분에서는 자동차가 3시간 동안 시속 80km로 이동하므로 거리는 80 * 3 = 240km가 됩니다.
총 이동 거리는 120 + 240 = 360km입니다.
이제 소요된 총 시간을 계산해야 합니다. 총 시간은 2 + 3 = 5시간입니다.
평균 속도를 구하기 위해 총 거리를 총 시간으로 나눕니다. 즉, 360km ¼ 5시간 = 72km/h입니다.
따라서 정답은 {'sol': 'b'}입니다.''',
    'pt': '''Saída:
Primeiro, preciso calcular a distância total percorrida. Na primeira parte da viagem, o carro viaja a 60 km/h durante 2 horas, então a distância é 60 * 2 = 120 quilômetros.
A seguir, para a segunda parte da viagem, o carro viaja a 80 km/h durante 3 horas, então a distância é 80 * 3 = 240 quilômetros.
A distância total percorrida é 120 + 240 = 360 quilômetros.
Agora, preciso calcular o tempo total gasto. O tempo total é 2 + 3 = 5 horas.
Para encontrar a velocidade média, divido a distância total pelo tempo total: 360 quilômetros ÷ 5 horas = 72 km/h.
Portanto, a resposta correta é {'sol': 'b'}.''',
    'es': '''Producción:
Primero, necesito calcular la distancia total recorrida. Durante la primera parte del viaje, el auto viaja a 60 km/h durante 2 horas, por lo que la distancia es 60 * 2 = 120 kilómetros.
Luego, para la segunda parte del viaje, el auto viaja a 80 km/h durante 3 horas, por lo que la distancia es 80 * 3 = 240 kilómetros.
La distancia total recorrida es 120 + 240 = 360 kilómetros.
Ahora necesito calcular el tiempo total invertido. El tiempo total es 2 + 3 = 5 horas.
Para encontrar la velocidad promedio, divido la distancia total por el tiempo total: 360 kilómetros ÷ 5 horas = 72 km/h.
Por tanto, la respuesta correcta es {'sol': 'b'}.''',
    'sw': '''Pato:
Kwanza, ninahitaji kuhesabu jumla ya umbali uliosafiri. Kwa sehemu ya kwanza ya safari, gari husafiri kwa kilomita 60 / h kwa saa 2, hivyo umbali ni 60 * 2 = 120 kilomita.
Ifuatayo, kwa sehemu ya pili ya safari, gari husafiri kwa kilomita 80 / h kwa saa 3, hivyo umbali ni 80 * 3 = 240 kilomita.
Jumla ya umbali uliosafiri ni 120 + 240 = kilomita 360.
Sasa, ninahitaji kuhesabu jumla ya muda uliotumika. Muda wote ni 2 + 3 = 5 masaa.
Ili kupata kasi ya wastani, ninagawanya umbali wa jumla kwa muda wote: kilomita 360 ÷ masaa 5 = 72 km / h.
Kwa hivyo, jibu sahihi ni {'sol': 'b'}.''',
    'yo': '''Abajade:
Ni akọkọ, Mo nilo lati ṣe iṣiro lapapọ ijinna ti o rin irin-ajo. Fun apakan akọkọ ti irin-ajo naa, ọkọ ayọkẹlẹ naa rin irin-ajo ni 60 km / h fun wakati 2, nitorina ijinna jẹ 60 * 2 = 120 kilomita.
Nigbamii ti, fun apakan keji ti irin-ajo naa, ọkọ ayọkẹlẹ naa rin irin-ajo ni 80 km / h fun wakati 3, nitorina ijinna jẹ 80 * 3 = 240 kilomita.
Lapapọ ijinna ti a rin jẹ 120 + 240 = 360 kilomita.
Bayi, Mo nilo lati ṣe iṣiro lapapọ akoko ti o lo. Lapapọ akoko jẹ 2 + 3 = 5 wakati.
Lati wa iyara apapọ, Mo pin aaye lapapọ nipasẹ akoko apapọ: 360 kilomita ÷ 5 wakati = 72 km / h.
Nitorina, idahun ti o pe ni {'sol': 'b'}.''',
    'zh': '''输出：
首先，我需要计算行驶的总距离。行程的第一部分，汽车以 60 公里/小时的速度行驶 2 小时，因此距离为 60 * 2 = 120 公里。
接下来，对于行程的第二部分，汽车以 80 公里/小时的速度行驶 3 小时，因此距离为 80 * 3 = 240 公里。
总行驶距离为120+240=360公里。
现在，我需要计算花费的总时间。总时间为2+3=5小时。
为了找到平均速度，我将总距离除以总时间：360 公里 ÷ 5 小时 = 72 公里/小时。
因此，正确答案是{'sol': 'b'}。'''}


def replaceSpaces(text, language):
    if language in ['ja', 'zh']:
        parts = re.split(r'(\{[^}]*\})', text)
        for i in range(len(parts)):
            if not parts[i].startswith('{') and not parts[i].endswith('}'):
                parts[i] = " ".join(parts[i].replace(' ', ''))
        return ''.join(parts)
    else:
        return text.replace(' ', '  ')


def addEmojis(text, language):
    if language in ['ja', 'zh']:
        parts = re.split(r'(\{[^}]*\})', text)
        for i in range(len(parts)):
            if not parts[i].startswith('{') and not parts[i].endswith('}'):
                parts[i] = "🙂".join(parts[i].replace(' ', ''))
        return ''.join(parts)
    else:
        return text.replace(' ', '🙂')

def concatenate_dicts(dict1, dict2, dict3):
    result = {}
    for key in dict1:
        result[key] = []
        # for item1 in dict1[key]:
        result[key].append(f"{dict1[key][0]}{dict2[key]}{dict3[key]}")  # Original
        result[key].append(f"{dict1[key][1]}{dict2[key]}{replaceSpaces(dict3[key],key)}")  # TwoSpaces
        result[key].append(f"{dict1[key][2]}{dict2[key]}{addEmojis(dict3[key],key)}")  # Emojis
        result[key].append(f"{dict1[key][3]}{dict2[key]}{dict3[key].upper()}")  # CapitalLetters
    return result

system_messages = concatenate_dicts(prompt_instructions,prompt_example_inputs,prompt_example_outputs)
1
