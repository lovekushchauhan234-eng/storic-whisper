"""

Natural conversation layer — human-first responses before psychology depth.

"""

import random



from .domains import Domain

from .emotional import EmotionalContext, EmotionalTone

from .intent import ConversationIntent, IntentResult, ResponseDepth

from .memory.schemas import SessionMemory





def _pick(options: list[str]) -> str:

    return random.choice(options)





GREETING_REPLIES = [
    "Hey! 👋 Kya haal hai?",
    "Hi there! Aaj kya scene hai?",
    "Hello! Long time no see... ya pehli baar? 😄",
    "Yo! Kya chal raha hai?",
    "Namaste! 🙏 Kya baat karni hai?",
    "Hey! Tum aa gaye, achha hai",
    "Hi! Aaj ka mood kaisa hai?",
    "Hello! Kis baare mein baat karna hai?",
    "Hey there! Kya plan hai aaj ka?",
    "Hi! Sab theek?",
    "Hello! Tum kaise ho?",
    "Hey! Kya naya chal raha hai life mein?",
    "Hi! Aaj din kaisa gaya?",
    "Hello! Kya kar rahe ho?",
    "Hey! Mood kaisa hai?",
    "Hi! Kis baat pe discuss karna hai?",
    "Hello! Tumhari taraf se kya sunna hai?",
    "Hey! Aaj kya special hai?",
    "Hi! Kya scene hai?",
    "Hello! Tum theek ho na?",
]



SMALL_TALK_REPLIES = {
    'how_are_you': [
        "Main theek hoon! Tum batao, kya scene hai?",
        "Sab chill! Tum kaise ho?",
        "Bas normal, tumhari taraf se kya hai?",
        "Theek hoon, tum kya kar rahe ho?",
        "Achha hoon! Aaj ka din kaisa hai tumhara?",
        "Steady! Tum kaise chal rahe ho?",
        "Main fine, tum batao kya haal hai?",
        "All good! Tum theek ho na?",
        "Bas yahin! Tum kya plan kar rahe ho?",
        "Chill! Tum kaise ho aaj?",
    ],
    'what_doing': [
        "Bas yahin tumhari baat sun raha hoon! 😄",
        "Kuch special nahi, tumse hi baat kar raha hoon",
        "Free hoon, tum kya scene kar rahe ho?",
        "Bas chill! Tum kya plan hai?",
        "Kuch naya nahi, tumhari hi wait kar raha tha",
        "Relaxing! Tum kya kar rahe ho?",
        "Bas time pass, tum kya chal raha hai?",
        "Free hoon! Kya baat karni hai?",
        "Kuch khaas nahi, tum batao kya scene hai",
        "Bored! Tum kya kar rahe ho?",
    ],
    'thanks': [
        "No problem! 😊",
        "Welcome!",
        "Anytime!",
        "Arey bas! Kuch nahi",
        "Kuch nahi! Tum batao kya chahiye",
        "Pleasure! 😄",
        "No worries!",
        "Sure thing!",
        "Achha! Kuch aur baat hai?",
        "You're welcome!",
    ],
    'bye': [
        "Bye bye! Take care 👋",
        "See ya! Phir milenge",
        "Okay, bye! Achha raha",
        "Chal bye! Phir kab",
        "Take care! Phir milte hain",
        "Bye! Kal baat karte hain",
        "Okay bye! Stay safe",
        "See you later! 👋",
        "Chal, phir!",
        "Bye! Achha tha",
    ],
    'good_morning': [
        "Good morning! ☀️ Aaj ka plan kya hai?",
        "Morning! Coffee pee li?",
        "GM! Aaj kya karna hai?",
        "Suprabhat! Aaj din kaisa hai?",
        "Good morning! Aaj mood kaisa hai?",
        "Morning! Uth gaye?",
        "GM! Kya scene hai aaj?",
        "Good morning! Kya special hai aaj?",
        "Morning! Kya plan hai?",
        "Suprabhat! Aaj kya karna hai?",
    ],
    'good_night': [
        "Good night! 😴 Sweet dreams",
        "GN! Achhi neend aaye",
        "Shubh ratri! Kal milte hain",
        "Good night! Sleep tight",
        "GN! Kal baat karte hain",
        "Night! Achha raha",
        "Good night! Take care",
        "GN! So jao",
        "Shubh ratri! Kal phir",
        "Night! Sweet dreams ✨",
    ],
    'default': [
        "Haan bolo?",
        "Kya hai?",
        "Batao kya chal raha hai",
        "Kya scene hai?",
        "Haan, sun raha hoon",
        "Bolo bolo",
        "Kya baat hai?",
        "Haan, tell me",
        "Kya chahiye?",
        "Batao na",
    ],
}



CASUAL_REPLIES = [
    "Haan bolo, kya hai?",
    "Kya scene hai?",
    "Batao na, kya chal raha hai",
    "Hmm, sun raha hoon",
    "Achha, aur batao",
    "Kya baat karni hai?",
    "Haan, tell me",
    "Bolo bolo, main sun raha hoon",
    "Kya chahiye?",
    "Aur kya?",
    "Batao",
    "Kya hua?",
    "Sunna hai kya?",
    "Kya plan hai?",
    "Bolo",
    "Kya scene?",
    "Haan haan, batao",
    "Achha",
    "Kya baat hai?",
    "Tell me",
    "Batao na",
]



# Dating/Relationship casual conversation
DATING_CASUAL_REPLIES = [
    "Dating scene alag hota hai! Tum kis type ki dhundh rahe ho?",
    "Relationship mein thoda time lagta hai. Kisi specific ke baare mein baat kar rahe ho?",
    "Har case different hota hai. Tumhara situation kya hai?",
    "Sabse pehle khud ko samajhna zaroori hai. Tum kya chahte ho exactly?",
    "Approach karna ya impress karna - dono alag hain. Tum kaun se try kar rahe ho?",
    "Dating mein patience chahiye. Kisi ke baare mein baat kar rahe ho?",
    "Har relationship alag hoti hai. Tumhara case kya hai?",
    "Pehle khud ko clear karo. Tum kis type ki partner chahte ho?",
    "Kya tum kisi ke saath involved ho ya planning kar rahe ho?",
    "Tum kya chahte ho exactly - casual ya serious?",
    "Dating mein expectations set karna zaroori hai. Tum kya soch rahe ho?",
    "Har person alag hota hai. Tum kis ke baare mein baat kar rahe ho?",
    "Tumhara preference kya hai?",
    "Kya tum already kisi ke saath ho ya naya dhundh rahe ho?",
    "Approach method alag hota hai. Tum kaun se follow kar rahe ho?",
]



# Personal questions
PERSONAL_QUESTION_REPLIES = [
    "Achha sawal! Kyun soch rahe ho is baare mein?",
    "Yeh thodi personal hai, par theek hai. Batao kya jaanna chahte ho",
    "Hmm, interesting! Pehle tum batao - khud kya feel karte ho?",
    "Aaj suddenly is baare mein kyun socha?",
    "Good question! Tumhara perspective kya hai is baare mein?",
    "Yeh sawal sunke kuch socha?",
    "Kyun puch rahe ho exactly?",
    "Interesting! Tum kya sochte ho?",
    "Batao, kya curiosity hai?",
    "Hmm, kyun jaanna chahte ho?",
    "Yeh sawal deep hai! Tum kya feel karte ho?",
    "Achha! Kya specific jaanna chahte ho?",
    "Pehle tum batao - tumhara view kya hai?",
    "Kyun important lag raha hai yeh sawal?",
    "Batao, kya soch rahe ho?",
]



# Psychological concept question replies (for "what is X" type questions)
CONCEPT_QUESTION_REPLIES = [
    "Yeh concept interesting hai! Kya specific aspect pe discuss karna chahte ho?",
    "Achha sawal! Yeh topic depth mein hai. Kya samajhna chahte ho exactly?",
    "Yeh concept samajhna zaroori hai. Tumhara perspective kya hai is baare mein?",
    "Good question! Yeh multiple dimensions ka hai - psychological, behavioral, practical. Kya pehle explore karna chahte ho?",
    "Yeh bahut useful concept hai. Kya context mein jaanna chahte ho?",
    "Interesting topic! Kya specific jaanna chahte ho?",
    "Yeh concept important hai. Tum kya sochte ho is baare mein?",
    "Achha! Kya detail mein samajhna chahte ho?",
    "Yeh topic deep hai. Kya pehle explore karna chahte ho?",
    "Good one! Tumhara view kya hai?",
    "Yeh concept helpful ho sakta hai. Kya situation mein use karna chahte ho?",
    "Yeh bahut relevant hai. Kya specific aspect pe focus karna chahte ho?",
    "Achha sawal! Kya practical application jaanna chahte ho?",
    "Yeh concept samajhne ke liye thoda time lagta hai. Kya step by step samjhau?",
    "Yeh topic alag hai. Kya pehle basic samajhna chahte ho ya advanced?",
]



# Deep psychology replies (for general psychological discussions)
DEEP_PSYCHOLOGY_REPLIES = [
    "Yeh topic interesting hai! Kya soch rahe ho is baare mein?",
    "Achha point! Kya specific aspect pe discuss karna chahte ho?",
    "Hmm, yeh deep hai. Pehle tum batao - khud kya feel karte ho?",
    "Yeh baat depth mein hai. Kya tumhare life mein iska experience hai?",
    "Interesting! Kya perspective hai tumhara?",
    "Yeh topic alag hai. Kya explore karna chahte ho?",
    "Achha! Kya specific baat karni hai?",
    "Yeh bahut relevant hai. Tum kya sochte ho?",
    "Hmm, yeh important hai. Kya detail mein baat karni hai?",
    "Yeh topic discuss karne layak hai. Kya pehle start karein?",
    "Achha sawal! Kya angle se dekhna chahte ho?",
    "Yeh deep hai. Kya step by step discuss karein?",
    "Interesting! Kya context hai tumhara?",
    "Yeh topic samajhne layak hai. Kya pehle basic clear karein?",
    "Achha! Kya specific explore karna chahte ho?",
]



EMOTIONAL_CHECKIN_REPLIES = [
    "Jo feel ho raha hai, wo real hai. Sabse heavy kya lag raha hai abhi?",
    "Sun liya. Abhi clarity chahiye ya bas koi sunna chahte ho?",
    "Okay, main yahin hoon. Thoda context do - ye feeling kab se hai?",
    "Haan, samajh raha hoon. Kya specifically feel ho raha hai?",
    "Valid hai ye feeling. Kya trigger hua?",
    "Sun raha hoon. Kya share karna chahte ho?",
    "Okay, batao. Kya chal raha hai mind mein?",
    "Haan, samajha. Kya specifically disturb kar raha hai?",
    "Valid hai ye. Kya pehle discuss karna chahte ho?",
    "Sun liya. Kya depth mein baat karni hai?",
    "Okay, main yahin hoon. Kya specifically feel ho raha hai?",
    "Haan, batao. Kya heavy lag raha hai?",
    "Samajh raha hoon. Kya share karna chahte ho?",
    "Valid hai. Kya specifically discuss karna chahte ho?",
    "Okay, batao. Kya scene hai?",
]



STUDY_OPENERS = [
    "Padhte waqt distraction aksar brain ki cry hoti hai - 'mujhe stimulation chahiye'",
    "Study mode mein mind wander karna failure nahi - signal hai ki task ya environment match nahi kar rahe",
    "Focus nahi kar pa rahe? Ye common hai",
    "Padhai mein distraction normal hai, par fix karna possible hai",
    "Study mein attention issue hota hai. Kya specifically distract kar raha hai?",
    "Mind wander karna normal hai. Kya specifically focus nahi kar pa rahe?",
    "Padhai mein problem common hai. Kya specifically disturb kar raha hai?",
    "Focus issues aksar environment se hote hain. Kya scene hai?",
    "Study mein distraction common hai. Kya try kar rahe ho?",
    "Attention span issue hai. Kya specifically help chahiye?",
    "Padhai mein focus problem normal hai. Kya specifically hua?",
    "Study distractions kabhi kabhi bahut frustrating ho jaate hain. Batao kya scene hai",
    "Mind wandering common hai. Kya specifically pareshan kar raha hai?",
    "Focus nahi kar pa raha? Ye common issue hai. Kya try kar rahe ho?",
    "Study mein attention problem hai. Kya specifically discuss karna chahte ho?",
]



STUDY_FOLLOW_LIGHT = [
    "\n\nEk cheez try karo: phone doosre room mein, sirf 25 minute ek block - bina perfect hone ka pressure.\n\nKya abhi exam pressure hai ya general focus?",
    "\n\nTry karo: phone door rakh do, 25-30 minute focus block.\n\nKya exam pressure hai ya general focus issue?",
    "\n\nSimple trick: phone alag room mein, 25 minute timer.\n\nExam pressure hai ya general focus problem?",
    "\n\nEk idea: phone doosre room, 25 minute study block.\n\nKya exam hai ya general focus?",
    "\n\nTry karo: phone door, 25 minute timer set karo.\n\nExam pressure hai ya general focus?",
    "\n\nSimple: phone alag, 25 minute block.\n\nExam pressure hai ya general?",
    "\n\nPhone door rakh do, 25 minute focus.\n\nExam hai ya general focus?",
    "\n\n25 minute rule try karo - phone door.\n\nExam pressure ya general?",
    "\n\nPhone doosre room, 25 minute timer.\n\nExam hai ya general focus?",
    "\n\nSimple approach: phone door, 25 minute block.\n\nExam pressure hai ya general?",
]



RELATIONSHIP_OPENERS = [
    "Ye sunke lagta hai kuch heavy chal raha hai",
    "Relationship pain sirf fight nahi hota - connection ya safety tootne jaisa feel hota hai",
    "Lagta hai kuch baat hai. Batao kya hua?",
    "Ye sunke feel ho raha hai kuch disturb ho",
    "Relationship issues kabhi kabhi bahut heavy ho jaate hain",
    "Kuch hua hai jo tum disturb kar raha hai. Batao",
    "Ye sunke lag raha hai kuch serious hai",
    "Relationship mein problems common hain, par personal feel hota hai",
    "Kuch baat hai jo tum pareshan kar rahi hai. Share karo",
    "Ye sunke samajh raha hoon kuch deep hai",
    "Relationship issues kabhi easy nahi hote. Batao kya scene hai",
    "Lagta hai kuch emotional hai. Batao",
    "Ye sunke feel ho raha hai kuch hurt ho",
    "Relationship pain alag hota hai. Kya specifically hua?",
    "Kuch baat hai jo tum affect kar rahi hai. Batao",
]



RELATIONSHIP_FOLLOW = [
    "\n\nMain judge nahi karunga - bas samajhna chahta hoon.\n\nKya recently koi moment hai jo sabse zyada repeat ho raha hai?",
    "\n\nBatao kya specifically hua?",
    "\n\nNo judgment zone. Batao kya disturb kar raha hai?",
    "\n\nSamajhne ki koshish karunga. Kya share karna chahte ho?",
    "\n\nKya specifically discuss karna chahte ho?",
    "\n\nKuch bhi bol sakte ho. Kya pehle batana chahte ho?",
    "\n\nSafe space hai. Batao kya heavy lag raha hai?",
    "\n\nMain understand karne ki koshish karunga. Kya context hai?",
    "\n\nKuch bhi share kar sakte ho. Kya specifically hua?",
    "\n\nBina judge kiye sununga. Batao kya hai?",
    "\n\nKya pehle discuss karna chahte ho?",
    "\n\nOpen space hai. Batao kya feel ho raha hai?",
    "\n\nKuch bhi bol sakte ho. Kya specifically disturb ho?",
    "\n\nKya share karna chahte ho?",
    "\n\nBatao, main samajhne ki koshish karunga",
]



LONELINESS_OPENERS = [
    "Akelapan kabhi kabhi crowd mein bhi aata hai - ye connection ki kami ho sakti hai, logon ki nahi",
    "Ye feeling valid hai. Kabhi kabhi hum available hote hain, par witnessed nahi feel karte",
    "Lagta hai akela feel kar rahe ho. Kya specifically disturb kar raha hai?",
    "Loneliness common hai, par personal feel hota hai. Kya scene hai?",
    "Ye sunke lag raha hai kuch disconnect feel ho raha hai",
    "Akelapan bahut heavy ho sakta hai. Kya specifically feel ho raha hai?",
    "Crowd mein bhi akela feel karna common hai. Kya trigger hua?",
    "Ye feeling valid hai. Kya specifically disturb kar raha hai?",
    "Loneliness alag hota hai. Kya specifically feel ho raha hai?",
    "Ye sunke samajh raha hoon kuch deep hai",
    "Akelapan kabhi kabhi bahut tough ho jaata hai. Batao kya scene hai",
    "Kuch baat hai jo tum akela feel kar rahi hai. Share karo",
    "Ye sunke feel ho raha hai kuch hurt ho",
    "Loneliness alag hota hai. Kya specifically hua?",
    "Kuch baat hai jo tum affect kar rahi hai. Batao",
]



LONELINESS_FOLLOW = [
    "\n\nAaj raat - kya tumhe kisi specific person ki kami hai, ya bas khud se disconnect feel ho raha hai?",
    "\n\nKya specifically miss kar rahe ho?",
    "\n\nKuch specific hai jo disturb kar raha hai?",
    "\n\nKya specifically discuss karna chahte ho?",
    "\n\nKya pehle bataana chahte ho?",
    "\n\nKya specifically heavy lag raha hai?",
    "\n\nKya context hai?",
    "\n\nKya specifically hua?",
    "\n\nKya share karna chahte ho?",
    "\n\nKya specifically disturb ho?",
    "\n\nKya pehle discuss karna chahte ho?",
    "\n\nKya specifically feel ho raha hai?",
    "\n\nKya specifically miss ho raha hai?",
    "\n\nKya specifically heavy hai?",
    "\n\nBatao, main samajhne ki koshish karunga",
]



# Crisis responses (safety priority)

CRISIS_SUICIDAL_REPLIES = [

    "मैं सुन रहा हूँ कि तुम्हें बहुत heavy लग रहा है। तुम alone नहीं हो।\n\n"

    "अभी professional help लेना important है:\n\n"

    "📞 India: 112 (Emergency), 9152987821 (iCall)\n"

    "📞 International: 988 or 999 (UK/US emergency)\n\n"

    "ये numbers 24/7 available हैं। तुम्हारी life matters है।",

]



CRISIS_EMERGENCY_REPLIES = [

    "अगर तुम्हें immediate danger में feel हो रहा है, तो right now emergency services call करो:\n\n"

    "📞 India: 112\n"

    "📞 US: 911\n"

    "📞 UK: 999\n\n"

    "तुम्हारी safety पहले priority है।",

]



ANXIETY_SUPPORT_REPLIES = [
    "Panic attack feel ho raha hai - ye scary hai, par temporary hai.\n\nRight now try karo:\n1. 4-7-8 breathing: 4 sec inhale, 7 sec hold, 8 sec exhale\n2. 5 things jo tum dekh sakte ho, 4 jo tum touch kar sakte ho\n3. Ye pass hoga - body ko time do.",
    "Anxiety attack aa raha hai? Ye scary feel hota hai par temporary hai.\n\nAbhi try karo:\n1. Deep breathing - 4-7-8 technique\n2. Grounding - 5 things dekho, 4 touch karo\n3. Ye pass hoga, patience rakho.",
    "Panic feel ho raha hai? Normal hai, par temporary.\n\nRight now:\n1. 4-7-8 breathing try karo\n2. 5 things around you dekho, 4 touch karo\n3. Body ko time do, ye pass hoga.",
    "Anxiety attack? Scary hai par temporary.\n\nTry karo abhi:\n1. 4-7-8 breathing\n2. 5 things dekho, 4 touch karo\n3. Ye jayega, thoda time do.",
    "Panic mode mein ho? Ye normal hai par temporary.\n\nAbhi:\n1. Deep breathing - 4-7-8\n2. Grounding - 5 dekho, 4 touch karo\n3. Pass hoga, relax karo.",
]



DEPRESSION_SUPPORT_REPLIES = [
    "Jab sab kuch hopeless lage, ye depression ki voice ho sakti hai - reality nahi.\n\nYe feeling permanent nahi hai, par abhi real lag rahi hai.\n\nProfessional help is stage mein bahut help kar sakti hai. Therapist ya counselor se baat karna consider karo - ye weakness nahi, smart step hai.",
    "Sab kuch hopeless feel ho raha hai? Ye depression ka signal ho sakta hai, reality nahi.\n\nYe feeling permanent nahi hai, abhi real lag rahi hai.\n\nProfessional help bahut useful ho sakti hai. Therapist se baat karo - ye smart step hai, weakness nahi.",
    "Hopeless feel ho raha hai? Ye depression ki voice ho sakti hai.\n\nYe temporary hai, permanent nahi.\n\nProfessional help consider karo - therapist se baat karo. Ye strength hai, weakness nahi.",
    "Sab kuch hopeless lag raha hai? Ye depression ho sakta hai.\n\nYe feeling temporary hai, permanent nahi.\n\nProfessional help lein - therapist se baat karein. Ye smart move hai.",
    "Hopeless feel? Ye depression ka symptom ho sakta hai.\n\nYe permanent nahi hai, temporary hai.\n\nProfessional help bahut helpful hai. Counselor se baat karein - ye brave step hai.",
]



TRIGGER_SUPPORT_REPLIES = [
    "Trigger activate hona uncomfortable hai - ye body ka safety signal hai.\n\nRight now grounding try karo:\n• Feet flat on floor, feel the ground\n• 5 slow breaths\n• Khud se bolo: 'I am safe right now'\n\nJab calm ho jao, tab trigger ko observe karo - pattern dikhega.",
    "Trigger ho gaya? Ye uncomfortable hai par body ka safety signal hai.\n\nAbhi grounding try karo:\n• Feet floor pe, ground feel karo\n• 5 slow breaths lo\n• Bolo: 'I am safe right now'\n\nCalm hone ke baad trigger observe karo - pattern dikhega.",
    "Trigger activate hua? Uncomfortable feel hota hai.\n\nGrounding try karo:\n• Feet floor pe, ground feel karo\n• 5 deep breaths\n• Bolo: 'Main safe hoon right now'\n\nCalm hone ke baad trigger observe karo - pattern samajh aayega.",
    "Trigger ho gaya? Ye uncomfortable hai.\n\nGrounding karo:\n• Feet floor pe, ground feel karo\n• 5 slow breaths\n• Bolo: 'I am safe right now'\n\nCalm hone ke baad trigger dekho - pattern dikhega.",
    "Trigger activate hua? Body ka signal hai.\n\nGrounding try karo:\n• Feet floor pe, ground feel karo\n• 5 breaths lo\n• Bolo: 'Main safe hoon'\n\nCalm hone ke baad trigger observe karo.",
]



COPING_STRATEGY_REPLIES = [
    "Coping strategies unique hote hain - jo ek ke liye kaam karta, doosre ke liye nahi.\n\nKuch try kar sakte ho:\n• Journaling (thoughts paper par likho)\n• Walk ya light exercise\n• Creative activity (drawing, music)\n• Talking to someone safe\n\nKaun sa approach tumhe suit karta hai?",
    "Coping strategies alag hote hain - har person ke liye different.\n\nTry kar sakte ho:\n• Journaling - thoughts likho\n• Walk ya light exercise\n• Creative activity - drawing, music\n• Kisi safe se baat karo\n\nKaun sa approach tumhe suit karta hai?",
    "Coping unique hota hai - ek ke liye kaam karta, doosre ke liye nahi.\n\nTry karo:\n• Journaling\n• Walk ya exercise\n• Creative activity\n• Safe se baat karo\n\nKaun sa suit karta hai?",
    "Coping strategies alag hoti hain.\n\nTry kar sakte ho:\n• Journaling\n• Walk ya exercise\n• Creative activity\n• Safe se baat\n\nKaun sa approach suit karta hai?",
    "Coping unique hai.\n\nOptions:\n• Journaling\n• Walk ya exercise\n• Creative activity\n• Safe se baat\n\nKaun sa suit karta hai?",
]



PROGRESS_ACKNOWLEDGE_REPLIES = [
    "Progress recognize karna important hai - aksar hum ignore kar dete hain.\n\nJo bhi small improvement hai, wo valid hai. Healing linear nahi hoti - par forward movement hota hai.\n\nAbhi kaun sa area mein tumhe change feel ho raha hai?",
    "Progress ko recognize karna zaroori hai - hum aksar ignore kar dete hain.\n\nSmall improvement bhi valid hai. Healing linear nahi hoti, forward movement hota hai.\n\nAbhi kaun sa area mein change feel ho raha hai?",
    "Progress acknowledge karna important hai.\n\nSmall improvement valid hai. Healing linear nahi hoti, forward movement hota hai.\n\nKaun sa area mein change feel ho raha hai?",
    "Progress recognize karo.\n\nSmall improvement valid hai. Healing linear nahi, forward movement hota hai.\n\nKaun sa area mein change feel ho raha hai?",
    "Progress important hai.\n\nSmall improvement valid. Healing linear nahi, forward movement hota.\n\nKaun sa area mein change feel ho raha hai?",
]



CLARITY_QUESTION_REPLIES = [
    "Achha sawal - clarity seek karna healthy hai.\n\nPsychology mechanisms deti hain, perfect answers nahi. Par mechanism samajhne se confusion kam hota hai.\n\nBatao - sabse confuse kya lag raha hai abhi?",
    "Good question - clarity seek karna healthy hai.\n\nPsychology mechanisms help karti hain, perfect answers nahi deti. Par samajhne se confusion kam hota hai.\n\nBatao - sabse confuse kya lag raha hai abhi?",
    "Achha sawal - clarity seek healthy hai.\n\nPsychology mechanisms help karti hain. Samajhne se confusion kam hota hai.\n\nSabse confuse kya lag raha hai abhi?",
    "Good question - clarity healthy hai.\n\nPsychology mechanisms help. Samajhne se confusion kam.\n\nSabse confuse kya lag raha hai?",
    "Achha sawal - clarity seek healthy.\n\nPsychology mechanisms help. Samajhne se confusion kam.\n\nSabse confuse kya lag raha hai?",
]





def _small_talk_variant(message: str) -> str:

    lower = message.lower()

    if any(x in lower for x in ('how are', 'kaise ho', 'kya haal', "what's up", 'wyd')):

        return _pick(SMALL_TALK_REPLIES['how_are_you'])

    if any(x in lower for x in ('what doing', 'kya kar', 'kya kar rahe', 'kya chal')):

        return _pick(SMALL_TALK_REPLIES['what_doing'])

    if any(x in lower for x in ('thank', 'shukriya', 'dhanyavad')):

        return _pick(SMALL_TALK_REPLIES['thanks'])

    if any(x in lower for x in ('bye', 'goodbye', 'see you', 'byy')):

        return _pick(SMALL_TALK_REPLIES['bye'])

    if any(x in lower for x in ('good morning', 'morning', 'gm', 'suprabhat')):

        return _pick(SMALL_TALK_REPLIES['good_morning'])

    if any(x in lower for x in ('good night', 'night', 'gn', 'shubh ratri')):

        return _pick(SMALL_TALK_REPLIES['good_night'])

    return _pick(SMALL_TALK_REPLIES['default'])





def compose_conversational(

    intent_result: IntentResult,

    message: str,

    emotion: EmotionalContext,

    memory: SessionMemory | None = None,

) -> str:

    intent = intent_result.intent



    # Crisis responses (highest priority)

    if intent == ConversationIntent.SUICIDAL:

        return _pick(CRISIS_SUICIDAL_REPLIES)



    if intent == ConversationIntent.EMERGENCY:

        return _pick(CRISIS_EMERGENCY_REPLIES)



    if intent == ConversationIntent.ANXIETY_ATTACK:

        return _pick(ANXIETY_SUPPORT_REPLIES)



    if intent == ConversationIntent.DEPRESSION_CHECK:

        return _pick(DEPRESSION_SUPPORT_REPLIES)



    if intent == ConversationIntent.TRIGGER_IDENTIFICATION:

        return _pick(TRIGGER_SUPPORT_REPLIES)



    if intent == ConversationIntent.COPING_STRATEGY:

        return _pick(COPING_STRATEGY_REPLIES)



    if intent == ConversationIntent.PROGRESS_UPDATE:

        return _pick(PROGRESS_ACKNOWLEDGE_REPLIES)



    if intent == ConversationIntent.CLARITY_SEEKING:

        return _pick(CLARITY_QUESTION_REPLIES)



    # Original intents

    if intent == ConversationIntent.GREETING:

        return _pick(GREETING_REPLIES)



    if intent == ConversationIntent.SMALL_TALK:

        return _small_talk_variant(message)



    if intent == ConversationIntent.CASUAL:

        return _pick(CASUAL_REPLIES)



    if intent == ConversationIntent.DEEP_PSYCHOLOGY:

        # For psychological concept questions, provide informative responses even without insights

        # Check if it's a short concept question or direct psych term mention

        lower_msg = message.lower()

        concept_keywords = ('kya hai', 'what is', 'what are', 'kaise', 'how to', 'meaning', 'definition', 'क्या है', 'कैसे')

        direct_psych_terms = (

            'gaslighting', 'narcissist', 'stoicism', 'manipulation',

            'attachment', 'coping', 'mindfulness', 'cbt', 'therapy',

            'anxiety', 'depression', 'trauma', 'trigger', 'boundary',

            'emotional', 'intelligence', 'self esteem', 'confidence',

            'eq', 'meditation', 'boundaries', 'strategies', 'mechanisms',

            'toxic', 'self worth', 'being present', 'codependency'

        )

        if any(k in lower_msg for k in concept_keywords) or any(t in lower_msg for t in direct_psych_terms):

            return _pick(CONCEPT_QUESTION_REPLIES)

        # Otherwise use general deep psychology replies

        return _pick(DEEP_PSYCHOLOGY_REPLIES)



    if intent == ConversationIntent.EMOTIONAL_CHECKIN:

        if memory and memory.turns:

            return (

                "समझा।\n\n"

                "जो बताया — उसके साथ तुम्हारा body और mind दोनों react कर रहे होंगे।\n\n"

                "अगर चाहो, थोड़ा और खोल सकते हो — मैं यहीं हूँ।"

            )

        return _pick(EMOTIONAL_CHECKIN_REPLIES)



    if intent == ConversationIntent.STUDY_FOCUS:

        base = _pick(STUDY_OPENERS)

        if intent_result.depth == ResponseDepth.LIGHT:

            return base + _pick(STUDY_FOLLOW_LIGHT)

        return base + _pick(STUDY_FOLLOW_LIGHT)



    if intent == ConversationIntent.RELATIONSHIP:

        # Check if it's a casual dating question (not emotional pain)

        lower = message.lower()

        dating_keywords = ('ladki kaise patayen', 'kaise pataye', 'impress kaise', 'girlfriend kaise banaye', 

                          'dating tips', 'first date', 'approach kaise', 'ladki patane ke tarike')

        if any(k in lower for k in dating_keywords):

            return _pick(DATING_CASUAL_REPLIES)

        

        # Check if it's a personal question

        personal_keywords = ('tum kya', 'tum kaun', 'tumhara naam', 'tum kahan', 'tumse puch', 

                           'tumhare baare mein', 'about you')

        if any(k in lower for k in personal_keywords):

            return _pick(PERSONAL_QUESTION_REPLIES)

        

        # Emotional relationship discussion

        parts = [_pick(RELATIONSHIP_OPENERS)]

        if emotion.primary in (EmotionalTone.GRIEF, EmotionalTone.ATTACHMENT, EmotionalTone.CONFUSION):

            parts[0] = "यह भारी लग रहा है — और यह valid है।"

        return parts[0] + _pick(RELATIONSHIP_FOLLOW)



    if intent == ConversationIntent.LONELINESS:

        return _pick(LONELINESS_OPENERS) + _pick(LONELINESS_FOLLOW)



    if intent == ConversationIntent.AI_PHILOSOPHY:

        if intent_result.depth == ResponseDepth.NONE:

            return "मैं LUPPI हूँ 🌙\nPsychology companion — casual बात भी, depth भी।\n\nतुम क्या जानना चाहते हो?"

        return (

            "AI और mind के बीच सवाल अक्सर tech नहीं — attachment का होता है।\n\n"

            "तुम्हें क्या feel होता है जब तुम यहाँ बात करते हो — comfort, curiosity, या कुछ और?"

        )



    return _pick(CASUAL_REPLIES)





def intent_to_domain(intent: ConversationIntent) -> Domain | None:

    """Suggested domain when depth allows — not used for greetings."""

    mapping = {

        ConversationIntent.STUDY_FOCUS: Domain.DOPAMINE,

        ConversationIntent.RELATIONSHIP: Domain.BREAKUP,

        ConversationIntent.LONELINESS: Domain.HUMAN,

        ConversationIntent.AI_PHILOSOPHY: Domain.AIMIND,

        ConversationIntent.DEEP_PSYCHOLOGY: None,

    }

    return mapping.get(intent)





def trim_insight_for_light(insight_body: str, max_sentences: int = 2) -> str:

    """One soft insight paragraph — not a lecture."""

    parts = insight_body.replace('\n\n', '\n').split('\n')

    text = ' '.join(p.strip() for p in parts if p.strip())

    sentences = []

    buf = ''

    for char in text:

        buf += char

        if char in '.!?|' and len(buf.strip()) > 20:

            sentences.append(buf.strip())

            buf = ''

        if len(sentences) >= max_sentences:

            break

    if not sentences and buf.strip():

        sentences.append(buf.strip()[:280])

    return '\n\n'.join(sentences[:max_sentences])

