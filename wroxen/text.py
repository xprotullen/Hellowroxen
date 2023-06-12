# (c) TheLx0980

class ChatMSG(object):

      # Start text
      START_TXT = """
नमस्ते {}
      
मेरा नाम रॉक्सन है, मेरे बारे में और जानने के लिए नीचे दिए हुए मदद बटन पर दबाए| 
      """
      
      #help text
      HELP_TXT = """
आपको जिस बारे में मदद चाहिए उस उसके लिए नीचे बटन पर क्लिक करें।
"""

      ABOUT_TXT = """
<b>नाम:<b> रॉक्सन 
<b>लाइब्रेरी:</b> Pyrogram
<b>डेटाबेस:</b> MongoDB 
<b>भाषा:</b> पायथन 
<b>बनाने वाला:</b> @Lx0980AI
"""
      NOT_FOUND_TXT = """
आपके चैनल के लिए कोई कैप्शन नही मिला डेटाबेस में

<b>चैनल नाम:</b> {}
<b>चैनल आईडी:</b> <code>{}</code>
"""
      
      #caption
      CAPTION_TXT = """
स्वचालित कैप्शन के लिए आदेश।

<code>/set_caption</code> - इस आदेश से अपने चैनल के लिए कैप्शन तय करें, जिसे आप अपने चैनल में आने वाले मीडिया कैप्टन में संपादित करना चाहते हैं।
<b>उदाहरण:</b> /set_caption -100(चैनल_आईडी)::(आपका कैप्शन) आईडी और कैप्शन को इससे :: अलग करें।
<b>जैसे:</b> /set_caption -1001906731426::@Lx0980AI आने वालेवाले

<code>/update_caption</code> - इस आदेश की मदत से आप अपने चैनल में पहले से तय किए हुए कैप्शन को संपादित कर सकते है।
<b>जैसे:</b> <code>/update_caption (चैनल आईडी)::(कैप्शन)</code>

<code>/caption</code> - इस आदेश की मदद से आप अपने चैनल के वर्तमान के कैप्शन को चेक कर सकते हैं
<b>जैसे:</b> <code>/caption - (चैनल आईडी)</code> 
<b>सूचना</b> चैनल आईडी के शुरू में  "<code>-100</code>" लगाना न भूलें।

<code>/delete_caption</code> - इस आदेश की मदद से आप अपने चैनल के कैप्शन को डिलीट कर सकते हैं।
<b>जैसे:</b> <code>/delete_caption (चैनल आईडी)</code>

⚠️ <b>विशेष सूचना चैनल आईडी के शुरू में -100 लगाना नहीं भूलें।</b>
<b>⚠️ ऊपर दिए गए सभी आदेश केवल चैनल में ही काम (वर्क ) करेंगे। </b> 

<b>@Lx0980AI</b> के द्वारा 
"""
      
      AUTO_FORWARD_TXT = """
<code>/set_forward</code> यह आदेश आपको उस चैनल में भेजना है जिससे आप मीडिया को फॉरवर्ड करना चाहते हैं,
<b> जैसे:</b> /set_forward = (टारगेट चैनल आईडी)
टारगेट चैनल आईडी का मतलब है जिस चैनल में फॉरवर्ड करना चाहते हैं।

<code>/delete_forward</code> - फॉरवर्ड कनेक्शन को वापस हटाने के लिए यह कमांड टारगेट चैनल या जिस चैनल से आप फॉरवर्ड कर रहे थे उस चैनल में भेजें।

<b>⚠️ चैनल कनेक्शन सेट करने के बाद आप नीचे दिए गए आदेश या कमांड्स का उपयोग कर सकते हैं</b>
<code>/add_f_caption_info</code> - इस कमांड से आप यदि फॉरवर्ड चैनल आपने सेट किए हुए हैं, तो आप इस कमांड से फॉरवर्ड किए हुए मैसेज या मीडिया कैप्शन को संपादित कर सकते हैं 
       जैसे अगर आप चाहते हैं कि बोट फॉरवर्ड करने वाले मैसेजेस  में से किसी यूजरनेम को आपके यूजरनेम से बदल दे और साथ में एक कैप्शन भी जोड़ दे। तो यह आदेश आपके लिए फायदेमंद हो सकता है।
<b>आदेश फॉर्मेट:</b>
<code>/add_f_caption_info (old_username) (new_username) (Your_caption)</code>

<code>/add_f_caption</code> - इस आदेश से आप फॉरवर्ड होने वाले मीडिया के कैप्शन में किसी भी नए कैप्शन को जोड़ सकते हैं।
<b>प्रारूप:</b>
<code>/add_f_caption (कैप्शन)</code>

<code>/update_f_caption</code> - इस आदेश से आप फॉरवर्ड होने वाले के मीडिया add_f_caption को संपादित कर सकते हैं।

<code>/add_f_replace</code> - फॉरवर्ड होने वाले मीडिया के कैप्शन में कैप्शन या यूजरनाम को दूसरे यूजरनेम से बदल सकते हैं।
प्रारूप:
<code>/add_f_replace (पुराना यूजरनेम) (नया यूजरनेम)</code>

<code>/update_replace_text</code> - इस आदेश से आप add_f_replace के यूजरनेम को अपडेट कर सकते हैं प्रारूप पहले वाला ही रहेगा।

<code>/delete_f_captions</code> - इस आदेश से आप एक साथ जो भी कैप्शन फॉरवर्ड होने वाले मीडिया के कैप्शन में ऐड हो रहा था और जो यूजरनेम नए यूजरनेम से बदल रहा था वह एक साथ डिलीट हो जाएंगे।

<b>⚠️ ऊपर दिए गए सभी आदेश केवल चैनल में ही काम (वर्क ) करेंगे। </b> 

<b>@Lx0980AI</b> के द्वारा।
"""
      
      ADMIN_COMMAND_TXT = """
<b>केवल बॉट व्यवस्थापक ही इन आदेश का उपयोग कर सकता है।</b>

<code>/add_authorised_chat</code> - इस आदेश की मदद से बॉट व्यवस्थापक अधिकृत चैट को डेटाबेस में जोड़ सकते हैं।

<code>/delete_authorised_chat</code> - इस आदेश की मदद से बॉट व्यवस्थापक अधिकृत चैट को डेटाबेस से हटा सकते हैं।

<code>/check_authorised_chats</code> - इस आदेश की मदद से बॉट व्यवस्थापक जोड़े गए सभी अधिकृत चैट्स की सूची देख सकते हैं।

<code>/clearForwardDb</code> - इस आदेश की मदद से बॉट व्यवस्थापक सभी चैनल के फवार्डिंग कनेक्शन्स को हटा सकते हैं।

<code>/ClearCaptionDB</code>  - इस आदेश की मदद से बॉट व्यवस्थापक सभी चैनल के ऑटो कैप्शन को डेटाबेस से हटा सकते हैं। 

<code>/ClearDB</code> - इस कमांड से बोट व्यवस्थापक पूरे डेटाबेस को साफ कर सकता है या हटा सकता है।

<b>© @Lx0980AI</b>
"""
      
      MEDIA_CLONE_TXT = """
इन आदेशों की मदद से आप एक चैनल की सभी वीडियोस और फाइलों को दूसरे चैनल में क्लोन कर सकते हो उसके लिए बोट दोनों चैनल में एडमिन होना जरूरी है।
( <i>Forward Existing Messages</i> 🔃 )

/id - ID प्राप्त करें
/set_clone_skip - स्किप संदेश सेट करें। यानि उस मैसेज की आईडी जहां से फॉरवर्ड शुरू करना चाहते हैं।
/set_target_channel - लक्षित चैनल सेट करें।
/set_clone_caption - फ़ाइल कैप्शन सेट करें।

कैप्शन प्रारूप:
`{file_name}` - फ़ाइल नाम।
`{file_size}` - फ़ाइल का आकार।
`{caption}` - डिफ़ॉल्ट फ़ाइल कैप्शन। = पहले से मौजूद कैप्शन।

वर्तमान कैप्शन : (फाइल नाम) 

टारगेट चैनल, और कैप्शन सेट करने के बाद आप मुझे सोर्स चैनल से उस मैसेज को फॉरवर्ड करें <b>फॉरवर्ड टैग</b> के साथ जहां तक आप फॉरवर्ड करना चाहते हैं यानी लास्ट मैसेज जहां तक आप फॉरवर्ड करना चाहते हैं।

<b>⚠️ नोट - इस बॉट में चैनल क्लोन के लिए कोई डेटाबेस नहीं है,</b> तो आपका विवरण स्थायी रूप से सहेजा नहीं जा रहा है।  अगर बॉट रीस्टार्ट हुआ तो आपका फॉरवर्ड रुक जाएगा और आपका विवरण डिलीट हो जाएगा। 

</b>@Lx0980AI</b>
"""

      
      
      
      
      
      
      
