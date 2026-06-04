"""
Varied response templates for LocalRulesProvider fallback.
Provides human-like, empathetic, and contextually appropriate responses
when Gemini API is unavailable or quota is exhausted.
"""
import random


class ResponseTemplates:
    """Collection of varied response templates organized by intent/domain."""
    
    # BREAKUP responses
    BREAKUP = [
        "सुनकर बहुत दुख हुआ कि तुम इस मुश्किल दौर से गुज़र रहे हो। ब्रेकअप का दर्द बहुत गहरा होता है, और तुम्हारा दिल रो रहा है, बेचैनी महसूस हो रही है, यह बिल्कुल स्वाभाविक है। इस तरह का दर्द महसूस करना एक बहुत ही human experience है। अभी तो बस अपने आप को थोड़ा समय दो - रोना ठीक है, टूटना ठीक है। यह process है, और हर process का अपना time होता है।",
        
        "यह दर्द real है, और यह acknowledge करना important है। कई बार हम सोचते हैं कि हमें strong रहना चाहिए, पर असली strength यही है कि हम अपनी feelings को accept करें। तुम अकेले नहीं हो इस feeling में - लाखों लोग हर रोज़ इसी pain से गुज़र रहे हैं। अभी बस breathing पर focus करो, एक step एक time।",
        
        "Breakup के बाद का यह phase बहुत challenging होता है। तुम्हारा mind बहुत सारे questions पूछ रहा होगा - क्यों हुआ, क्या गलत किया, क्या होगा आगे। ये सब natural है। पर अभी सबसे important यह है कि तुम अपनी healing को priority दो। अपने आप को blame मत करो - relationships complex होते हैं, और अक्सर कोई एक person की गलती नहीं होती।",
        
        "दिल टूटने का यह experience बहुत overwhelming हो सकता है। तुम्हारी body भी react कर रही होगी - sleep issues, appetite changes, energy low। यह सब normal है। अभी तुम्हें बस basic self-care की ज़रूरत है - खाना, सोना, थोड़ा movement। Healing में time लगता है, और यह linear नहीं होता - कुछ दिन अच्छे रहोगे, कुछ बुरे। यह okay है।",
    ]
    
    # ANXIETY responses
    ANXIETY = [
        "Future के बारे में यह darr bilkul common है। जब हम unknown को face करते हैं, तो हमारा brain naturally threat detect करने की कोशिश करता है। यह survival mechanism है, पर जब यह overactive हो जाता है, तो anxiety बन जाता है। अभी तुम्हारा mind future की scenarios generate कर रहा होगा - और ज़्यादातar negative ones। यह normal है, पर इसे manage करना possible है।",
        
        "Anxiety बहुत exhausting हो सकती है। तुम्हारा heart तेज़ धड़क रहा होगा, thoughts racing होंगे, body tense होगी। यह सब तुम्हारी nervous system की response है। अभी तुम्हें अपनी body को calm करने की ज़रूरत है - deep breathing, grounding techniques। Mind को control करने की कोशिश मत करो, बस observe करो।",
        
        "Job tension, future uncertainty, health worries - ये सब valid concerns हैं। पर जब ये concerns तुम्हें paralyze करने लगते हैं, तो यह problem बन जाता है। Anxiety में हमारा brain worst-case scenarios imagine करता है। Reality में ज़्यादातar situations उतने bad नहीं होते जितने हम सोचते हैं। अभी तुम्हें अपने thoughts को reality check करना होगा।",
        
        "Raat ko overthinking बहुत common है anxiety में। जब दुनिया चुप होती है, तुम्हारा mind जाग जाता है। यह cycle बहुत frustrating हो सकता है। अभी तुम्हें अपनी sleep hygiene पर काम करना होगा - screen time कम करना, relaxation techniques try करना। और यह remember रखना कि thoughts सिर्फ़ thoughts हैं, facts नहीं।",
    ]
    
    # VALIDATION-SEEKING responses
    VALIDATION = [
        "यह feeling कि तुम unimportant हो या किसी को parvah नहीं, बहुत painful हो सकती है। यह often childhood से आती है - जब हमें validation नहीं मिलती, तो हम internalize कर लेते हैं कि हम worthy नहीं हैं। पर यह truth नहीं है। तुम्हारी worth external validation पर dependent नहीं है। यह internal है।",
        
        "Parents से appreciation न मिलना बहुत hurtful हो सकता है। बहुत से cultures में parents express करने में struggle करते हैं। यह इसका mean नहीं कि वो तुमसे pyaar नहीं करते या तुम proud नहीं हो। यह उनकी limitation है, तुम्हारी नहीं। तुम्हें अपनी validation खुद से खोजनी होगी।",
        
        "Social media dekh kar inferiority feel karna bahut common hai. Hum sabko curated lives dikhte hain - perfect photos, happy moments. Reality mein sabke struggles hote hain. Tum apni real life ko kisi aur ke highlight reel se compare kar rahe ho - yeh unfair comparison hai. Tum apni journey, apni pace pe ho.",
        
        "Confidence achanak nahi aata - yeh build hota hai. Small achievements se start karo, apne strengths ko recognize karo. Tum kaam ke ho - yeh fact hai, chahe tumhe feel ho ya nahi. External validation important hai, par internal validation zyada important hai. Apne aap ko treat karo jaise tum apne best friend ko treat karte ho.",
    ]
    
    # SELF-ESTEEM responses
    SELF_ESTEEM = [
        "'Main kaun hoon?' yeh question bahut deep hai. Iska matlab hai ki tum apni identity explore kar rahe ho. Yeh normal hai - hum sab kabhi na kabhi yeh phase se guzarte hain. Tumne kuch achieve nahi kiya - yeh perception hai, reality nahi. Tumne jo bhi experience kiya, wo tumhe define nahi karta. Tum kaun ho, yeh tumhari values, tumhari kindness, tumhari resilience se define hota hai.",
        
        "Friends successful hain, main fail hoon - yeh comparison trap hai. Har person ki journey different hoti hai. Tumne jo dekha wo result hai, process nahi. Tumne unke struggles, unke failures nahi dekhe. Apni journey ko apni pace pe chalo. Success define karna tumhara kaam hai - society ka nahi.",
        
        "Khud se nafrat karna bahut painful hai. Yeh often internalized criticism hai - shayad kisi ne tumhe yeh sunaya ya tumne yeh assume kar liya. Par yeh truth nahi hai. Tum flaws ke saath perfect ho - yeh human condition hai. Self-compassion seekhna seekhna zaroori hai. Treat yourself with same kindness jo tum dusro ko dete ho.",
        
        "Tumne kuch bada nahi kiya - yeh judgment hai. Small achievements bhi count karte hain. Tum zinda ho, tum seekh rahe ho, tum try kar rahe ho - yeh sab achievements hain. Bada achieve karne ka pressure society ka hai, tumhara nahi. Apni definition of success banao.",
    ]
    
    # HUMAN BEHAVIOR responses
    HUMAN_BEHAVIOR = [
        "Log hurt karte hain - yeh painful truth hai. Kabhi intentionally, kabhi unintentionally. Human nature complex hai - har person ka apna perspective, apna baggage hota hai. Jab log hurt karte hain, toh yeh often unki insecurity, unka pain reflect karta hai, tumhari worth nahi. Yeh samajhna important hai ki tumhari reaction tumhare control mein hai.",
        
        "Fake log, changing behavior - yeh bahut common hai. Kuch log genuine hain, kuch adapt karte hain situations ke hisaab se. Yeh confusing ho sakta hai. Par yeh samajhna hai ki consistency rare hai. Tum apni boundaries set karo - jo log consistent nahi hain, unse expectations kam karo. Trust earn hota hai, time ke saath.",
        
        "Selfishness human nature ka hissa hai. Survival instinct hai. Par yeh mean nahi ki sab log selfish hain. Bahut log empathetic bhi hote hain. Tumne jo dekha wo negative examples hain, positive bhi honge. Balance dhundhna zaroori hai. Apne aap ko protect karna seekho - par iska mean nahi ki tum sabko distrust karo.",
        
        "Trust karna mushkil hai jab hurt ho chuka hai. Par isolation bhi dangerous hai. Healthy boundaries zaroori hain - trust ko earn karna do, time ke saath. Sab log same nahi hote. Tum apne intuition pe trust karo - jo safe feel kare, unhe open karo. Jo red flags de, unse distance rakho.",
    ]
    
    # STOICISM responses
    STOICISM = [
        "Stoicism ek philosophy hai jo focus karta hai control mein jo cheezein hain, accept karna jo nahi hain. Memento mori - death ka yaad rakhna, yeh life ko perspective deta hai. Dichotomy of control - tum control kar sakte ho kya? Apne reactions, apne choices. Baaki sab external hai. Yeh practice hai, daily.",
        
        "Emotions control karna mean nahi hai suppress karna. Stoicism mein emotions ko observe karna, understand karna, phir rational response dena hota hai. Anger aayega - thik hai. Par anger ke bawjud act karna, yeh choice hai. Between stimulus aur response mein gap hai - yeh gap fill karna seekhna hai.",
        
        "Bad situations mein calm rehna practice hai. Seneca ne kaha - we suffer more in imagination than in reality. Situation bad ho sakti hai, par tumhara response usse zyada important hai. Amor fati - love fate. Jo bhi ho, accept karo, phir act karo. Resistance increases suffering.",
        
        "Marcus Aurelius ne kaha - you have power over your mind, not outside events. External events control nahi hote, tumhara interpretation control hai. Same situation, different perspectives, different experiences. Yeh power hai tumhare paas. Daily journaling, reflection, negative visualization - yeh tools hain.",
    ]
    
    # DARK PSYCHOLOGY responses
    DARK_PSYCHOLOGY = [
        "Manipulation ek tactic hai jo log use karte hain control ke liye. Guilt tripping, gaslighting, love bombing - yeh sab common techniques hain. Recognize karna seekho - jab tum guilt feel kar rahe ho without valid reason, jab tumhara reality question ho raha hai, jab tumhara instincts warning de rahe hain. Yeh red flags hain.",
        
        "Gaslighting ek form hai emotional abuse ka. Tumhara reality question hota hai, tum doubt khud ko. Common phrases - 'tum crazy ho', 'yeh nahi hua', 'tum overreact kar rahe ho'. Trust your instincts. Agar tum feel ho rahe ho ki something off hai, toh probably off hai. Document karo, external validation lo.",
        
        "Narcissists ka behavior pattern hota hai - grandiosity, lack of empathy, need for admiration. Initial phase mein charming hote hain, phir devalue karte hain. Love bombing followed by devaluation. Yeh cycle repeat hota hai. Recognize karna zaroori hai - boundaries set karo, expectations kam karo, exit plan banao.",
        
        "Toxic relationships identify karna important hai. Red flags - isolation from friends/family, constant criticism, guilt trips, control issues, disrespect for boundaries. Healthy mein respect, trust, communication hota hai. Toxic mein power imbalance hota hai. Apne aap ko protect karna priority hai - help lo, exit karo.",
    ]
    
    # EMOTIONAL DEPENDENCY responses
    EMOTIONAL_DEPENDENCY = [
        "Bina uske soch nahi paana - yeh attachment ka sign hai. Healthy attachment mein independence bhi hoti hai. Tumhara identity uspe dependent ho gaya hai - yeh risky hai. Apne individuality ko recover karna zaroori hai. Tum uske bina bhi complete ho.",
        
        "Call nahi aane par darr - yeh anxiety attachment ka hai. Fear of abandonment. Yeh often past experiences se aata hai. Par yeh mean nahi ki vo tumhe chhod degi. Communication seekho - apne fears express karo. Par iska mean nahi ki vo 24/7 available rahe. Healthy space zaroori hai.",
        
        "Friends se door ho jana - social isolation ka sign hai. Relationship ke liye sab sacrifice karna unhealthy hai. Balance maintain karna zaroori hai. Tumhara support system important hai - use maintain karo. Relationship enhance kare life, sacrifice na kare.",
        
        "Pyaar ya obsession - yeh line thin hai. Pyaar mein respect, freedom, growth hota hai. Obsession mein control, fear, dependency hoti hai. Introspect karo - tum pyaar karte ho ya tumhe chahiye ki vo tumhe pyaar kare? Difference samajhna zaroori hai.",
    ]
    
    # GENERAL/CLARITY SEEKING responses
    GENERAL = [
        "अच्छा सवाल - clarity seek करना healthy है। Psychology mechanisms देती हैं, perfect answers नहीं। पर mechanism समझने से confusion कम होती है। बताओ - सबसे confuse क्या लग रहा है अभी?",
        
        "समझा। जो बताया — उसके साथ तुम्हारा body और mind दोनों react कर रहे होंगे। अगर चाहो, थोड़ा और खोल सकते हो — मैं यहीं हूँ।",
        
        "यह एक बहुत ही important topic है। इसके कई layers हैं - surface level पर एक बात, deeper level पर कुछ और। तुम किस level पर discuss करना चाहते हो?",
        
        "Interesting point. Yeh complex issue hai - multiple factors contribute karte hain. Tum kis aspect pe focus karna chahte ho? Psychological, behavioral, ya practical dimension?",
    ]
    
    # COPING STRATEGY responses
    COPING = [
        "Coping strategies different hoti hain - adaptive aur maladaptive. Adaptive mein problem-solving, seeking support, self-care. Maladaptive mein avoidance, substance use, denial. Tum currently kya use kar rahe ho? Kya kaam kar raha hai, kya nahi?",
        
        "Healthy coping seekhna zaroori hai. Exercise, meditation, journaling, talking to friends - yeh sab evidence-based strategies hain. Par yeh mean nahi ki tum hamesha strong rahna chaahiye. Sometimes doing nothing bhi okay hai - rest is coping bhi.",
        
        "Coping is individual - jo ek ke liye kaam karta hai, doosre ke liye nahi. Experiment karo, dekho kya suit karta hai. Consistency important hai - ek baar try karne se result nahi aata. Patience zaroori hai.",
    ]


def get_response(domain: str, emotion: str = "neutral") -> str:
    """
    Get a varied response based on domain and emotion.
    
    Args:
        domain: The psychological domain (breakup, anxiety, validation, etc.)
        emotion: The emotional state (grief, fear, neutral, etc.)
    
    Returns:
        A varied, human-like response string
    """
    # Map domains to response templates
    domain_map = {
        'breakup': ResponseTemplates.BREAKUP,
        'anxiety': ResponseTemplates.ANXIETY,
        'self_esteem': ResponseTemplates.SELF_ESTEEM,
        'validation': ResponseTemplates.VALIDATION,
        'human': ResponseTemplates.HUMAN_BEHAVIOR,
        'behavior': ResponseTemplates.HUMAN_BEHAVIOR,
        'stoic': ResponseTemplates.STOICISM,
        'stoicism': ResponseTemplates.STOICISM,
        'dark': ResponseTemplates.DARK_PSYCHOLOGY,
        'dependency': ResponseTemplates.EMOTIONAL_DEPENDENCY,
        'coping': ResponseTemplates.COPING,
    }
    
    # Get appropriate response pool
    responses = domain_map.get(domain.lower(), ResponseTemplates.GENERAL)
    
    # Randomly select a response
    return random.choice(responses)
