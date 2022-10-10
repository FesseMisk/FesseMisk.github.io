---
title: "OP HOLMGANG - Writeup"
categories: Writeup
tags: writeup
published: true
toc: true 
toc_sticky: true
header:
    overlay_image: /images/2022-10-04-09-15-04.png
    overlay_filter: 0.5
    teaser: /images/2022-10-04-09-15-48.png
tagline: ""
read_time: true
date: 2022-10-07
last_modified_at: 2022-10-10
---


# Intro
OP HOLMGANG was a CTF hosted by Kripos, a special agency of the Norwegian Police Service, for the University of Oslo, but it was open to the public. Although it was a classic jepoardy-style CTF, it was special in the sence that every chall was connected up to a central incidenct. It was all made to look like an actual police investigation, which made the CTF a lot more fun. The Case Summary can be read here, [case_summary.pdf](/assets/2022-09-04-op_homlgang/case_summary.pdf).

This was the first CTF we competed in as a team, and we are very pleased with how well it went. Ending at 8th place, and possibly the highest scoring student team, was not something we envisioned beforehand. 


## Scoreboard

| Place | Team | Score |
| --- | --- | --- |
| 1 | bootplug | 130 |
| 2 | coldboots | 125 |
| 3 | RumbleInTheJungle | 125 |
| 4 | give cake | 115 |
| 5 | The Long Quay | 115 |
| 6 | Corax | 100 |
| 7 | i773 | 100 |
| 8 | FesseMisk | 95 |
| 9 | КГБ | 92 |
| 10 | støvelpropp | 90 |

## Solves for our team

| Challenge | Category | Value | Time |
| --- | --- | --- | --- |
| Solve me first | Start here | 0 | September 21st, 10:01:59 AM |
| [Password match - Shredder](#match---shredder) | Password | 3 | September 21st, 12:01:31 PM |
| [ChatTomato - Get access](#chattomato---get-access) | Chat | 5 | September 21st, 12:59:37 PM |
| [ChatTomato - Fetch contents](#chattomato---fetch-contents) | Chat | 5 | September 21st, 1:00:30 PM |
| [Password match - Belongs to whom?](#match---belongs-to-whom) | Password | 7 | September 21st, 1:02:36 PM |
| [Where's the money hidden - Phone number](#wheres-the-money-hidden---phone-number) | Location | 3 | September 21st, 1:30:14 PM |
| [Where's the money hidden - Address](#wheres-the-money-hidden---address) | Location | 4 | September 21st, 1:51:58 PM |
| [Where's the money hidden - Location](#wheres-the-money-hidden---location) | Location | 3 | September 21st, 2:20:53 PM |
| Be concrete - Methods | Chemistry | 3 | September 21st, 2:34:49 PM |
| Be concrete - Afterthought | Chemistry | 3 | September 21st, 2:38:42 PM |
| Be concrete - Conclusion | Chemistry | 4 | September 21st, 2:49:27 PM |
| Documents schmockuments - Comparison | Forgery | 5 | September 21st, 5:00:39 PM |
| [Credential Custodian](#credential-custodian) | Reversing | 10 | September 21st, 6:27:26 PM |
| [Criminal polyglot](#criminal-polyglot) | Language | 10 | September 21st, 6:49:34 PM |
| Needle in the haystack | Logs | 10 | September 21st, 10:09:36 PM |
| [Greedy Grafana Governor - Announcement date](#greedy-grafana-governor---announcement-date) | Gain access | 5 | September 21st, 11:13:16 PM |
| Documents schmockuments - Authenticity | Forgery | 5 | September 22nd, 8:34:05 AM |
| Free space | Open source intelligence | 10 | September 22nd, 9:55:55 AM |



## Credential Custodian

Credential Custodian is a program found on IVANOVICH’s computer. It includes a ciphertext and a clue that he might be hiding a bip39 seed phrase.

### Solution

Credential custodian is a program that has two functionalities. Firstly it can generate a random password. Secondly it can encrypt a text-string with the random password, and later retrieve the secret text string if you have the password. 

Looking through the first third of the program we can spot two of the essential clues to crack this challenge 

```jsx
#!/usr/bin/env python3

'''
2010-05-04: Here is the password manager you wanted; Start using it TODDAY!
2010-05-03: Implemented OWN generate_password function. Probably secure.
2010-05-02: Started development. Stole most of the code from hackexchange.
'''

import sys
import string
import random
import time
import base64

def generate_password(length=50):
    '''Return an UNPREDICTALBE password of given length'''

    random.seed(int(time.time()))
    characters =  string.digits + string.ascii_letters
    password = ''

    for i in range(length):
        offset = random.randrange(0, len(characters))
        password += characters[offset]

    return password

...
```

We can quickly notice that generate_password uses the current time as their seed. 

A seed is “the starting point” of randomness in computers, and using the same seed in the same generator will always grant exactly the same results. 

We can also see that there are a few time stamps at the start of the file, guiding us to what time IVANOVICH might have generated their password. 

The `time.time()` function is getting the current unix epoch time which equals seconds since 1.jan 1970 00.00 GMT. 

Knowing what we know we started to modify the program to be able to bruteforce the password. We know that the password was originally generated after the 3rd of may, probably the 3rd of 4th. 

Using a unix epoch time calculator we found our staring second and approximated an ending second as well. Brute forcing on a modern computer is quite fast as long as it isn’t programmed in obviously inefficient ways. In our example we included quite a few extra hours on either side resulting in over 250 000 combinations to be brute forced, and the complete program used 36 seconds. 

`generate_password()` was edited to include custom numbers as seeds rather than `time.time()`.

```python
def generate_password(t, length=50):
    '''Return an UNPREDICTALBE password of given length'''

    random.seed(t)
    characters =  string.digits + string.ascii_letters
    password = ''

    for i in range(length):
				...
```

In the running part of the code we start a brute force of all seeds and tried to decrypt the cipher text with the generated passwords. All decoded “plain text” that only included printable characters were printed, which turned out to be quite a few. 

It would be possible to search out the flag only looking at the output, but further filtering was possible. Knowing that it might be a BIP39 seed phrase the correct plain text should have 12 words. Looking for a minimum of 5 words was done like this `if len(message.split()) > 5:`, and was enough to filter out the correct flag.

```python
def main():
	if sys.argv[1] == 'generate':
	        for t in range(1272848461,1273104061):
	        	message = show_secret(generate_password(t).encode())
	        	if message.isprintable():
	        		print(message)
	        		if len(message.split()) > 5:
	        			likely = message

	        print(likely)
	
```


```
{% raw %} 
Up^*"VtP|HI'Heg&Z1dH!y`wG4@fkUvu|rt]y]ZQ)GFhiQQK^i
cPB#uj{\xcO>KdA+~fPsXAId26PJaGXqK[7~eAyHd{DId56Lyu
@}u!YyhWF6\=k9;iz,'W?PFKX-_Yeyuhhf6QhHPw6m&79C[MhI
nPo>{QL!\IF95cM\# nI?"CUc+q`X_]bt]0|wSDPf9 mMX-eth
qai$}u4T|^o.qiZBV$Le?GKP18zzPx_Gwrsgjz6If=;uJvTl}Q
lB\4GkG\LjXCMFyTs?vR:gpEr;DT]{{g]a(%*]DC4h)D{e/ut)
UbI%SK92VPf@j>a_l4dZ[QAN;'CT}HeZir,QGCR73IHH=ZTusL
wTh<\ll3T7D:jFjJU'RR=/pA4"B#se^}w$tWrzOs#i7mquVuq*
_JBap57RY4_$dkX@|"|%6&xdm/akPWgwqd!J(^4r*=&7pW9xu}
van use aim leg wall deal sad air put wide act pen
{% endraw %}
```

### Flag

`van use aim leg wall deal sad air put wide act pen`

### Files

[credential_custodian.py](/assets/2022-09-04-op_homlgang/credential_custodian.py)

[credential_custodian_solved.py](/assets/2022-09-04-op_homlgang/credential_custodian_solved.py)

# Language

## Criminal polyglot

A wiretap has intercepted a call 
from Sergei Ivanovich's telephone number, see the wav file in the case 
folder. Sergei talks with two culprits and the audio is believed to 
contain information that can identify the manufacturer of the faulty 
pipes.

The flag is an international phone number with no spaces.

Example: +4723208000

[wav.wav](/assets/2022-09-04-op_homlgang/wav.wav)

### Solution

In the wire tape he said the phone number in romanian, and afterwards mentioned the +40 in polish. 

### Flag
```
+40 21 314 54 13 
```

# Password

## Match - Shredder

A search on the premises of KALLESTAD's employer turned up some interesting shredded paper strips. Looks like someone tried to shred a password written on a post-it note. We're not sure if all the pieces were recovered. Can you piece them together?

A photo of the shredded paper strips can be found in the case folder.

The flag is the password.

Example: V3ryS3cur3PaZZw0rd

### Solution

The photo of the shredded paper strips was clearly the most important hint we got. 

![shredded.jpg](/assets/2022-09-04-op_homlgang/shredded.jpg)

One might say that you usually have two methods of solving a challenge. The smart and universal solution that solves the challenge every time in the most effective way, and there is the simple way that might be dumber, but you’ll make it work either way. The first one will often require a lot of work to get going, so we chose the “simple, lets just do it”-approach. Printing out the paper, cutting out the pieces and solving it like a ordinary puzzle.   

![IMG_20220921_115746.jpg](/assets/2022-09-04-op_homlgang/IMG_20220921_115746.jpg)

From this solution we considered a few different spellings, and we had to get it right as we only had 3 opportunities to submit the flag. 

The organizers showed of after the event that they had a ton of different spellings submitted.  Some shown below. 

![Screenshot from 2022-09-29 10-54-44.png](/assets/2022-09-04-op_homlgang/Screenshot_from_2022-09-29_10-54-44.png)

After having tried two passwords and failed twice we looked for more evidence to back up what our last submission would be.

![image1.jpg](/assets/2022-09-04-op_homlgang/image1.jpg)

This image gave us the final clue.

**140 Ton Fatberg** was an article on his working dashboard with link to the article. [https://www.businessinsider.com/this-130-tonne-fatberg-has-been-discovered-under-the-streets-of-east-london-2017-9?r=US&IR=T](https://www.businessinsider.com/this-130-tonne-fatberg-has-been-discovered-under-the-streets-of-east-london-2017-9?r=US&IR=T) 

### Flag

`140TonFatberg`

## Match - Belongs to whom

This was a followup-challenge to **Match - Shredder.** We have not saved the exact challenge text, but the challenge was to figure out whose password 140TonFatberg is. We were given a shadow-file extracted from Kallestads computer.

The flag is the user

example: uid123

### Solution

The contents of shadow looks like this. 

```csharp
...
uid269:$apr1$hLPQ2STl$VY28dnGq.a.Yv6L.hsm5f1:18298:0:99999:7:::
uid270:$6$OAnyQFwNdH$u8bjf2h8f8QeEKx9jokjAtlx.t6dc7Tn3iUE/qzuVNrFcjOKwUEPRF1XF5ktCD70CptUmgYwrf0a4wBGIEJ9O0:18226:0:99999:7:::
uid273:$apr1$YI1s8plV$hzbpGy.XacyX8.fWTD9GY/:18280:0:99999:7:::
uid274:$apr1$FOfSgJFX$reWulZST7BNPJPt4S8bY90:18291:0:99999:7:::
uid275:$5$gizTwIB5uM$7jRzJbk9XgzyOcOY.KLO1Q5aGrYei7WIDwNjfaICN21:18273:0:99999:7:::
uid276:$apr1$cyOzOE55$dZ4jjtY9MQYgj6CT5weJd/:18278:0:99999:7:::
uid277:$apr1$8apMktaJ$c4vk2A.s81CdayFF7wyUP/:18213:0:99999:7:::
uid278:$1$0ksdhyfC$pis7jlpvCysyy/Zdauqs./:18230:0:99999:7:::
uid280:$apr1$OsoDazfU$UVDJnQ4WBqT4ddWw1wz5o0:18221:0:99999:7:::
uid281:$1$KilvYCzr$mmRJriApddtoJsXkBBEON.:18268:0:99999:7:::
uid282:$5$zjcoxLw5NE$D8jcVmEBwXwIpSK4hdf0VuMyHVoTvOnYJfYSwziI7a5:18217:0:99999:7:::
uid283:$apr1$YbAYwnlm$CNNrvMWTldapx5bDcMbg9.:18213:0:99999:7:::
...
```

Firstly we tried to use john (the ripper) to crack the shadow-file with only the given password in the wordfile, but john raised a lot of unclear warnings and didn’t produce the correct result. 

```csharp
$ john shadow --wordlist=/tmp/wordlist.txt
Warning: hash encoding string length 37, type id $a
appears to be unsupported on this system; will not load such hashes.
Warning: only loading hashes of type "crypt", but also saw type "md5crypt"
Use the "--format=md5crypt" option to force loading hashes of that type instead
Loaded 192 password hashes with 192 different salts (crypt, generic crypt(3) [?/64])
Remaining 191 password hashes with 191 different salts
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
0g 0:00:00:00 100% 0g/s 1.785p/s 341.0c/s 341.0C/s 140TonFatberg
Session completed
$
```

A lot of unclear problem solving was applied and nothing gave results. 

In the end we appended the known password to a short separate passwordlist such that the new file included 50 known wrong passwords and one know correct password.

This made john function correctly and gave us the correct result. 

```haskell
john shadow --wordlist=pass.txt
> 140TonFatberg    (uid224)
```



### Flag

`uid224` 

# Chat

## **ChatTomato - Get access**

### Description:

A suspicious image was found on KALLESTAD's computer. Look in the case folder under Search and seizures. We suspect the image contains relevant information for accessing a darknet service listed at okskqu2ypqewyqk2igdath7zylsayqucdjeztlha3jvtelcc4pncshid.onion, but we are unable to extract it from the picture.

The flag is a username.

Example: SomeUser

### Solution

Bitplanes, photoshop, qrazybox

Used phtoshop to make the image more viewable. 

Then we manually recreated the QR code in [https://merricx.github.io/qrazybox/](https://merricx.github.io/qrazybox/)

![canvas.png](/assets/2022-09-04-op_homlgang/canvas.png)

**Decrypted QR code:**

user=`PipeDigger` pass=`140TonFatberg`

### Flag

`PipeDigger`

## **ChatTomato - Fetch contents**

### Description

Accessing the ChatTomato service is easy once you have the URL, username and password combo. Log in and get hold of the chat contents. We're interested in the first user that KALLESTAD chatted with.

The flag is a username.

Example: SomeUser

### Solution

Logged in to [Onion site](http://3pcy56xc56d6ej55lm3vvq2tgdsizwanq3npcvqthftxumqp6verytid.onion/chattomato/rooms/228625664_1503454667/reader.html) with user=`PipeDigger`and pass=`140TonFatberg`

![Untitled](/assets/2022-09-04-op_homlgang/Untitled.png)

### Flag

`Yosemite`

[chat.pdf](/assets/2022-09-04-op_homlgang/chat.pdf)

## Gain access

### **Greedy Grafana Governor - Announcement date**

The revenue and related announcements is available in a Grafana database. The URL is found in the case folder. We don't have access but maybe you can get hold of the database somehow?

Can you look for any announcements regarding decreasing revenue and report back any relevant dates.

Tha flag is a date in ISO-format: YYYY-MM-DD.

Example: 2022-01-01

### Solution

Googling around we found that grafana had a [path traversal vulnerability](https://www.exploit-db.com/exploits/50581). We used metasploit to download the database and find the flag.

Metasploit

`msf6 auxiliary(scanner/http/grafana_plugin_traversal) > set filepath /var/lib/grafana/grafana.db`

### Flag

`2010-05-01`

## ****Greedy Grafana Governor - Password****

Looking into the “grafana.db” we found in previous task. To make it easier to search around in the database, I downloaded “DB Browser for SQlite”, and opened the .db file there. Under table “User”, we find a hashed password with salt and rand to user IVANOVICH.

![Untitled](/assets/2022-09-04-op_homlgang/Untitled%201.png)


# Location

## Where's the money hidden - Phone number

### Description

According to photos in the cases 
folder, Mr and Mrs Mørkved have been dining at a restaurant. What is the
 phone number of the restaurant?

The flag is the phone number, including country code, but without any signs or pauses.

Example: 479988776655

![Image3408.jpg](/assets/2022-09-04-op_homlgang/Image3408.jpg)

![Image3409.jpg](/assets/2022-09-04-op_homlgang/Image3409.jpg)

Googling `ersete security club resturant croatia` we find this link:

[https://www.sail-croatia.com/set-sail/sailing-croatian-restaurants-route](https://www.sail-croatia.com/set-sail/sailing-croatian-restaurants-route)

Here we see this picture:

![Screenshot 2022-09-21 132700.png](/assets/2022-09-04-op_homlgang/Screenshot_2022-09-21_132700.png)

Which is in the same location. Doing a reverse image search on this image we find it is from the following restaurant: [Konoba Bako](https://www.tripadvisor.com/Restaurant_Review-g424973-d1462116-Reviews-Konoba_BAKO-Vis_Island_of_Vis_Split_Dalmatia_County_Dalmatia.html#MAPVIEW)

A resturant really close by **[Konoba Jastožera](https://www.tripadvisor.com/Restaurant_Review-g1062125-d8432167-Reviews-Konoba_Jastozera-Komiza_Island_of_Vis_Split_Dalmatia_County_Dalmatia.html)**, Seems to be the correct resturant. 

### Flag

`385919842513`

## Where's the money hidden - Location

### Description

Mr KALLESTAD has an apartment abroad. What are the GPS coordinates?

The flag is the GPS coordinates in decimal degrees form:

- Latitude first and then longitude: lat, lon
- Use a dot (.) as the decimal point in your coordinates: 12.1234
- Coordinates can be negative: -12.1234, -10.3456
- Use a comma and/or space to separate lat and lon: 12.1234, 23.2345
- Coordinates should have FOUR decimal places

Example: 39.0581, -1.9872

![IMG_9502.JPG](/assets/2022-09-04-op_homlgang/IMG_9502.jpg)

![IMG_9461.JPG](/assets/2022-09-04-op_homlgang/IMG_9461.jpg)

### Solution

On the one picture we can see a Swedish restaurant and their phone number. Googling them gave us a address in Torrevieja Spain which matched up with the photos. We had the correct location. In the police report it is stated that Kallestad texted

*"Hi Sergei. You know the street name, and the number of the apartment
with the red ring on it, is 22. Hope to see you soon, Robbans Pizzario is near by and very
nice It's about a 500m walk".*

Thus we know its about a 500m walk. We can also see from the pictures that is has a red pavement, is located in a small hill, have a right turn and has a few tall apartments in the background. Searching the area we found the tall apartments. Further search round that area gave result with the red pavement and a right turn which turned out to be the correct position of the photo. Then opening google maps and right-clicking on the balcony from the picture resulted in the correct coordinates. 

[Google earth](https://earth.google.com/web/search/C.+Granada,+5,+Torrevieja,+Spain/@38.00456615,-0.65358012,40.60143652a,0d,60y,21.18704986h,85t,0r/data=CigiJgokCYF14CyZAENAERkZtV1uAENAGQRdFVTx8uS_IRitL124_uS_IhoKFmM1Z1NlZXA4MUlOUGoyb0dvMnVEWmcQAjoDCgEw?authuser=0)

### Flag

`38.0045, -0.6536`

## ****Where's the money hidden - Address****

We found a picture of the watchtower and the appartment in the task “Where's the money hidden - Phone number” - and figured out this was in KOMIŽA, Croatia. Using Google Maps, we navigate to the watchtower, and from there look at pictures nearby. The flag was found on [this](https://www.google.com/maps/place/Ul.+Riva+Svetoga+Mikule+2,+21485,+Komi%C5%BEa,+Kroatia/@43.0439957,16.0883026,3a,75y,149.29h,92.38t/data=!3m6!1e1!3m4!1slyF2rhvBIRpZOFBPL5jqwQ!2e0!7i13312!8i6656!4m5!3m4!1s0x1335bc3e107739e3:0xfd9042829b62694e!8m2!3d43.0439704!4d16.0883704?hl=nb) picture

![Untitled](/assets/2022-09-04-op_homlgang/Untitled%202.png)

### Flag

`2`