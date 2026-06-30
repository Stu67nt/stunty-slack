## Stunty

It does as it says on the tin. You can watch Bad Apple be played on any Slack channel stunty is in!

I decided to make this because I wanted to challenge myself to make a project within the span of 1 show and tell. 
I succeeded!

### Usage
Visit #stunty on the Hack Club Slack to test the commands!

#### Bad Apple
Run the command /badapple for it to run in 80x24 resolution.  
To customise the resolution, add the extra arguments [width] [height] to the end. (This will fail for resolutions with more than 3000 characters, for example, 110x30 will fail, but 90x70 won't)

#### Cat Photos
To generate a cat image, run /generatecat for it to run in 80x24 resolution.  
To customise the resolution, add the extra arguments [width] [height] to the end. This command works for any resolution, but to be able to properly see larger resolution images, you may need to 
zoom out (on Slack web) or have a big monitor.

#### Generate slop
To generate slop videos of a thread, either ping @stunty and say slopify like "@stunty pls slopify this thread" WITHIN THE THREAD or in a main channel, run the command /slopify. A menu will pop up where you can paste in the thread URL which you want to slopify. All other arguments are optional; however, they are explained below. If the bot is not in the channel where the thread you want to slopify is, it will not work and return an error message. Make sure to add it to the channel where the thread you want to slopify is first.

| Argument | Example | Explanation |
| -------- | ------- | ------- |
| Language | fr-FR (there are many more listed later on) | Determines the language of the voice model which should be used for the text-to-speech. It uses edge-tts which has really weird codes for the locales so they will all be stated below for ease of use. |
| Don't Translate | yes or no not much else lmao | This just lets you have a TTS model not designed to read English; read English pretty much. |
| Voice Gender | Man, Woman, I don't care | Determines whether it uses a male or female voice. I don't care chooses a random gender. |

##### All edge-tts Locales
| Locale | Language/Region |
|---|---|
| af-ZA | Afrikaans (South Africa) |
| am-ET | Amharic (Ethiopia) |
| ar-AE | Arabic (United Arab Emirates) |
| ar-BH | Arabic (Bahrain) |
| ar-DZ | Arabic (Algeria) |
| ar-EG | Arabic (Egypt) |
| ar-IQ | Arabic (Iraq) |
| ar-JO | Arabic (Jordan) |
| ar-KW | Arabic (Kuwait) |
| ar-LB | Arabic (Lebanon) |
| ar-LY | Arabic (Libya) |
| ar-MA | Arabic (Morocco) |
| ar-OM | Arabic (Oman) |
| ar-QA | Arabic (Qatar) |
| ar-SA | Arabic (Saudi Arabia) |
| ar-SY | Arabic (Syria) |
| ar-TN | Arabic (Tunisia) |
| ar-YE | Arabic (Yemen) |
| az-AZ | Azerbaijani (Latin, Azerbaijan) |
| bg-BG | Bulgarian (Bulgaria) |
| bn-BD | Bangla (Bangladesh) |
| bn-IN | Bangla (India) |
| bs-BA | Bosnian (Latin, Bosnia & Herzegovina) |
| ca-ES | Catalan (Spain) |
| cs-CZ | Czech (Czechia) |
| cy-GB | Welsh (United Kingdom) |
| da-DK | Danish (Denmark) |
| de-AT | German (Austria) |
| de-CH | German (Switzerland) |
| de-DE | German (Germany) |
| el-GR | Greek (Greece) |
| en-AU | English (Australia) |
| en-CA | English (Canada) |
| en-GB | English (United Kingdom) |
| en-HK | English (Hong Kong SAR China) |
| en-IE | English (Ireland) |
| en-IN | English (India) |
| en-KE | English (Kenya) |
| en-NG | English (Nigeria) |
| en-NZ | English (New Zealand) |
| en-PH | English (Philippines) |
| en-SG | English (Singapore) |
| en-TZ | English (Tanzania) |
| en-US | English (United States) |
| en-ZA | English (South Africa) |
| es-AR | Spanish (Argentina) |
| es-BO | Spanish (Bolivia) |
| es-CL | Spanish (Chile) |
| es-CO | Spanish (Colombia) |
| es-CR | Spanish (Costa Rica) |
| es-CU | Spanish (Cuba) |
| es-DO | Spanish (Dominican Republic) |
| es-EC | Spanish (Ecuador) |
| es-ES | Spanish (Spain) |
| es-GQ | Spanish (Equatorial Guinea) |
| es-GT | Spanish (Guatemala) |
| es-HN | Spanish (Honduras) |
| es-MX | Spanish (Mexico) |
| es-NI | Spanish (Nicaragua) |
| es-PA | Spanish (Panama) |
| es-PE | Spanish (Peru) |
| es-PR | Spanish (Puerto Rico) |
| es-PY | Spanish (Paraguay) |
| es-SV | Spanish (El Salvador) |
| es-US | Spanish (United States) |
| es-UY | Spanish (Uruguay) |
| es-VE | Spanish (Venezuela) |
| et-EE | Estonian (Estonia) |
| fa-IR | Persian (Iran) |
| fi-FI | Finnish (Finland) |
| fil-PH | Filipino (Philippines) |
| fr-BE | French (Belgium) |
| fr-CA | French (Canada) |
| fr-CH | French (Switzerland) |
| fr-FR | French (France) |
| ga-IE | Irish (Ireland) |
| gl-ES | Galician (Spain) |
| gu-IN | Gujarati (India) |
| he-IL | Hebrew (Israel) |
| hi-IN | Hindi (India) |
| hr-HR | Croatian (Croatia) |
| hu-HU | Hungarian (Hungary) |
| id-ID | Indonesian (Indonesia) |
| is-IS | Icelandic (Iceland) |
| it-IT | Italian (Italy) |
| ja-JP | Japanese (Japan) |
| jv-ID | Javanese (Indonesia) |
| ka-GE | Georgian (Georgia) |
| kk-KZ | Kazakh (Kazakhstan) |
| km-KH | Khmer (Cambodia) |
| kn-IN | Kannada (India) |
| ko-KR | Korean (South Korea) |
| lo-LA | Lao (Laos) |
| lt-LT | Lithuanian (Lithuania) |
| lv-LV | Latvian (Latvia) |
| mk-MK | Macedonian (North Macedonia) |
| ml-IN | Malayalam (India) |
| mn-MN | Mongolian (Mongolia) |
| mr-IN | Marathi (India) |
| ms-MY | Malay (Malaysia) |
| mt-MT | Maltese (Malta) |
| my-MM | Burmese (Myanmar (Burma)) |
| nb-NO | Norwegian Bokmål (Norway) |
| ne-NP | Nepali (Nepal) |
| nl-BE | Dutch (Belgium) |
| nl-NL | Dutch (Netherlands) |
| pl-PL | Polish (Poland) |
| ps-AF | Pashto (Afghanistan) |
| pt-BR | Portuguese (Brazil) |
| pt-PT | Portuguese (Portugal) |
| ro-RO | Romanian (Romania) |
| ru-RU | Russian (Russia) |
| si-LK | Sinhala (Sri Lanka) |
| sk-SK | Slovak (Slovakia) |
| sl-SI | Slovenian (Slovenia) |
| so-SO | Somali (Somalia) |
| sq-AL | Albanian (Albania) |
| sr-RS | Serbian (Cyrillic, Serbia) |
| su-ID | Sundanese (Latin, Indonesia) |
| sv-SE | Swedish (Sweden) |
| sw-KE | Swahili (Kenya) |
| sw-TZ | Swahili (Tanzania) |
| ta-IN | Tamil (India) |
| ta-LK | Tamil (Sri Lanka) |
| ta-MY | Tamil (Malaysia) |
| ta-SG | Tamil (Singapore) |
| te-IN | Telugu (India) |
| th-TH | Thai (Thailand) |
| tr-TR | Turkish (Türkiye) |
| uk-UA | Ukrainian (Ukraine) |
| ur-IN | Urdu (India) |
| ur-PK | Urdu (Pakistan) |
| uz-UZ | Uzbek (Latin, Uzbekistan) |
| vi-VN | Vietnamese (Vietnam) |
| zh-CN | Chinese (Simplified, China) |
| zh-CN-liaoning | Chinese (Simplified, China) |
| zh-CN-shaanxi | Chinese (Simplified, China) |
| zh-HK | Chinese (Traditional, Hong Kong SAR China) |
| zh-TW | Chinese (Traditional, Taiwan) |
| zu-ZA | Zulu (South Africa) |

### AI
I used Gemini and Claude to help me with regex for filtering some inputs and to help with getting and sending messages with the slack api, as well as finding some MoviePy functions, as half of the information is out of date. 
